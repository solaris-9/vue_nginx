from django.shortcuts import render,redirect

# Create your views here.

#from datetime import datetime, timedelta
import simplejson
import json
import os
import shutil
import smtplib 
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse, Http404
from pymysql.converters import escape_string
from django.conf import settings
from utils import analyzer_db
from utils import DatabaseConnector as dc
from utils import Jira as Jira
import pandas as pd
import numpy as np
import dproject.utils as u
import logging
from dproject import settings as rs
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django")

# db = dc('requestdb')
tbl = 'auth_user'

table_fields = {
	'Id': {'as': 'id', 'type': 'str'},
	'Username': {'as': 'username', 'type': 'str'},
	'FirstName': {'as': 'firstname', 'type': 'str'},
	'LastName': {'as': 'lastname', 'type': 'str'},
	'FullName': {'as': 'fullname', 'type': 'str'},
	'Email': {'as': 'email', 'type': 'str'},
	'Roles': {'as': 'roles', 'type': 'str'},
	'Level': {'as': 'level', 'type': 'str'},
	'LastLogin': {'as': 'lastlogin', 'type': 'str'},
}

@csrf_exempt
def list(request):
    logger.info(f'list, method = {request}')
    res = {
        'code': 20000,
        'data': {
            'items': [],
        },
    }

    try:
        l_fields = ','.join([f'`{field}`' for field in table_fields.keys()])
        sql = f'select {l_fields} from {tbl}'
        ttype = request.GET['type']
        if ttype == 'single':
            id = request.GET['id']
            sql = f'{sql} where `Id` = "{id}" '
        logger.info(f'sql = {sql}')
        db = dc('requestdb')
        df = db.read_query(sql)
        for i_index in df.index:
            item = {}
            for field in table_fields.keys():
                if type(df.at[i_index, field]) == pd.Timestamp:
                    item[field] = str(df.at[i_index, field])
                elif type(df.at[i_index, field]) == np.int64:
                    item[field] = int(df.at[i_index, field])
                else:
                    item[field] = df.at[i_index, field]
            res['data']['items'].append(item)
    except Exception as e:
        logger.info(f"exception caught: {e}")
        res['code'] = 20001

    return HttpResponse(simplejson.dumps(res), content_type='application/json')


def handle_edit(tbl, data):
    generated_str = u.generate_update_sql(table_fields, data, ['LastLogin'])

    sql = 'update {tbl} set {fields} where `Id` = "{id}"'.format(
        tbl=tbl,
        fields=generated_str,
        id=data['Id']
    )
    logger.debug(f'handle_edit, sql = {sql}')
    db = dc('requestdb')
    db.execute(sql)

    pass

def handle_add(tbl, data):
    l_data = data
    
    #l_data['Id'] = u.strNum(u.gen_tbl_index(tbl, 'Id', db), 'G', 6)

    generated_str = u.generate_insert_sql(table_fields, l_data, skip=['Id', 'LastLogin'])

    sql = "insert into {tbl} ({fields}) values ({values})".format(
            tbl=tbl,
            fields=generated_str[0],
            values=generated_str[1]
        )
    logger.info(f'handle_add: sql = {sql}')
    db = dc('requestdb')
    db.execute(sql)
    rt =  'Add successful, back and refresh page to show it'

    return rt
    pass

@csrf_exempt
def edit(request):
    logger.info(f'executing edit {request.body} ......')
    res = {
        'code': 20000,
        'data': {
        },
    }

    try:
        req = json.loads(request.body.decode('utf-8'))
        mail = req['mail']
        logger.info(f"mail = {mail}")
        l_data = {}
        for field in table_fields.keys():
            if field == "LastLogin":
                continue
            # as_field = table_fields[field]['as']
            if field in req.keys():
                l_data[field] = req[field]

        if request.method == "POST":
            rt = handle_add(tbl, l_data)
            res['data']['status'] = rt  
        elif request.method == "PUT":
            handle_edit(tbl, l_data)
            res['data']['status'] = "Edit successful"
    except Exception as e:
        res['code'] = 20001
        logger.info(f"exception caught: {e}")
    
    return HttpResponse(simplejson.dumps(res), content_type='application/json')


@csrf_exempt
def delete(request):
    logger.info(f'executing delte {request.body} ......')
    res = {
        'code': 20000
    }

    try:
        req = json.loads(request.body.decode('utf-8'))
        mail = req['mail']
        ids = req['id']

        sql = 'delete from {tbl} where `Id` in ({LIST})'.format(
            tbl=tbl,
            LIST=u.generate_delete_sql(ids)
        )
        logger.info(f'delete, sql = {sql}')
        db = dc('requestdb')
        db.execute(sql)
    except Exception as e:
        logger.info(f"exception caught: {e}")
        res['code'] = 20001

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

    

