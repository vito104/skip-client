import json


def load_config(path):
    with open(path) as f:
        return json.load(f)


def load_psk(file):
    with open(file) as f:
        result = f.read()
    identity, psk = result.split(":", 1)
    return identity.encode(), bytes.fromhex(psk)


def load_peer(peer):
    peer_config = load_config(peer)
    peer_ip = peer_config["host"]
    peer_port = peer_config["port"]
    peer_server = peer_config["remote_server_id"]
    return peer_ip, peer_port, peer_server

def load_server(server):
    server_config = load_config(server)
    server_ip = server_config["host"]
    server_port = server_config["port"]
    auth_type = server_config["auth_type"]
    server_id = server_config["server_id"]
    
    ca_file = None
    cert_file = None
    key_file = None
    psk = None
    identity = None

    if auth_type == "cert":
        ca_file = server_config.get("ca-file")
        cert_file = server_config.get("cert-file")
        key_file = server_config.get("key-file")
    elif auth_type == "psk":
        psk_file = server_config["psk-file"]
        identity, psk = load_psk(psk_file)
    else:
        print(f"Unknown auth type: {auth_type}")
        exit(1)
        
    return server_ip, server_port, server_id, identity, psk, ca_file, cert_file, key_file