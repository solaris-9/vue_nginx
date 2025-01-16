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
from util.database import DatabaseConnector as dc
from util.mail import mail
from utils import Jira as Jira
import pandas as pd
import numpy as np
import dproject.utils as u
import logging
from dproject import settings as rs
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django")

# db = dc('devicedp')
tbl = 'tbl_devicedp'

table_fields = {
	'ID': {'type': 'str'},
	'field_customer': {'type': 'str'},
    'field_status': {'type': 'str'},
    'field_assignee': {'type': 'str'},
    #'field_mail': {'type': 'str'},
    'field_jira_id': {'type': 'str'},
    'field_root_device': {'type': 'str'},
    'bizline': {'type': 'str'},
    'field_product_variant': {'type': 'str'},
    'field_managed_by_hc': {'type': 'str'},
    'field_managed_by_hdm': {'type': 'str'},
    'field_home_controller': {'type': 'str'},
    'field_root_update_method': {'type': 'str'},
    'field_separate_license': {'type': 'str'},
    'field_auto_ota': {'type': 'str'},
    'field_waiver': {'type': 'str'},
    'field_boeng_rule': {'type': 'str'},
    'field_whitelisting_method': {'type': 'str'},
    'field_ip_ranges': {'type': 'str'},
    'field_customer_id': {'type': 'str'},
    'field_csv_file': {'type': 'str'},
    'field_boeng_options': {'type': 'str'},
    'field_acs_url': {'type': 'str'},
    'field_acs_username': {'type': 'str'},
    'field_acs_password': {'type': 'str'},
    'field_usp_addr': {'type': 'str'},
    'field_usp_port': {'type': 'str'},
    'field_mesh_extended': {'type': 'str'},
    'field_extender_beacon': {'type': 'str'},
    'field_extender_update_method': {'type': 'str'},
    'field_extender_separate_license': {'type': 'str'},
    'field_extender_auto_ota': {'type': 'str'},
    'field_extender_waiver': {'type': 'str'},
    'field_ouid': {'type': 'str'},
	'field_additional': {'type': 'str'},
    'creator': {'type': 'str'},
    'createon': {'type': 'str'},
    'modifier': {'type': 'str'},
    'modifiedon': {'type': 'str'},
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
            id = request.GET['ID']
            sql = f'{sql} where `Id` = "{id}" '
        logger.info(f'sql = {sql}')
        db = dc('devicedp')
        df = db.read_query(sql)
        with pd.option_context('future.no_silent_downcasting', True):
            df = df.replace({np.nan: None}).fillna('')
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
    generated_str = u.generate_update_sql(table_fields, data, ['creator', 'createon'])

    sql = 'update {tbl} set {fields} where `Id` = "{id}"'.format(
        tbl=tbl,
        fields=generated_str,
        id=data['ID']
    )
    logger.debug(f'handle_edit, sql = {sql}')
    db = dc('devicedp')
    db.execute(sql)

    # sending email
    tto = []
    if 'modifier' in data.keys() and data['modifier'] is not None:
        tto.append(data['modifier'])
    if 'creator' in data.keys() and data['creator'] is not None:
        tto.append(data['creator'])
    if 'field_assignee' in data.keys() and data['field_assignee'] is not None and len(data['field_assignee']) > 0:
        tto.append(data['field_assignee'])

    logging.debug(f'tto = {tto}')

    subject = f"{data['ID']}: updated"
    body = f"""
    ID: {data['ID']}
    Modifier: {data['modifier']}
    Status: {data['field_status']}
    Assignee: {data['field_assignee']}
    """
    mail(tto, subject, body)
    pass

def handle_add(tbl, data):
    l_data = data
    logger.info(f'handle_add, data = f{data}')
    db = dc('devicedp')
    l_data['ID'] = u.strNum(u.gen_tbl_index(tbl, 'ID', db), 'DEVICEDP-', 10)

    generated_str = u.generate_insert_sql(table_fields, l_data, skip=['modifier', 'modifiedon'])

    sql = "insert into {tbl} ({fields}) values ({values})".format(
            tbl=tbl,
            fields=generated_str[0],
            values=generated_str[1]
        )
    logger.info(f'handle_add: sql = {sql}')
    
    db.execute(sql)
    rt =  'Add successful, back and refresh page to show it'

    # sending email
    tto = []
    if 'creator' in data.keys() and data['creator'] is not None:
        tto.append(data['creator'])
    if 'field_assignee' in data.keys() and data['field_assignee'] is not None and len(data['field_assignee']) > 0:
        tto.append(data['field_assignee'])

    logging.debug(f'tto = {tto}')

    subject = f"{data['ID']}: created"
    body = f"""
    ID: {data['ID']}
    Creator: {data['creator']}
    Status: {data['field_status']}
    Assignee: {data['field_assignee']}
    """
    mail(tto, subject, body)
    return rt
    pass

@csrf_exempt
def edit(request):
    logger.info(f'executing edit {request.body} ......')
    res = {
        'code': 20000,
        'data': {},
    }

    try:
        req = json.loads(request.body.decode('utf-8'))
        #logger.info(f'req = f{req}')
        mail = req['mail']
        logger.info(f"mail = {mail}")
        l_data = {}
        for field in table_fields.keys():
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
        mmail = req['mail']
        ids = req['id']

        sql = 'delete from {tbl} where `Id` in ({LIST})'.format(
            tbl=tbl,
            LIST=u.generate_delete_sql(ids)
        )
        logger.info(f'delete, sql = {sql}')
        db = dc('devicedp')
        db.execute(sql)
    except Exception as e:
        logger.info(f"exception caught: {e}")
        res['code'] = 20001

    # sending email
    tto = [mmail]
    logging.info(f'tto = {tto}')

    subject = f'{ids}: deleted'
    body = f"""
    Tickets deleted: {ids}
    Deleted by: {mmail}
    """
    logging.info(f'subject = {subject}')
    logging.info(f'body = {body}')
    mail(tto, subject, body)

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

    

