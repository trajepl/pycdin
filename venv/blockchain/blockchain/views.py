from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db import connection
import blockchain.models as BCModels
import hashlib
import json
import time

from . import gengraph, route_client, chain, block

def active(func):
    def wrapper(*args, **kw):
        if not args[0].session.has_key('user_id'):
            return render(args[0], 'blockchain/login.html')
        else:
            return func(*args, **kw)
    return wrapper


@active
def index(request):
    with connection.cursor() as cursor:
        cursor.execute("select user, host, port from blockchain_node where user=%s", [request.session['user_id']])
        addrs_list = cursor.fetchall()
        count_node = len(addrs_list)
    
    request.session['is_built'] = False if count_node == 0 else True
    
    context = {
        'userid'   : request.session['user_id'],
        'root'     : request.session['is_root'],
        'is_built' : request.session['is_built'],
        'addrs'    : addrs_list,
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

def insert_into_node(request, addr_list, route):
    user = request.session['user_id']
    with connection.cursor() as cursor:
        for addr in addr_list:
            host = addr[0]
            port = addr[1]
            key = host + ':' + port
            cursor.execute("insert into blockchain_node values(%s, %s, %s, %s)", [user, host, int(port), route[key]])
        cursor.execute('commit')


@active
def build(request): 
    with connection.cursor() as cursor:
        cursor.execute("select * from blockchain_host")
        hosts_list_tmp = list(cursor.fetchall())

        hosts_list = list()
        for host in hosts_list_tmp:
            hosts_list.append(host[0])
        
        cursor.execute("select count(*) from blockchain_node where user = %s", [request.session['user_id']])
        count_node = cursor.fetchone()[0]

    if count_node == 0:

        ROUTE_PORT = 8100
        PRE_FIX_ROUTE = '[ROUTE]'
        PRE_FIX_PROCESS = '[PROCESS]'

        num_node = request.POST['num_node']
        if len(num_node) == 0:
            num_node = 10
        else:
            num_node = int(num_node)
    
        addr_list, route = gengraph.host_list(num_node, hosts_list)

        route_dir = build_dir(addr_list, route)
        insert_into_node(request, addr_list, route_dir)
        print('@var views addr_list %s' % addr_list)
        print('@var views route_dir %s' % route_dir)

        for addr in addr_list:
            addr_key = addr[0] + ":" + addr[1]
            route_dir_port = {}
            route_dir_port[addr[1]] = route_dir[addr_key]
            route_client.route_client(addr[0], ROUTE_PORT, PRE_FIX_ROUTE, route_dir_port)
            route_client.route_client(addr[0], ROUTE_PORT, PRE_FIX_PROCESS, addr[1], addr_list)

    else:
        with connection.cursor() as cursor:
            cursor.execute("select host, port from blockchain_node where user=%s",[request.session['user_id']])
            addr_list = list(cursor.fetchall())
        
    content = {
        'hosts'       : hosts_list,
        'addr_list'   : addr_list,
        # 'route'       : route,
    }
    return render(request, "blockchain/simulation.html", content)

@active
def netdelete(request):
    if request.session['user_id'] != None:
        with connection.cursor() as cursor:
            cursor.execute("delete from blockchain_node where user=%s",[request.session['user_id']])
            cursor.execute("commit")
    return JsonResponse({})

def class_to_dict(obj):
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            #把Object对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
    return dict

def format_blockchain(blockchain_tmp, hash_dict, id_tmp = 0):
    nodes = []
    links = []
    for item in blockchain_tmp:
        t = time.gmtime(int(item['timestamp']))
        item['timestamp'] = time.asctime(t)
        item_tmp = {}
        item_tmp['name'] = id_tmp
        item_tmp['value'] = item
        item_tmp['draggable'] = True
        item_tmp['symbolSize'] = 40
        item_tmp['category'] = 0
        item_tmp['x'] = None
        item_tmp['y'] = None

        if id_tmp == 0: 
            id_tmp += 1
            continue
        link_tmp = {}
        link_tmp['id'] = id_tmp
        link_tmp['source'] = hash_dict[item['prev_hash']]
        link_tmp['target'] = hash_dict[item['merkle_root']]
        id_tmp += 1
        nodes.append(item_tmp)
        links.append(link_tmp)
    return nodes, links

def format_route_table(route_table):
    nodes = []
    links = []
    id_tmp = 0
    for item in route_table:
        item_tmp = {}
        item_tmp['name'] = item[0] + ' ' + str(item[1])
        item_tmp['value'] = item_tmp['name']
        item_tmp['draggable'] = True
        item_tmp['symbolSize'] = 40
        item_tmp['category'] = 0
        item_tmp['x'] = None
        item_tmp['y'] = None

        target_list = item[2].split('|')[:-1]
        for target in target_list:
            link_tmp = {}
            link_tmp['id'] = id_tmp
            link_tmp['source'] = item_tmp['name']
            link_tmp['target'] = target
            id_tmp += 1
            links.append(link_tmp)
        nodes.append(item_tmp)
    return nodes, links

@active
def show(request):
    # get route table
    with connection.cursor() as cursor:
        cursor.execute("select host, port, target from blockchain_node where user=%s",[request.session['user_id']])
        route_table = cursor.fetchall()
    route_nodes, route_links = format_route_table(route_table)

    # return all of the current block info
    port = 9999 # to do
    bc_ins = chain.Chain(port)
    bc_ins.read_chain()
    last_index = bc_ins.last_index(0)

    # bytes cannot be json serialize
    hash_dict = {}
    id_tmp = 0
    for i in range(len(bc_ins.blockchain)):
        bc_ins.blockchain[i].merkle_root = bc_ins.blockchain[i].merkle_root.decode()
        bc_ins.blockchain[i].prev_hash = bc_ins.blockchain[i].prev_hash.decode()
        hash_dict[bc_ins.blockchain[i].merkle_root] = id_tmp
        id_tmp += 1
    blockchain_tmp = class_to_dict(bc_ins.blockchain)

    nodes, links = format_blockchain(blockchain_tmp, hash_dict)
    data = {
        'nodes'       : nodes,
        'links'       : links,
        'route_nodes' : route_nodes,
        'route_links' : route_links,
        'route_nodes_x' : route_nodes,
        'route_links_x' : route_links,
        'last_id'     : last_index[0],
        'offset'      : last_index[1]
    }
    return JsonResponse(data)
      
@active
def new_block(request):
    # accept new block
    # return new block to front-end
    last_id = request.GET['last_id']
    offset = request.GET['offset']
    last_index = [int(last_id), int(offset)]
    
    port = 9999 # to do
    ret_list = []
    index = []
    tmp_chain = chain.Chain(port)
    last_index_cur = tmp_chain.last_index(0)
    index.append(last_index_cur)
    
    id = 1
    while last_index_cur[0] != last_index[0]:
        last_index_cur = tmp_chain.last_index(id)
        index.append(last_index_cur)
        id += 1
    last_index_cur = tmp_chain.last_index(id)
    index.append(last_index_cur)
    
    print(index)
    hash_dict = {}
    for item in index[1:]:
        block = tmp_chain.read_chain_index(item)
        block.merkle_root = block.merkle_root.decode()
        block.prev_hash = block.prev_hash.decode()
        ret_list.append(block)
        hash_dict[block.merkle_root] = item[0]
    
    if len(ret_list) >= 1:
        blockchain_tmp = class_to_dict(ret_list[:-1])
        nodes, links = format_blockchain(blockchain_tmp, hash_dict, int(last_id))
        print(nodes)
        data = {
            'nodes'    : nodes, 
            'links'    : links,
            'last_id'  : index[0][0],
            'offset'  : index[0][1],
        }
    else:
        data = {
            'nodes'    : [], 
            'links'    : [],
        }
    return JsonResponse(data)  

@active
def new_route_info(request):
    node_x = [] 
    node_y = []
    with open('blockchain/bcinfo/9999/x', 'r') as x_out:
        tmp = x_out.readline()
        if len(tmp) > 0:
            node_x.append(tmp)
    with open('blockchain/bcinfo/9999/y', 'r') as y_out:
        tmp = y_out.readline()
        if len(tmp) > 0: 
            node_y.append(tmp)
    with open('blockchain/bcinfo/9999/x', 'w') as tmp: pass
    with open('blockchain/bcinfo/9999/y', 'w') as tmp: pass
    
    data = {
        'node_x'    : node_x,
        'node_y'    : node_y,
    }
    return JsonResponse(data)

@active
def visual(request):
    return render(request, 'blockchain/visual.html')
