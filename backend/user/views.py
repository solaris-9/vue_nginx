from django.shortcuts import render

# Create your views here.
import datetime
import simplejson
import json
import ldap
import base64
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils import analyzer_db, create_token, tbl_index, strnum

# LDAP_HOST = 'ldap://10.152.138.3:389'
LDAP_HOST = 'ldap://10.158.52.11:389' 
LDAP_BASE_DN = 'OU=Users,OU=UserAccounts,DC=nsn-intra,DC=net'

def ldap_auth(username, password):
  try:
    conn = ldap.initialize(LDAP_HOST)
    
    conn.simple_bind_s('nsn-intra\\' + username, password)    
    result = conn.search_s(LDAP_BASE_DN, ldap.SCOPE_SUBTREE, 'sAMAccountName=' + username)
    result = result[0][1]
    user_info = {
      'full_name': result['cn'][0].decode('utf-8'),
      'f_name': result['givenName'][0].decode('utf-8'),
      'l_name': result['sn'][0].decode('utf-8'),
      'mail': result['mail'][0].decode('utf-8')}
    return user_info
   
  except Exception as e:
    print('--> ldap_auth Err:', e)
    return False


@csrf_exempt
def login(request):  
  if 'HTTP_X_FORWARDED_FOR' in request.META:
    print('--> rocklog login ip:', request.META.get('HTTP_X_FORWARDED_FOR'))
  else:
    print('--> rocklog login ip:', request.META.get('REMOTE_ADDR'))
  info = json.loads(request.body.decode('utf-8'))
  username = info['username']
  password = info['password']
  ldap_user = ldap_auth(username, password)
  sLastupdate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  token, exp_time = create_token(username)
  if ldap_user:
    auth_str = username + ':' + password
    binary_str = base64.b64encode(auth_str.encode('latin_1'))
    encodedAuth = bytes.decode(binary_str,encoding='latin_1')
    sql = analyzer_db()    
    old_user = sql.search_user(key=username)    
    if old_user:
      user = sql.update_user(
        old_user['id'], ldap_user['full_name'], ldap_user['f_name'],
        ldap_user['l_name'], ldap_user['mail'], token, exp_time,sLastupdate)
    else:
      user = sql.insert_user(
        username, ldap_user['mail'], token,
        f_name = ldap_user['f_name'],
        l_name = ldap_user['l_name'],
        full_name = ldap_user['full_name'],
        roles = 'Guest',
        level = '1',
        exp_time = exp_time,
        login_time = sLastupdate)
    log1 = sql.search_log(key1=username,key2='',key3='Login',key4=sLastupdate,key5='login success') 
    if not log1:
        log2=sql.insert_log(
            username = username,
            accweb='',
            operation='login',
            accdate=sLastupdate,
            status ='login success'
            )
    sql.close()
    data = {
      'name': username,
      'token': user['token'],
      'auth': encodedAuth,
    }
    resp = {
      'code': 20000,
      'mes': 'login success',
      'data': data
    }
    return HttpResponse(json.dumps(resp), content_type='application/json')
  else:
      sql = analyzer_db() 
      log1 = sql.search_log(key1=username,key2='',key3='Login',key4=sLastupdate,key5='login failure') 
      if not log1:
          log2=sql.insert_log(
              username = username,
              accweb='',
              operation='login',
              accdate=sLastupdate,
              status ='login failure'
              )
      data = {
        'name': username        
      }
      resp = {
        'code': 30000,
        'mes': 'login failure,username or password error ',
        'data': data
      } 

      return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def info(request):
  token = request.GET.get('token', None)
  sql = analyzer_db()
  user_info = sql.search_user(key=token)
  sql.close()
  if user_info:
    data = {
      'name': user_info['username'],
      'avatar': 'http://135.251.207.221/images/avatar.gif',
      'mail': user_info['mail'],
      'roles': user_info['roles'],
      'level': user_info['level'],
      'add': user_info['add'],
      'edit': user_info['edit'],
      'delete': user_info['delete'],
      'search': user_info['search'],
      'view': user_info['view'],
      'export': user_info['export'],
      'download': user_info['download']
    }
    resp = {
      'code': 20000,
      'mes': 'get user info success',
      'data': data
    }
    return HttpResponse(json.dumps(resp), content_type='application/json')
  else:
      resp = {
          'code': 30001,
          'mes': 'token error'
      }
      return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def logout(request):
  token = request.COOKIES['vue_admin_template_token']
  sql = analyzer_db()  
  sLastupdate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  user_info = sql.search_user(key=token)
  username = user_info['username']
  log1 = sql.search_log(key1=username,key2='',key3='Logout',key4=sLastupdate,key5='logout success') 
  if not log1:
    log2=sql.insert_log(
        username = username,
        accweb='',
        operation='logout',
        accdate=sLastupdate,
        status ='logout success'
        )  
  sql.close()
  # sql.delete_user(Id=user_info['id'])
  resp = {
    'code': 20000,
    'mes': 'Logout success',
  }
  return HttpResponse(json.dumps(resp), content_type='application/json')
 

