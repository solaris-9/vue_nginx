from django.shortcuts import render,redirect

# Create your views here.

#from datetime import datetime, timedelta
import simplejson
import json
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse, Http404
from pymysql.converters import escape_string
from django.conf import settings
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

# db = dc('requestdb')
tbl = 'tbl_nwcc'

table_fields = {
	'ID': {'type': 'str'},
	'field_customer': {'type': 'str'},
    'field_status': {'type': 'str'},
    'field_assignee': {'type': 'str'},
    # 'field_mail': {'type': 'str'},
    'field_jira_id': {'type': 'str'},
    'field_customer_id': {'type': 'str'},
    'field_country': {'type': 'str'},
    'field_hosted_by': {'type': 'str'},
    'field_tenant_type': {'type': 'str'},
    'field_hc_type': {'type': 'str'},
    'field_alive_date': {'type': 'str'},
    'field_dedicated_region': {'type': 'str'},
    'field_hosting_platform': {'type': 'str'},
    'field_dedicated_legal_clearance': {'type': 'str'},
    'field_multi_region': {'type': 'str'},
    'field_multi_legal_clearance': {'type': 'str'},
    'field_trial_type': {'type': 'str'},
    'field_trial_tenant': {'type': 'str'},
    'field_trial_other_tenant': {'type': 'str'},
    'field_trial_date': {'type': 'str'},
    'field_trial_device_number': {'type': 'str'},
    'field_trial_test_plan': {'type': 'str'},
    'field_3_month': {'type': 'str'},
    'field_6_month': {'type': 'str'},
    'field_12_month': {'type': 'str'},
    'field_committed_1st_year': {'type': 'str'},
    'field_fcc_compilance': {'type': 'str'},
    'field_support_level': {'type': 'str'},
    'field_deploy_region': {'type': 'str'},
    'field_integration_corteca': {'type': 'str'},
    'field_hdm_po': {'type': 'str'},
    'field_advance_fingerprinting': {'type': 'str'},
    'field_customer_responsible': {'type': 'str'},
    'field_wbs_billing': {'type': 'str'},
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
        db = dc('requestdb')
        df = db.read_query(sql)
        df = df.replace({np.nan: None}).fillna('').infer_objects(copy=False)
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
    db = dc('requestdb')
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
    # l_data['ID'] = u.strNum(u.gen_tbl_index(tbl, 'ID', db), 'DEVICEDP-', 10)
    db = dc('requestdb')
    l_data['ID'] = u.strNum(u.gen_tbl_index(tbl, 'ID', db), 'NWCC-', 10)

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
        db = dc('requestdb')
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

    

