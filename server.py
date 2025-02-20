import socket
import time
import random


def create_server():
    # Server settings
    HOST = "127.0.0.1" #Endereço do servidor (localhost)
    PORT = 8080 #Porta do servidor
    BUFFER_SIZE = 1024 #Tamanho do buffer para receber dados
    WIN_SIZE = 3  # Tamanho da janela deslizante REVISAR A NECESSIDADE DESSE CARA
    LOSS_PROB = 0.1 # Probabilidade de perda de pacotes(10%)

    # Create UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Cria um socket UDP (socket.AF_INET, socket.SOCK_DGRAM), pois UDP não estabelece conexão prévia como TCP.
    server_socket.bind((HOST, PORT)) #Associa o socket ao endereço e porta do servidor.

    print(f"Server running on {HOST}:{PORT}, Window Size = {WIN_SIZE}")

    received_packets = {}  #  Um dicionário que armazena pacotes recebidos
    expected_seq = 1  # Controla qual número de sequência o servidor espera receber.

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE) # Espera receber um pacote
        seq_num = int(data.decode())  # Converte o número do pacote recebido
        #O servidor fica rodando indefinidamente, esperando pacotes.
        # recvfrom(BUFFER_SIZE) → Aguarda receber dados do cliente e retorna:
        # data → O conteúdo recebido (número do pacote).
        # addr → O endereço e a porta do cliente que enviou o pacote.

        if random.random() < LOSS_PROB:
            print(f"Pacote {seq_num} não chegou no server!")
            #random.random() gera um número aleatório entre 0 e 1.
            # Se esse número for menor que LOSS_PROB (0.1), significa que o pacote foi "perdido".
            # O servidor simula essa perda ignorando o pacote e não enviando ACK.

        else:
            time.sleep(0.1) #simular tempo de processamento de pacote


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
