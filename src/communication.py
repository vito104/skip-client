import os
from networking import socket_create
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import socket


def encrypt_message(key, plaintext):
    aes = AESGCM(key)

    nonce = os.urandom(12)

    ciphertext = aes.encrypt(nonce, plaintext.encode("utf-8"), None)

    return nonce + ciphertext


def decrypt_message(key, data):
    aes = AESGCM(key)

    nonce = data[:12]
    ciphertext = data[12:]

    plaintext = aes.decrypt(nonce, ciphertext, None)

    return plaintext.decode("utf-8")




def send_message(host, port, key, message):
    encrypted = encrypt_message(key, message)
    sock = socket_create(host, port, autoconnect=True)
    try:
        sock.sendall(encrypted)
    finally:
        sock.close()


def receive_message(port, key):
    server_sock = socket_create()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", port))
    server_sock.listen(1)
    conn, addr = server_sock.accept()
    chunks = []
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    conn.close()
    server_sock.close()
    data = b"".join(chunks)
    return decrypt_message(key, data)