def user_manage(request):

    try:
        sUsername = request.GET['username']       
    except:
        return HttpResponse('Invalid Parameters', content_type='application/json')
    dResult = {}
    dResult['code'] = 20000
    dResult['data'] = {}
    dResult['data']['column'] = []
    dResult['data']['items'] = []
    dResult['data']['column'].append('ID')
    dResult['data']['column'].append('Username')
    dResult['data']['column'].append('Email')
    dResult['data']['column'].append('Roles')
    dResult['data']['column'].append('Level')
    dResult['data']['column'].append('FirstName')
    dResult['data']['column'].append('LastName')
    dResult['data']['column'].append('FullName')
    dResult['data']['column'].append('LastLogin') 
    
    cmd = """
        SELECT
            ID,Username, Email, Roles, Level, FirstName, LastName, FullName, LastLogin
        FROM
            auth_user
            %s
            
    """
    if sUsername == 'all':       
        sRule = ''
    else:
        sRule = "WHERE Username = '%s'" % sUsername       
        
    SQLConn = analyzer_db() 
    SQLConn.cur.execute(cmd % sRule)
    SQLResult = SQLConn.cur.fetchall()
    SQLConn.close()
        
    for row in SQLResult:        
        dItem = {}
        dItem['ID'] = row[0]        
        dItem['Username'] = row[1]
        dItem['Email'] = row[2]
        dItem['Roles'] = row[3]
        dItem['Level'] = row[4]        
        dItem['FirstName'] = row[5]
        dItem['LastName'] = row[6]
        dItem['FullName'] = row[7]
        dItem['LastLogin'] = str(row[8])
        dResult['data']['items'].append(dItem)
    
    return HttpResponse(simplejson.dumps(dResult), content_type='application/json')

def user_edit(request):
    
    try:
        sType = request.GET['type'] 
        sLastupdate = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        if sType == '1':
            sUsername = request.GET['Username']  
            sMail = request.GET['Mail'] 
            sLevel = request.GET['Level'] 
            sGrade = request.GET['Roles']            
        elif sType == '2':
            sUSID = request.GET['ID']
            sMail = request.GET['Mail']
            sLevel = request.GET['Level'] 
            sGrade = request.GET['Roles'] 
                        
    except:
        return HttpResponse('Invalid Parameters', content_type='application/json')
    
    dResult = {}
    dResult['code'] = 20000
    dResult['data'] = {}
    dResult['data']['status'] = []   
    Result ='' 
    
    # 1 add
    if sType == '1': 
        token, exp_time = create_token(sUsername)
        sql = analyzer_db()    
        old_user = sql.search_user(key=sUsername) 
        if old_user:           
            Result = 'The user is exist, do not add again.'    
        else:          
          user = sql.insert_user(
            sUsername, sMail, token,
            f_name ='',
            l_name ='',
            full_name ='',
            roles = sGrade,
            level = sLevel,
            exp_time = exp_time,
            login_time = sLastupdate)
          Result = 'successful' 
        sql.close()   
    # 2 edit
    elif sType == '2': 
        sql = analyzer_db()        
        cmd="update auth_user set  Email ='%s', Level= '%s', Roles= '%s' where ID =  '%s'" % (sMail, sLevel, sGrade, sUSID) 
        
        sql.cur.execute(cmd)
        sql.commit()
        Result = 'successful' 
        sql.close()
    
    dResult['data']['status']= Result                
    
    return HttpResponse(simplejson.dumps(dResult), content_type='application/json')

