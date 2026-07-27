import json
import sys
from networking import create_tls, socket_create


def request(tls_sock, method, path, server_id, remote_server_id=None):
    if remote_server_id:
        path = f"{path}?remoteSystemID={remote_server_id}"
    else:
        print("No remote server id provided!")
        exit(1)
    req = f"{method} {path} HTTP/1.1\r\nHost: {server_id}\r\nConnection: close\r\n\r\n"
    tls_sock.send(req.encode())
    response = b""
    while True:
        resp = tls_sock.recv(4096)
        if not resp:
            break
        response += resp
    return response.decode(errors="replace")


def request_key(server_ip, peer_server, server_id, port, identity, psk, ca_file, cert_file, key_file):
    tls_sock = create_tls(socket_create(server_ip, port, True), identity, psk, ca_file, cert_file, key_file)
    resp = request(tls_sock, "GET", "/key", server_id, remote_server_id=peer_server)
    header, body = resp.split("\r\n\r\n", 1)
    
    print(body)
    start = body.find('{')
    end = body.rfind('}') + 1
    if start != -1 and end != 0:
        clean_json = body[start:end]
        data = json.loads(clean_json)
    else:
        raise ValueError(f"Nepodařilo se najít platný JSON v těle odpovědi: {body}")

    key_id = data["keyId"]
    key = bytes.fromhex(data["key"])
    return key_id, key


def fetch_key_by_id(server_ip, peer_server, server_id, port, identity, psk, ca_file, cert_file, key_file, key_id, remote_server_id):
    tls_sock = create_tls(socket_create(server_ip, port, True), identity, psk, ca_file, cert_file, key_file)
    resp = request(tls_sock, "GET", f"/key/{key_id}", server_id, remote_server_id=remote_server_id)
    header, body = resp.split("\r\n\r\n", 1)
    
    start = body.find('{')
    end = body.rfind('}') + 1
    if start != -1 and end != 0:
        clean_json = body[start:end]
        data = json.loads(clean_json)
        print("DEBUG SERVER RESPONSE:", data)
    else:
        raise ValueError(f"Nepodařilo se najít platný JSON v těle odpovědi: {body}")

    # Pokud server klíč nevrátil, vypíšeme chybu a ukončíme program
    if "key" not in data:
        print(f"\n[!] CHYBA: Server nevratio klíč! Odpověď serveru: {data}")
        sys.exit(1)

    key = bytes.fromhex(data["key"])
    print(f"Key: {key}")
    return key