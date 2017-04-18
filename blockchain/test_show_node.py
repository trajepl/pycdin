import socket
import hashlib

def check(check_code, sock, data):
    """
    : check information which server receives
    """
    origin_data = data
    hash_code = hashlib.sha256(origin_data.encode()).hexdigest().encode()

    return True if hash_code == check_code else False


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(15)

client_socket.connect(('127.0.0.1', 9999))
data = '[BLOCK]|IP 0000|123|123|prev_hash|merkle_root|random|length|data1$data2'
client_socket.send(data.encode())

try:
    check_code = client_socket.recv(1024)
    if check(check_code, client_socket, data):
        client_socket.send(b'success')
except Exception as e:
    print(e)
finally:
    client_socket.close()