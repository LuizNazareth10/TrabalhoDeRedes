import socket
import time
import random
from graph import plot_vazão, plot_packet_loss

def create_server():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 8080
    BUFFER_SIZE = 1024
    LOSS_PROB = 0.000
    receive_times = {}
    start_time = time.time()
    loss_times = []
    RWND = 50


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print(f"Server running on {SERVER_IP}:{SERVER_PORT}, Receiver Window Size = {RWND}, Loss Probability = {LOSS_PROB}")

    received_packets = {}
    expected_seq = 0

    while True:
        try:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            seq_num_str, msg = data.decode().split("|", 1)
            recv_time = time.time() - start_time
            seq_num = int(seq_num_str)
            print(f"Pacote recebido {seq_num} de {addr}")

            if random.random() < LOSS_PROB:
                print(f"Pacote {seq_num} descartado (simulação de perda).")
                loss_times.append(recv_time)
                continue

            received_packets[seq_num] = msg
            receive_times[seq_num] = recv_time

            # Entrega ordenada
            while expected_seq in received_packets:
                print(f"Entregando pacote {expected_seq} à aplicação.")
                del received_packets[expected_seq]
                expected_seq += 1

            # Envia ACK acumulativo
            ack_num = expected_seq - 1
            ack_msg = f"ACK|{ack_num}|{RWND}"
            server_socket.sendto(ack_msg.encode(), addr)
            print(f"Enviando ACK {ack_num} para {addr}")

        except Exception as e:
            print(f"Erro no servidor: {e}")
            break

        if expected_seq == 10001:
            plot_vazão(receive_times)  # Vazão vs. Tempo
            plot_packet_loss(loss_times)    # Número de Pacotes Perdidos vs. Tempo






def create_server_sem_controle():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 8080
    BUFFER_SIZE = 1024
    LOSS_PROB = 0.001
    receive_times = {}
    start_time = time.time()
    loss_times = []
    RWND = 50

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print(f"Server running on {SERVER_IP}:{SERVER_PORT}, Receiver Window Size = {RWND}, Loss Probability = {LOSS_PROB}")

    received_packets = {}
    expected_seq = 0
    lost_packets = []

    while True:
        try:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            seq_num_str, msg = data.decode().split("|", 1)
            recv_time = time.time() - start_time
            seq_num = int(seq_num_str)
            print(f"Pacote recebido {seq_num} de {addr}")

            if random.random() < LOSS_PROB:
                print(f"Pacote {seq_num} descartado (simulação de perda).")
                loss_times.append(recv_time)
                lost_packets.append(seq_num)
                continue

            received_packets[seq_num] = msg
            receive_times[seq_num] = recv_time
                
            # Entrega ordenada
            while expected_seq in received_packets:
                print(f"Entregando pacote {expected_seq} à aplicação.")
                del received_packets[expected_seq]
                expected_seq += 1

        except Exception as e:
            print(f"Erro no servidor: {e}")
            break

        if seq_num == 10000:
            plot_vazão(receive_times)  # Vazão vs. Tempo
            plot_packet_loss(loss_times)    # Número de Pacotes Perdidos vs. Tempo
            print(f"Pacotes perdidos: {lost_packets}")

create_server_sem_controle()


