import socket

def create_client():
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for i in range(10):
        message = f'Hello, server! Message {i}'
        c.sendto(message.encode(), ('127.0.0.1', 8080))  # Envia para o servidor
        
        data, addr = c.recvfrom(1024)  # Aguarda resposta
        print(f'Received ACK from {addr}: {data.decode()}')

create_client()
