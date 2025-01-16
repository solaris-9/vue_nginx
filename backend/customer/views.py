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
from util.sql import generate_select_as_sql
from util.jira import Jira as Jira
import pandas as pd
import numpy as np
import dproject.utils as u
import logging
from dproject import settings as rs
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django")

#db = dc('bbddb')
tbl = 'jira_issues_cust'

table_fields = {
	'field_jira_id': {'col': 'Key', 'jira': 'key', 'update': 'none'},
	'field_customer_name': {'col': 'Summary', 'jira': 'summary', 'update': 'text'},
    'field_customer_id': {'col': 'CustomerReferenceNumber', 'jira': 'customfield_14555', 'update': 'text'},
    'field_description': {'col': 'Description', 'jira': 'description', 'update': 'text'},
    'field_customer_olcs': {'col': 'CustomerReference', 'jira': 'customfield_51694', 'update': 'text'},
    'field_customer_impact': {'col': 'CustomerImpact', 'jira': 'customfield_46695', 'update': 'text'},
    'field_ont_plm': {'col': 'PLMPrime', 'jira': 'customfield_18893', 'update': 'name'},
    'field_nwf_plm': {'col': 'PLMContact', 'jira': 'customfield_37445', 'update': 'name'},
    'field_fwa_plm': {'col': 'ProductManager', 'jira': 'customfield_37783', 'update': 'name'},
    'field_local_contact': {'col': 'CustomerAccountManager', 'jira': 'customfield_38490', 'update': 'name'},
}

# @csrf_exempt
# def list(request):
#     logger.info(f'list, method = {request}')
#     res = {
#         'code': 20000,
#         'data': {
#             'items': [],
#         },
#     }

#     try:
#         #l_fields = ','.join([f'`{field}`' for field in table_fields.keys()])
#         sql = 'SELECT {fields} FROM {tbl} '.format(
#             fields=u.generate_select_as_sql(table_fields),
#             tbl=tbl
#         )
#         ttype = request.GET['type']
#         if ttype == 'all':
#             sql = f'{sql} ORDER BY field_jira_id'
#         elif ttype == 'single':
#             id = request.GET['ID']
#             sql = f'{sql} where `Id` = "{id}" '

#         logger.info(f'sql = {sql}')

#         df = db.read_query(sql)
#         for i_index in df.index:
#             item = {}
#             for field in table_fields.keys():
#                 if type(df.at[i_index, field]) == pd.Timestamp:
#                     item[field] = str(df.at[i_index, field])
#                 elif type(df.at[i_index, field]) == np.int64:
#                     item[field] = int(df.at[i_index, field])
#                 else:
#                     item[field] = df.at[i_index, field]
#             res['data']['items'].append(item)
#     except Exception as e:
#         logger.info(f"exception caught: {e}")
#         res['code'] = 20001

#     return HttpResponse(simplejson.dumps(res), content_type='application/json')
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
        jira = Jira()
        i_start = 0
        i_total = 500
        i_max = 500
        fields = [table_fields[field]['jira'] for field in table_fields.keys()]
        jql = 'project = BBDCUST and issuetype = "New Customer" order by key ASC'
        params = {
            'jql': jql,
            'fields': ','.join(fields),
            'maxResults': i_max
        }

        logger.info(f'jql = {jql}')
        logger.info(f'params = {params}')

        while i_start < i_total:
            params['startAt'] = i_start
            resp = jira.get('rest/api/latest/search', params)
            if not resp.ok:
                logger.info(f'Start: {i_start} failed!!!')
                continue
            result = resp.json()
            i_start += result['maxResults']
            i_total = result['total']
            logger.info(f'startAt: {i_start}, total: {i_total}')
            issues = result['issues']
            for issue in issues:
                item = {}
                for field in table_fields.keys():
                    jira_field = table_fields[field]['jira']
                    if jira_field == 'key':
                        item[field] = issue[jira_field]
                    else:
                        if issue['fields'][jira_field] is None:
                            item[field] = ""
                        else:
                            if table_fields[field]['update'] == 'name':
                                item[field] = issue['fields'][jira_field]['emailAddress']
                            else:
                                item[field] = issue['fields'][jira_field].strip()
                res['data']['items'].append(item)
    except Exception as e:
        logger.info(f"exception caught: {e}")
        res['code'] = 20001

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

