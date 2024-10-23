from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import io
import base64
import time
import socket

app = Flask(__name__)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = socket.gethostbyname(socket.gethostname())
    server_port = 12345

    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    client_sockets = []

    while True:
        client_socket, client_address = server_socket.accept()
        client_sockets.append(client_socket)
        print(f"Connection established with {client_address}")

        # Threading to handle multiple clients
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_sockets))
        client_thread.start()

def handle_client(client_socket, client_sockets):
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        for cs in client_sockets:
            cs.send(f"{client_socket.getpeername()}: {message}".encode())

start_server()

app.run(debug=True)