def grade_manage(request):

    try:
        sGrade = request.GET['Grade']       
    except:
        return HttpResponse('Invalid Parameters', content_type='application/json')

    
    dResult = {}
    dResult['code'] = 20000
    dResult['data'] = {}      
    dResult['data']['column'] = []
    dResult['data']['items'] = []
    dResult['data']['column'].append('Grade')
    dResult['data']['column'].append('Add')
    dResult['data']['column'].append('Edit')
    dResult['data']['column'].append('Delete')
    dResult['data']['column'].append('Search')
    dResult['data']['column'].append('View')
    dResult['data']['column'].append('Export')
    dResult['data']['column'].append('Download')
    dResult['data']['column'].append('GID') 
    
    cmd = """
        SELECT
            Grade,`Add`,Edit,`Delete`,Search,View,Export,Download,GID
        FROM
            auth_grade         
            
    """  
        
    SQLConn = analyzer_db() 
    SQLConn.cur.execute(cmd)
    SQLResult = SQLConn.cur.fetchall()
    SQLConn.close()
    
    for row in SQLResult:        
        dItem = {}
        dItem['Grade'] = row[0]        
        dItem['Add'] = row[1]
        dItem['Edit'] = row[2]
        dItem['Delete'] = row[3]
        dItem['Search'] = row[4]        
        dItem['View'] = row[5]
        dItem['Export'] = row[6]
        dItem['Download'] = row[7] 
        dItem['GID'] = row[8]        
        dResult['data']['items'].append(dItem)
    
    return HttpResponse(simplejson.dumps(dResult), content_type='application/json')

def grade_list(request):
    try:
        sType = request.GET['type']        
    except:
        return HttpResponse('Invalid Parameters', content_type='application/json')
    dResult = {}
    dResult['code'] = 20000
    dResult['data'] = {}
    dResult['data']['items'] = []
    cmd = """
          SELECT
              Grade
          FROM
              auth_grade
         ORDER BY Grade
         """
    SQLConn = analyzer_db() 
    SQLConn.cur.execute(cmd )
    SQLResult = SQLConn.cur.fetchall()
    SQLConn.close()
    gradelist =[]
    for row in SQLResult:
        gradelist.append(row[0])    
    
    for grd in gradelist:        
        dItem = {}
        dItem['Grade'] = grd
        dResult['data']['items'].append(dItem)
    return HttpResponse(simplejson.dumps(dResult), content_type='application/json')

def grade_edit(request):
    
    try:
        sType = request.GET['type']                               
        if sType == '2':
            sGDID = request.GET['ID']
        
        sGrade = request.GET['Grade']  
        sAdd = request.GET['Add'] 
        sEdit = request.GET['Edit'] 
        sDelete = request.GET['Delete'] 
        sSearch = request.GET['Search'] 
        sView = request.GET['View'] 
        sExport = request.GET['Export'] 
        sDownload = request.GET['Download']             
                        
    except:
        return HttpResponse('Invalid Parameters', content_type='application/json')
    
    
    dResult = {}
    dResult['code'] = 20000
    dResult['data'] = {}
    dResult['data']['status'] = [] 
            
                
    # 1 add
    if sType == '1':             
        SQLConn = analyzer_db()         
        sql="SELECT ID FROM auth_grade ORDER BY ID"  
        SQLConn.cur.execute(sql)
        tblname ='auth_grade'
        stN = tbl_index(tblname,SQLConn) 
        sGDID = strnum(stN)  		
        sqlt="insert into auth_grade (ID,Grade, `Add`, Edit, `Delete`, Search, View, Export, Download) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        values = (sGDID, sGrade, sAdd, sEdit, sDelete, sSearch, sView, sExport, sDownload)
        SQLConn.cur.execute(sqlt, values)        
        SQLConn.commit()          
        SQLConn.close()    
        Result = 'successful' 
        
    # 2 edit
    elif sType == '2': 
        SQLConn = analyzer_db()        
        sql="""update auth_grade set Grade= '%s',`Add`= '%s', Edit= '%s',
        `Delete`= '%s', Search= '%s',View= '%s', Export= '%s',Download= '%s'
        where ID =  '%s'""" % (sGrade, sAdd, sEdit, sDelete, sSearch, sView, sExport, sDownload, sGDID)               
        SQLConn.cur.execute(sql)
        SQLConn.commit()
        SQLConn.close()    
        Result = 'successful' 
                
    dResult['data']['status']= Result 
    return HttpResponse(simplejson.dumps(dResult), content_type='application/json')