def handle_edit_jira(data, mail):
    logger.info(f'handle_add_jira: {data}')
    key = data["field_jira_id"]
    logger.info(f'handle_add_jira: key = {key}')

    # email -> uname mapping
    d_cus = dc('customerdb')
    df = d_cus.read_table('file_issues_engineer')
    mail_map = {}
    for i_index in df.index:
        mail_map[df.at[i_index, 'Email'].strip().lower()] = df.at[i_index, 'CSL'].strip()

    uname = ""
    if mail.strip().lower() in mail_map.keys():
        logger.info(f'{mail.strip().lower()} in mail_map.keys')
        uname = mail_map[mail.strip().lower()]
    ont = ""
    logger.info(f'{data["field_ont_plm"].strip().lower()}')
    if data['field_ont_plm'].strip().lower() in mail_map.keys():
        logger.info(f'{data["field_ont_plm"].strip().lower()} in mail_map.keys')
        ont = mail_map[data['field_ont_plm'].strip().lower()]
    nwf = ""
    if data['field_nwf_plm'].strip().lower() in mail_map.keys():
        nwf = mail_map[data['field_nwf_plm'].strip().lower()]
    fwa = ""
    if data['field_fwa_plm'].strip().lower() in mail_map.keys():
        fwa = mail_map[data['field_fwa_plm'].strip().lower()]
    local = ""
    if data['field_local_contact'].strip().lower() in mail_map.keys():
        local = mail_map[data['field_local_contact'].strip().lower()]

    param = {
        "update": {
            "summary": [{
                "set": f"{data['field_customer_name']}"
            }],
            "description": [{
                "set": f"{data['field_description']}"
            }],
            "customfield_14555": [{
                "set": f"{data['field_customer_id']}"
            }],
            "customfield_18893": [{
                "set": {
                    "name": f"{ont}"
                }
            }],
            "customfield_37445": [{
                "set": {
                    "name": f"{nwf}"
                }
            }],
            "customfield_37783": [{
                "set": {
                    "name": f"{fwa}"
                }
            }],
            "customfield_38490": [{
                "set": {
                    "name": f"{local}"
                }
            }]
        }
    }
    logger.info(f'handle_edit_jira, param= {param.__str__()}')

    jira = Jira()
    rsp = jira.put_with_resp(f'rest/api/latest/issue/{key}', param)
    logger.info(f'rsp = {rsp}')
    if rsp.ok:
        logger.info(f'handle_edit_jira, OK')
        return 'Edit succefull'
    else:
        logger.info(f'handle_edit_jira failed: {rsp.json()}')
        return None

def handle_edit(tbl, data, mail):
    # generated_str = u.generate_update_sql(table_fields, data, ['creator', 'createon'])

    # sql = 'update {tbl} set {fields} where `Id` = "{id}"'.format(
    #     tbl=tbl,
    #     fields=generated_str,
    #     id=data['ID']
    # )
    # logger.debug(f'handle_edit, sql = {sql}')
    # db.execute(sql)
    handle_edit_jira(data, mail)
    pass

