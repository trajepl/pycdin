# chat_server.py

import sys
import socket
import select

HOST = ''
SOCKET_LIST = []
SOCKET_NUM = 10
RECV_BUFFER = 4096
PORT = 9090


def chat_server():
    # AF_INET -> IPV4(MOST OF THE INTERNET) | SOCK_STREAM -> TCP SOCK_DGRAM -> UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(SOCKET_NUM)

    # add server socket object on to list of readable connections
    SOCKET_LIST.append(server_socket)

    print("Chat server started on port " + str(PORT))

    while 1:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out = 0 : poll and never block
        ready_to_read, read_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            # a new connection request received
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("> Client (%s, %s) connected" % addr)
                module_name = input('> (select module inject) ')
                module_inject(server_socket, sockfd, module_name)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    data = data.decode()
                    print('> result is: ' + data)
                    if data:
                        print('> [' + sock.getpeername() + ']:' + data)
                except:
                    pass

    server_socket.close()


# module_inject chat messages to all connected clients
def module_inject(server_socket, sock, module_name):
    # send module_name first
    module_name = module_name + '.py'
    sock.sendall(module_name.encode())

    path = '../module/' + module_name
    with open(path, 'r') as fout:
        tmp = ''
        for line in fout.readlines():
            tmp += line
        try:
            sock.sendall(tmp.encode())
        except:
            sock.close()
            if sock in SOCKET_LIST:
                SOCKET_LIST.remove(sock)


if __name__ == "__main__":
    sys.exit(chat_server())

# :%s/goo/fd/gc  replace goo with fc. c:ask confirmation first
