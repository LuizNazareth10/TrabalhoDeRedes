import socket
import time
import random


def create_server():
    # Server settings
    HOST = "127.0.0.1"
    PORT = 8080
    BUFFER_SIZE = 1024
    WIN_SIZE = 3  # Fixed reception window size
    LOSS_PROB = 0.10  # Packet loss probability

    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print(f"Server running on {HOST}:{PORT}, Window Size = {WIN_SIZE}")

    received_packets = {}  # Stores received packets
    expected_seq = 0  # Expected sequence number

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        seq_num = int(data.decode())  # Convert received packet number


        if random.random() < LOSS_PROB:
            print(f"Pacote {seq_num} não chegou no server!")
            # Ignora o pacote e não envia ACK

        # Simulate packet processing delay

        else:
            time.sleep(0.1) #simular tempo de processamento de pacote
            print("seq_num:", seq_num)
            print('expected_seq:', expected_seq)

            if seq_num == expected_seq:
                print(f"Packet {seq_num} received correctly.")
                received_packets[seq_num] = True
                expected_seq += 1
            else:
                print(f"Packet {seq_num} out of order. Expected {expected_seq}")

            # Send ACK for the last correctly received sequence number
            print(f"📥 Sending ACK {expected_seq-1}")
            ack_msg = f"ACK {expected_seq-1}"
            server_socket.sendto(ack_msg.encode(), addr)
            

create_server()
