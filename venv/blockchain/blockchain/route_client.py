import socket
import sys
import json

PRE_FIX_ROUTE = "[ROUTE]"
PRE_FIX_PROCESS = "[PROCESS]"

def route_client(host, port, pre_fix, data_dir, host_list=''):
    route_clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    route_clt.settimeout(2)

    try:
        route_clt.connect((host, port))
    except Exception as e:
        print(e)
        sys.exit()

    while True:
        data = pre_fix
        if pre_fix == PRE_FIX_ROUTE:
            data += json.dumps(data_dir)
        elif pre_fix == PRE_FIX_PROCESS:
            host_list_str = ''
            for item in host_list:
                host_list_str += item + '#'
            data += host + '|' +str(data_dir) + '|' + host_list_str

        if not data:
            break
        print("24: route_client data: %s" %data)           
        route_clt.send(data.encode())
        data_recv = route_clt.recv(1024).decode()
        if data_recv == 'success':
            break
            
    route_clt.close()