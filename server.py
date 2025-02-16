import socket

def create_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    s.bind(("127.0.0.1", 8080))  # Vincula à porta 8080
    print("Server is running on port 8080")

    while True:
        try:
            data, addr = s.recvfrom(1024)  # Aguarda dados do cliente
            print(f"Received from {addr}: {data.decode()}")

            s.sendto(b"ACK", addr)  # Envia resposta ao cliente
        except Exception as e:
            print(f"Error: {e}")

create_server()
