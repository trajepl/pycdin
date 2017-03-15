from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db import connection
import blockchain.models as BCModels
import hashlib

from . import gengraph, route_client

def active(func):
    def wrapper(*args, **kw):
        if not args[0].session.has_key('user_id'):
            return render(args[0], 'blockchain/login.html')
        else:
            return func(*args, **kw)
    return wrapper


@active
def index(request):
    context = {
        'userid'   : request.session['user_id'],
        'root'     : request.session['is_root'],
    }
    return render(request, 'blockchain/index.html', context)


def login(request):
    if request.session.has_key('user_id'):
        return HttpResponseRedirect('/')

    if len(request.POST) <= 0:
        return HttpResponseRedirect('/')

    id_form = request.POST['userid']
    psw = request.POST['password']

    md5_encode = hashlib.md5()
    md5_encode.update(psw.encode())
    psw_form = md5_encode.hexdigest()

    users = BCModels.Auth.objects.raw("select * from blockchain_auth where id = '%s'" % id_form)

    for user in users:
        if user.password == psw_form:
            root = BCModels.Auth.objects.raw("select * from blockchain_root where id = '%s'" % id_form)    
            for su_user in root:
                request.session['is_root'] = True
            request.session['user_id'] = user.id
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("password is incorrect.")
    
    return HttpResponse("user does not exist")


@active
def logout(request):
    try:
        del request.session['user_id']
        request.session['is_root'] = False
    except:
        pass
    return HttpResponseRedirect('/')


@active
def userhandle(request):
    users_list = BCModels.Auth.objects.raw("select * from blockchain_auth")

    users = []

    for user in users_list:
        tmp={}
        tmp['id'] = user.id
        with connection.cursor() as cursor:
           cursor.execute("select * from blockchain_root where id = %s", [user.id])
           is_root = cursor.fetchall()
        # is_root = BCModels.Auth.objects.raw("select * from blockchain_root where blockchain_root.id = %s" % user.id)
        
        if len(is_root) == 0:
            tmp['root'] = False
        else:
            tmp['root'] = True
        users.append(tmp)

    content = {
        'users'    : users,
    }
    return render(request, "blockchain/userhandle.html", content)


@active
def userdelete(request):
    userid = request.GET['id']   
    with connection.cursor() as cursor:
        if userid == request.session['user_id']:
            data = {
                'status'    : 0, 
                'content'   : 'Cannot delete youself.',
            }
        else:
            cursor.execute("delete from blockchain_auth where id = %s", [userid])
            cursor.execute("commit")

            data = {
                'status'    : 1, 
                'content'   : '',
            }
    return JsonResponse(data)


@active
def useradd(request):
    userid = request.POST['id']
    psw = request.POST['password']

    md5_encode = hashlib.md5()
    md5_encode.update(psw.encode())
    password = md5_encode.hexdigest()

    with connection.cursor() as cursor:
        if userid == request.session['user_id']:
            data = {
                'status'    : 0,
                'content'   : 'User exists',
            }
        else:
            cursor.execute("insert into blockchain_auth values(%s, %s)", [userid, password])
            cursor.execute("commit")

            data = {
                'status'    : 1,
                'content'   : '',
            }
    return JsonResponse(data)

@active
def modifyauth(request):
    root = request.POST['root']
    userid = request.POST['id']

    with connection.cursor() as cursor:
        if userid == request.session['user_id']:
            data = {
                'status'    : 0,
                'content'   : "Cannot change the online user's auth.",
            }
        else:
            if root == 'true':
                cursor.execute("insert into blockchain_root values(%s)", [userid])
            elif root == 'false':
                cursor.execute("delete from blockchain_root where id = %s", [userid])
            cursor.execute('commit')

            data = {
                'status'    : 1,
            }
    return JsonResponse(data)

@active
def hostadd(request):
    host = request.POST['host']

    with connection.cursor() as cursor:
        cursor.execute("insert into blockchain_host values(%s)", [host])
        cursor.execute("commit")

        data = {
            'status'    : 1,
            'content'   : '',
        }
    return JsonResponse(data)

@active
def hostdelete(request):
    host = request.POST['host']   
    with connection.cursor() as cursor:
        cursor.execute("delete from blockchain_host where host = %s", [host])
        cursor.execute("commit")

        data = {
            'status'    : 1, 
            'content'   : '',
        }
    return JsonResponse(data)

@active
def hostmodify(request):
    origin_host = request.POST['origin_host']
    modify_host = request.POST['modify_host']

    with connection.cursor() as cursor:
        cursor.execute("select host from blockchain_host where host=%s", [modify_host])
        host_duplicate = cursor.fetchall();
        print(host_duplicate)
        if len(host_duplicate) != 0:
            data = {
                'status'    : 0,
                'content'   : 'host duplicate.',
            }
        else:
            cursor.execute("update blockchain_host set host=%s where host=%s", [modify_host, origin_host])
            cursor.execute('commit')

            data = {
                'status'    : 1,
                'content'   : '',
            }

    return JsonResponse(data)

@active   
def hostquery(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from blockchain_host")
        hosts = cursor.fetchall()

    host_list = []
    for host in hosts:
        host_list.append(host[0])

    content = {
        'hosts'    : host_list,
    }
    return render(request, "blockchain/hostquery.html", content)


def build_dir(keys, values):
    res = {}
    for i in range(len(keys)):
        key = keys[i][0] + ':' + keys[i][1]
        res[key] = values[i]
    return res

@active
def build(request):
    ROUTE_PORT = 8100
    PRE_FIX_ROUTE = '[ROUTE:]'
    PRE_FIX_PROCESS = '[PROCESS:]'

    num_node = request.POST['num_node']
    if len(num_node) == 0:
        num_node = 10
    else:
        num_node = int(num_node)
    
    
    with connection.cursor() as cursor:
        cursor.execute("select * from blockchain_host")
        hosts = cursor.fetchall()
    hosts_list = []

    for host in hosts:
        hosts_list.append(host[0])
    
    addr_list, route = gengraph.host_list(num_node, hosts_list)
    route_dir = build_dir(addr_list, route)


    for addr in addr_list:
        addr_key = addr[0] + ":" + addr[1]
        route_dir_port = {}
        route_dir_port[addr[1]] = route_dir[addr_key]
        route_client.route_client(addr[0], ROUTE_PORT, route_dir_port, PRE_FIX_ROUTE)
    
    content = {
        'num_node'    : num_node,
        'hosts'       : hosts_list,
        'addr_list'   : addr_list,
        'route'       : route,
    }
    return render(request, "blockchain/simulation.html", content)























