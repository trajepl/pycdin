# chat_client.py

import sys
import socket
import select
import importlib

DATA_LEN = 1024

def chat_client(host, port):
    # if (len(sys.argv) < 3):
    #     print('Usage : python chat_client.py hostname port')
    #     sys.exit()
    #
    # host = sys.argv[1]
    # port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try:
        s.connect((host, port))
    except Exception as e:
        print(e)
        sys.exit()

    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    flag = True
    filepath = ''
    while 1:
        socket_list = [s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server
                if flag:
                    data = sock.recv(DATA_LEN).decode() 
                    path = './module/' + data
                    filepath = data[:-3]
                    flag = False
                    fin = open(path, 'w')
                    break
        
                data = sock.recv(DATA_LEN).decode()
                fin.write(data)
                fin.close()

                i = importlib.import_module('module.'+filepath)
                ret = i.run(10)
                print(ret)
                sock.sendall(str(ret).encode())



if __name__ == "__main__":
    sys.exit(chat_client("localhost", 9090))
