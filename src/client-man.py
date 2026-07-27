import argparse
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
    args = parser.parse_args()
    server_ip, server_port, identity, psk, server_id = load_server(args.server)
    peer_ip, peer_port, peer_server = load_peer(args.peer)
    choose = input("Do you want to generate NEW or GET an existing key? (n/g): ").strip().lower()
    if choose == "n":
        key_id, key = request_key(server_ip, peer_server, server_id, server_port, identity, psk)
        print(f"KeyId: {key_id}, Key: {key}")
    elif choose == "g":
        key_id = input("Enter Key ID: ").strip()
        key = fetch_key_by_id(server_ip, key_id, server_id, server_port, identity, psk, peer_server)
        print(f"KeyId: {key_id}, Key: {key}")
    else:
        print("Invalid choice. Use 'n' to generate a new key or 'g' to get an existing key.")
    
    return 



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nEnd...")
        sys.exit(0)
