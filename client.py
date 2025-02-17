import socket
import time

def create_server():
    # Client settings
    HOST = "127.0.0.1"
    PORT = 8080
    BUFFER_SIZE = 1024
    WIN_SIZE = 3  # Fixed sending window size

    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (HOST, PORT)

    seq_num = 1  # Initial sequence number

    while seq_num <= 10:  # Send 10 packets as an example
        for _ in range(WIN_SIZE):  # Send up to WIN_SIZE packets
            if seq_num <= 10:
                print(f"📤 Sending packet {seq_num}")
                client_socket.sendto(str(seq_num).encode(), server_addr)
                seq_num += 1

        # Wait for ACKs
        acks_received = 0
        while acks_received < WIN_SIZE:
            try:
                client_socket.settimeout(1)  # Timeout for receiving ACK
                ack_data, _ = client_socket.recvfrom(BUFFER_SIZE)
                ack_msg = ack_data.decode()
                last_ack = ack_msg.split(" ")
                last_ack = last_ack[-1]  # Last confirmed packet
                print(f"Server confirmed up to {last_ack}")
                acks_received += 1
            except socket.timeout:
                print("Timeout: No response from server.")
                break

        time.sleep(0.5)  # Small delay between sends

create_server()