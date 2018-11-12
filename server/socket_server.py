#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 50000        # Port to listen on (non-privileged ports are > 1023)


class Server:

    def __init__(self):
        pass

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            print("Listening...")
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        try:
                            data = conn.recv(1024)
                            print(data.decode())
                            conn.sendall(data)
                        except socket.error as erro_excepcao:
                            print("Erro na recepção de dados, o cliente esta ligado? ", erro_excepcao)
                            break


if __name__ == "__main__":
    server = Server()
    server.run()
