import socket
import time

def create_client():
    HOST = "127.0.0.1" # Endereço do servidor (localhost)
    PORT = 8080 # Porta do servidor
    BUFFER_SIZE = 1024 # Tamanho do buffer para receber dados

    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Cria um socket UDP (socket.AF_INET, socket.SOCK_DGRAM), pois UDP não estabelece conexão prévia como TCP.
    server_addr = (HOST, PORT)

    seq_num = 1  # seq_num representa o número do pacote a ser enviado.
    cwnd = 1  # (Congestion Window) controla quantos pacotes podem ser enviados de uma vez.
    ssthresh = 8  # (Slow Start Threshold) define o limite entre crescimento exponencial e linear.
    last_ack = 0  # armazena o último número de sequência reconhecido pelo servidor.


    while seq_num <= 20:  # Enviar até 20 pacotes
        acks_received = 0  # Contador de ACKs recebidos
        
        for _ in range(cwnd):  # Send up to cwnd packets
            if seq_num <= 20:
                print(f"📤 Sending packet {seq_num}")
                client_socket.sendto(str(seq_num).encode(), server_addr)#O número do pacote é convertido para string, codificado (.encode()) e enviado via UDP.
                seq_num += 1

        
        while acks_received < cwnd: #Se acks_received for menor que cwnd, ainda há pacotes aguardando ACKs.
            try:
                new_cwnd = cwnd
                client_socket.settimeout(3)  # Timeout de 3 segundos. Se o cliente não receber ACKs dentro desse tempo, assume que os pacotes foram perdidos.
                ack_data, _ = client_socket.recvfrom(BUFFER_SIZE) #recvfrom(BUFFER_SIZE) recebe a resposta do servidor.
                ack_msg = ack_data.decode()
                last_ack = int(ack_msg.split()[1])#Atualiza last_ack com o número do último pacote confirmado.
                print(f"Server confirmou até {last_ack}")

                acks_received += 1
                print("acks_received: ", acks_received)
                print("cwmd: ", cwnd)

                if cwnd < ssthresh:
                    cwnd *= 2  # Se cwnd ainda for menor que ssthresh, o crescimento é exponencial (multiplica por 2).
                else:
                    cwnd += 1  # Se cwnd >= ssthresh, o crescimento é linear (soma 1).

                if acks_received == new_cwnd:
                    break



            except socket.timeout: #Se o cliente não recebe um ACK em 3 segundos, ocorre um timeout.
                print("Timeout: No response from server. Ajustando cwnd e ssthresh...")
                #Isso significa perda de pacotes, então ajustamos ssthresh e cwnd para simular TCP
                ssthresh = max(2, cwnd // 2)  # Reduz ssthresh pela metade
                cwnd = 1  # Volta para Slow Start
                seq_num = last_ack + 1  # Reenvia pacotes perdidos
                break


create_client()