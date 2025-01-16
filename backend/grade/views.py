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

# db = dc('devicedp')
tbl = 'auth_grade'

grade_fields = {
	'GID': {'as': 'gid', 'type': 'str'},
	'Grade': {'as': 'grade', 'type': 'str'},
	'Add': {'as': 'add', 'type': 'str'},
	'Edit': {'as': 'edit', 'type': 'str'},
	'Delete': {'as': 'delete', 'type': 'str'},
	'Search': {'as': 'search', 'type': 'str'},
	'View': {'as': 'view', 'type': 'str'},
	'Export': {'as': 'export', 'type': 'str'},
	'Download': {'as': 'download', 'type': 'str'},
	'RecordTime': {'as': 'recordtime', 'type': 'str'},
}

@csrf_exempt
def grade_list(request):
    logger.info(f'grade_list, method = {request}')
    res = {
        'code': 20000,
        'data': {
            'items': [],
        },
    }

    try:
        l_fields = ','.join([f'`{field}`' for field in grade_fields.keys()])
        sql = f'select {l_fields} from {tbl}'
        ttype = request.GET['type']
        if ttype == 'single':
            id = request.GET['gid']
            sql = f'{sql} where `GID` = "{id}" '
        logger.info(f'sql = {sql}')
        db = dc('devicedp')
        df = db.read_query(sql)
        for i_index in df.index:
            item = {}
            for field in grade_fields.keys():
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


def handle_grade_edit(tbl, data):
    generated_str = u.generate_update_sql(grade_fields, data, ['RecordTime'])

    sql = 'update {tbl} set {fields} where `GID` = "{GID}"'.format(
        tbl=tbl,
        fields=generated_str,
        GID=data['GID']
    )
    logger.debug(f'handle_grade_edit, sql = {sql}')
    db = dc('devicedp')
    db.execute(sql)

    pass

def handle_grade_add(tbl, data):
    l_data = data
    
    l_data['GID'] = u.strNum(u.gen_tbl_index(tbl, 'GID', db), 'G', 6)

    generated_str = u.generate_insert_sql(grade_fields, l_data, skip=['RecordTime'])

    sql = "insert into {tbl} ({fields}) values ({values})".format(
            tbl=tbl,
            fields=generated_str[0],
            values=generated_str[1]
        )
    logger.info(f'handle_grade_add: sql = {sql}')
    db = dc('devicedp')
    db.execute(sql)
    rt =  'Add successful, back and refresh page to show it'

    return rt
    pass

@csrf_exempt
def grade_edit(request):
    logger.info(f'executing grade_edit {request.body} ......')
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
        for field in grade_fields.keys():
            if field == "RecordTime":
                continue
            # as_field = grade_fields[field]['as']   
            if field in req.keys():
                l_data[field] = req[field]

        if request.method == "POST":
            rt = handle_grade_add(tbl, l_data)
            res['data']['status'] = rt  
        elif request.method == "PUT":
            handle_grade_edit(tbl, l_data)
            res['data']['status'] = "Edit successful"
    except Exception as e:
        res['code'] = 20001
        logger.info(f"exception caught: {e}")
    
    return HttpResponse(simplejson.dumps(res), content_type='application/json')


@csrf_exempt
def grade_delete(request):
    logger.info(f'executing grade_delte {request.body} ......')
    res = {
        'code': 20000
    }

    try:
        req = json.loads(request.body.decode('utf-8'))
        mail = req['mail']
        ids = req['id']

        sql = 'delete from {tbl} where `GID` in ({B_LIST})'.format(
            tbl=tbl,
            B_LIST=u.generate_delete_sql(ids)
        )
        logger.info(f'grade_delete, sql = {sql}')
        db = dc('devicedp')
        db.execute(sql)
    except Exception as e:
        logger.info(f"exception caught: {e}")
        res['code'] = 20001

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

    
@csrf_exempt
def role_list(request):
    logger.info(f'role_list, method = {request}')
    res = {
        'code': 20000,
        'data': {
            'items': [],
        },
    }

    try:
        sql = 'SELECT distinct `Grade` FROM `auth_grade` '
        ttype = request.GET['type']
        logger.info(f'sql = {sql}')
        db = dc('devicedp')
        df = db.read_query(sql)
        for i_index in df.index:
            item = {}
            item['Grade'] = df.at[i_index, 'Grade']
            res['data']['items'].append(item)
    except Exception as e:
        logger.info(f"exception caught: {e}")
        res['code'] = 20001

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

