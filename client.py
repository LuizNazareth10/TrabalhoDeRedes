import socket
import time

def create_server():
    # Client settings
    HOST = "127.0.0.1"
    PORT = 8080
    BUFFER_SIZE = 1024

    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (HOST, PORT)

    seq_num = 1  # Initial sequence number
    cwnd = 1  # Congestion Window inicial
    ssthresh = 8  # Slow Start Threshold inicial
    last_ack = 0  # Last ACK received
    


    while seq_num <= 20:  # Send 20 packets as an example
        acks_received = 0  # Number of ACKs received
        
        for _ in range(cwnd):  # Send up to cwnd packets
            if seq_num <= 20:
                print(f"📤 Sending packet {seq_num}")
                client_socket.sendto(str(seq_num).encode(), server_addr)
                seq_num += 1

        # Wait for ACKs
        
        while acks_received < cwnd:
            try:
                new_cwnd = cwnd
                client_socket.settimeout(3)  # Timeout de 3 segundos
                ack_data, _ = client_socket.recvfrom(BUFFER_SIZE)
                ack_msg = ack_data.decode()
                last_ack = int(ack_msg.split()[1])
                print(f"Server confirmou até {last_ack}")

                acks_received += 1
                print("acks_received: ", acks_received)
                print("cwmd: ", cwnd)

                if cwnd < ssthresh:
                    cwnd *= 2  # Crescimento exponencial
                else:
                    cwnd += 1  # Crescimento linear

                if acks_received == new_cwnd:
                    break



            except socket.timeout:
                print("Timeout: No response from server. Ajustando cwnd e ssthresh...")
                ssthresh = max(2, cwnd // 2)  # Reduz ssthresh pela metade
                cwnd = 1  # Volta para Slow Start
                seq_num = last_ack + 1  # Reenvia pacotes perdidos
                break


create_server()