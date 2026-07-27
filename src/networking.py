from sslpsk3 import *
import ssl
import socket
import json



import ssl
from sslpsk3 import SSLPSKContext

def create_tls(sock, identity, psk, ca_file, cert_file, key_file):
    if sock is None:
        print("Socket error")
        exit(1)

    # 1. ROZHODNUTÍ: Použijeme PSK, pokud máme identitu a klíč a NEMÁME certifikáty
    if identity and psk and not (ca_file or cert_file):
        def callback(hint):
            id_str = identity.decode() if isinstance(identity, bytes) else identity
            return id_str, psk

        context = SSLPSKContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        context.set_ciphers("PSK")
        context.set_psk_client_callback(callback)

    else:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        
        if ca_file:
            context.check_hostname = False  
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(cafile=ca_file)
        else:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        if cert_file and key_file:
            context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    tls_socket = context.wrap_socket(sock)
    return tls_socket


def socket_create(host=None, port=None, autoconnect=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if autoconnect:
        try:
            sock.connect((host, port))
            #print("Connected")
        except Exception as e:
            print(e)
            return None
    return sock


def send_key_id(host, port, key_id, my_server_id):
    payload = json.dumps({
        "key_id": key_id,
        "remote_server_id": my_server_id
    })
    sock = socket_create(host, port, autoconnect=True)
    try:
        sock.sendall(payload.encode())
    finally:
        sock.close()



def listen_for_data(host='0.0.0.0', port=5000, timeout=None):
    server_sock = socket_create()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(1)
    if timeout is not None:
        server_sock.settimeout(timeout)
    conn_sock, addr = server_sock.accept()
    chunks = []
    while True:
        chunk = conn_sock.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    data = b"".join(chunks)
    conn_sock.close()
    server_sock.close()
    payload = json.loads(data.decode('utf-8'))
    return payload["key_id"], payload["remote_server_id"], addr
