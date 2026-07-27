from html import parser
import json
import argparse
from urllib import response
from networking import *
from config import load_server, load_peer
from skip import request_key, fetch_key_by_id
from communication import *
import sys


def main():
    print("To end this app press CTRL + C")
    parser = argparse.ArgumentParser(description="SKIP client")
    parser.add_argument("--server", help="Path to server config", required=True)
    parser.add_argument("--peer", help="Path to peer config", default=None)
    parser.add_argument("--com", nargs='*', default=None, help="Communication flag or message")
    
    args = parser.parse_args()
    server_ip, server_port, server_id, identity, psk, ca_file, cert_file, key_file = load_server(args.server)
    if args.peer:
        peer_ip, peer_port, peer_server = load_peer(args.peer)
        print("Master mode")
        key_id, key = request_key(server_ip, peer_server, server_id, server_port, identity, psk, ca_file, cert_file, key_file)
        print("Calling neighbour to send key id...")
        send_key_id(peer_ip, peer_port, key_id, server_id)
        if args.com is not None:
                msg = receive_message(5001, key)
                if msg == "Ping":
                    print("Ping")
                    send_message(peer_ip, 5001, key, f"Pong")



    else:
        print("Slave mode")
        key_id, remote_server_id, addr = listen_for_data(host='0.0.0.0', port=5000)
# OPRAVENÉ VOLÁNÍ:
        key = fetch_key_by_id(
            server_ip,            # server_ip
            remote_server_id,     # peer_server (použijeme remote_server_id)
            server_id,            # server_id (načteno z load_server)
            server_port,          # port
            identity,             # identity
            psk,                  # psk
            ca_file,              # ca_file
            cert_file,            # cert_file
            key_file,             # key_file
            key_id,               # key_id (přijatý ze sítě)
            remote_server_id      # remote_server_id
        )        
        if args.com is not None:
            print(" <- Ping")
            send_message(addr[0], 5001, key, "Ping")
            response = receive_message(5001, key)
            print(f" -> {response}")



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nEnd...")
        sys.exit(0)
