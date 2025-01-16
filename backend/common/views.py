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
from utils import Jira as Jira
import pandas as pd
import numpy as np
import dproject.utils as u
import logging
import uuid
from dproject import settings as rs
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("django")

#db = dc('devicedp')

@csrf_exempt
def contacts_list(request):
    res = {
        'code': 20000,
        'data': {
            'items': [],
        },
    }
    cus = dc('bbddb')
    sql = "SELECT `Summary` as customer, `Key` as id, `CustomerReferenceNumber` as `cid` FROM `jira_issues_cust`"
    logger.debug(f'fetch_customer: {sql}')
    df = cus.read_query(sql)
    l_customers = {}
    for i_index in df.index:
        #l_customers.append({'customer': df.at[i_index, 'customer'], 'key': df.at[i_index, 'key']})
        l_customers[df.at[i_index, 'customer']] = {
            'id': df.at[i_index, 'id'],
            'cid': df.at[i_index, 'cid']
        }

    for cus in l_customers.keys():
            res['data']['items'].append({
                'customer': cus,
                'key': l_customers[cus]['id'],
                'cid': l_customers[cus]['cid']
            })
    return HttpResponse(simplejson.dumps(res), content_type='application/json')



@csrf_exempt
def customer_list(request):
    res = {
        'code': 20000,
        'data': {
            'items': [],
        },
    }
    cus = dc('bbddb')
    sql = "SELECT `Summary` as customer, `Key` as id, `CustomerReferenceNumber` as `cid` FROM `jira_issues_cust`"
    logger.debug(f'fetch_customer: {sql}')
    df = cus.read_query(sql)
    l_customers = {}
    for i_index in df.index:
        #l_customers.append({'customer': df.at[i_index, 'customer'], 'key': df.at[i_index, 'key']})
        l_customers[df.at[i_index, 'customer']] = {
            'id': df.at[i_index, 'id'],
            'cid': df.at[i_index, 'cid']
        }

    local_sql = 'SELECT `Customer` as customer, `Key` as id FROM `tbl_local_customers`'
    logger.debug(f'fetch_customer: {local_sql}')
    db = dc('devicedp')
    local_df = db.read_query(local_sql)
    for i_index in local_df.index:
        l_cus = local_df.at[i_index, 'customer']
        if l_cus not in l_customers.keys():
            #l_customers.append({'customer': l_customer, 'key': local_df.at[i_index, 'key']})
            l_customers[l_cus] = {
                'id': local_df.at[i_index, 'id'],
                'cid': ''
            }
    
    for cus in l_customers.keys():
            res['data']['items'].append({
                'customer': cus,
                'key': l_customers[cus]['id'],
                'cid': l_customers[cus]['cid']
            })
    return HttpResponse(simplejson.dumps(res), content_type='application/json')

@csrf_exempt
def nwcc_list(request):
    logger.debug('nwcc_list')
    #cus = dc('customerdb')
    nwcc_fields = [
        'ID',
        'field_customer',
        'field_status'
    ]
    db = dc('devicedp')
    df = db.read_query(
        'select {fields} from `tbl_nwcc`'.format(
            fields=','.join(
                [f'`{field}`' for field in nwcc_fields]
            )
        )
    )

    res = {
        'code': 20000,
        'data': {
            'items': [],
        },
    }
    for i_index in df.index:
        item = {}
        status = df.at[i_index, 'field_status']
        if status in ['Rejected', 'Closed']:
            continue
        for field in nwcc_fields:
            item[field] = df.at[i_index, field]
        res['data']['items'].append(item)
    
    return HttpResponse(simplejson.dumps(res), content_type='application/json')
    pass

@csrf_exempt
def device_list(request):
    res = {
        'code': 20000,
        'data': {
            'items': [],
        },
    }

    try:
        ttype = request.GET['type']
        logger.debug(f'type = {ttype}')
    except:
        return HttpResponse('Invalid Parameters', content_type='application/json')


    cus = dc('customerdb')
    sql = """
        SELECT `Product`, left(`KitCode`, 10) AS Code, `Businessline` AS Bizline 
        FROM `btm_issues_device` AS bid 
        WHERE NOT EXISTS (
            SELECT * FROM weblib_issues_phaseout AS wip 
            WHERE left(bid.KitCode, 10) = wip.KitCode
        )
        """
    if ttype == 'beacon':
        sql = f"{sql} and `Product` LIKE 'Beacon%%'"
    
    logger.debug(f'sql = {sql}')
    df = cus.read_query(sql)

    for i_index in df.index:
        res['data']['items'].append(
            {
                'Product': df.at[i_index, 'Product'],
                'Code': df.at[i_index, 'Code'],
                'Bizline': df.at[i_index, 'Bizline'],
            }
        )
        
    logger.debug('device_list.size = %s', len(res['data']['items']))

    return HttpResponse(simplejson.dumps(res), content_type='application/json')

@csrf_exempt
def country_list(request):
    sql = "select `country`,`iso` from `tbl_country` order by `iso` ASC"
    logger.debug(f'sql = {sql}')
    db = dc('devicedp')
    df = db.read_query(sql)

    res = {}
    res['code'] = 20000
    res['data'] = {}
    res['data']['items'] = []
    for i_index in df.index:
        item = {}
        item['country'] = df.at[i_index, 'country']
        item['iso'] = df.at[i_index, 'iso']
        res['data']['items'].append(item)
    
    return HttpResponse(simplejson.dumps(res), content_type='application/json')
    pass

@csrf_exempt
def hosting_list(request):
    sql = "select `field_public_cloud` as cloud,`field_region` as region from `tbl_platform`"
    logger.debug(f'sql = {sql}')
    db = dc('devicedp')
    df = db.read_query(sql)

    res = {}
    res['code'] = 20000
    res['data'] = {}
    res['data']['items'] = []
    for i_index in df.index:
        item = {}
        item['cloud'] = df.at[i_index, 'cloud']
        item['region'] = df.at[i_index, 'region']
        res['data']['items'].append(item)
    
    return HttpResponse(simplejson.dumps(res), content_type='application/json')
    pass


@csrf_exempt
def upload(request):
    res = {}
    res['code'] = 20000
    res['data'] = {}
    try:
        logger.info(f'file_upload, start: {request}')
        if request.method == 'POST' and request.FILES.get('file'):
            upload_file = request.FILES['file']
            file_name = "{}____{}".format(uuid.uuid4().hex, upload_file.name)
            save_path = os.path.join(rs.UPLOAD_ROOT, file_name)
            logger.info(f'csv_upload, save_path = {save_path}')
            with open(save_path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

        res['data']['status'] = 'File uploaded OK'
        res['data']['name'] = file_name
        logger.info(f'csv_upload, end: {res}')
    except Exception as e:
        res['code'] = 20001
        logger.info(f'upload failed: {e}')

    return HttpResponse(simplejson.dumps(res), content_type='application/json')
    pass

@csrf_exempt
def download(request):
    #logger.debug('download, request.body:', request.body.decode('utf-8'))
    try:
        name = request.GET['file']
        full_path = os.path.join(rs.UPLOAD_ROOT, name)
        logger.debug(f'download, file name: {name}, full path: {full_path}')
        if os.path.exists(full_path):
            with open(full_path, 'rb') as fh:
                content = "application/vnd.ms-excel"
                if 'pdf' in name.lower():
                    content = "application/pdf"
                res = HttpResponse(fh.read(), content_type=content)
                res['Content-Disposition'] = 'inline; filename=' + name
                return res
        else:
            raise Http404
    except Exception as e:
        raise Http404
    pass