def handle_add_jira(data, mail):
    logger.info(f'handle_add_jira: {data}')
    customer = data["field_customer_name"]
    desc = data["field_description"]
    #mail = data["AddedBy"]
    logger.info(f'handle_add_jira, {customer}')
    jira = Jira()

    # email -> uname mapping
    d_cus = dc('customerdb')
    df = d_cus.read_table('file_issues_engineer')
    mail_map = {}
    for i_index in df.index:
        mail_map[df.at[i_index, 'Email'].strip().lower()] = df.at[i_index, 'CSL'].strip()

    
    uname = ""
    if mail.strip().lower() in mail_map.keys():
        logger.info(f'{mail.strip().lower()} in mail_map.keys')
        uname = mail_map[mail.strip().lower()]
    ont = ""
    logger.info(f'{data["field_ont_plm"].strip().lower()}')
    if data['field_ont_plm'].strip().lower() in mail_map.keys():
        logger.info(f'{data["field_ont_plm"].strip().lower()} in mail_map.keys')
        ont = mail_map[data['field_ont_plm'].strip().lower()]
    nwf = ""
    if data['field_nwf_plm'].strip().lower() in mail_map.keys():
        nwf = mail_map[data['field_nwf_plm'].strip().lower()]
    fwa = ""
    if data['field_fwa_plm'].strip().lower() in mail_map.keys():
        fwa = mail_map[data['field_fwa_plm'].strip().lower()]
    local = ""
    if data['field_local_contact'].strip().lower() in mail_map.keys():
        local = mail_map[data['field_local_contact'].strip().lower()]
    param = {
        "fields": {
            "project": {"key": "BBDCUST"},
            "summary": f"{customer}",
            "description": f"{desc}",
            "issuetype": {"id": "15401"},
            "reporter": {"name": f"{uname}"},
            "customfield_14555": f"{data['field_customer_id']}",
            "customfield_18893": {"name": f"{ont}"},
            "customfield_37445": {"name": f"{nwf}"},
            "customfield_37783": {"name": f"{fwa}"},
            "customfield_38490": {"name": f"{local}"},
        }
    }
    logger.info(f'handle_new_customer_add, param= {param.__str__()}')
    rsp = jira.post_with_resp('rest/api/latest/issue', param)
    logger.info(f'rsp = {rsp}')
    if rsp.ok:
        new_key = rsp.json()['key']
        logger.info(f'handle_new_customer_add, Created new key = {new_key}')
        return new_key
    else:
        logger.info(f'handle_new_customer_add failed: {rsp.json()}')
        return None
    pass


def handle_add(tbl, data, mail):
    l_data = data
    logger.info(f'handle_add, data = {data}')

    rsp = handle_add_jira(data, mail)
    if rsp is None:
        logger.info('handle_new_customer_add failed!!!')
        return 'New Customer Add failed'
    l_fields = ','.join([f'`{f}`' for f in table_fields] + ['`Key`'])
    l_values = ','.join([f'"{v}"' for v in [data[k] for k in table_fields]] + [f'"{rsp}"'])
    sql = "insert into {tbl} ({fields}) values ({values})".format(
        tbl=tbl,
        fields=l_fields,
        values=l_values
    )
    logger.info(f'handle_new_customer_add: {sql}')
    db = dc('bbddb')
    db.execute(sql)
    return 'New Customer Add successful'

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
            rt = handle_add(tbl, l_data, mail)
            res['data']['status'] = rt  
        elif request.method == "PUT":
            handle_edit(tbl, l_data, mail)
            res['data']['status'] = "Edit successful"
    except Exception as e:
        res['code'] = 20001
        logger.info(f"exception caught: {e}")
    
    return HttpResponse(simplejson.dumps(res), content_type='application/json')


# @csrf_exempt
# def delete(request):
#     logger.info(f'executing delte {request.body} ......')
#     res = {
#         'code': 20000
#     }

#     try:
#         req = json.loads(request.body.decode('utf-8'))
#         mail = req['mail']
#         ids = req['id']

#         sql = 'delete from {tbl} where `Id` in ({LIST})'.format(
#             tbl=tbl,
#             LIST=u.generate_delete_sql(ids)
#         )
#         logger.info(f'delete, sql = {sql}')

#         db.execute(sql)
#     except Exception as e:
#         logger.info(f"exception caught: {e}")
#         res['code'] = 20001

#     return HttpResponse(simplejson.dumps(res), content_type='application/json')

    

