import socket
import random
import time

def create_client():
    HOST = "127.0.0.1" # Endereço do servidor (localhost)
    PORT = 8080 # Porta do servidor
    BUFFER_SIZE = 1024 # Tamanho do buffer para receber dados
    TOTAL_PACKETS = 10000 # Número total de pacotes a serem enviados

    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Cria um socket UDP (socket.AF_INET, socket.SOCK_DGRAM), pois UDP não estabelece conexão prévia como TCP.
    server_addr = (HOST, PORT)

    seq_num = 0  # seq_num representa o número do pacote a ser enviado.
    cwnd = 1  # (Congestion Window) controla quantos pacotes podem ser enviados de uma vez.
    ssthresh = 16  # (Slow Start Threshold) define o limite entre crescimento exponencial e linear.
    # last_ack = 0  # armazena o último número de sequência reconhecido pelo servidor.
    pac_env_not_confirm = 0  # Contador de pacotes enviados e nao confirmados.


    while seq_num <= TOTAL_PACKETS:  # Enviar até 10000 pacotes
        if pac_env_not_confirm < cwnd:  # Envia pacotes enquanto o número de pacotes enviados e não confirmados for menor que cwnd.
            msg = f"{seq_num}|Dados_{random.randint(1000, 9999)}"  # Cria uma mensagem com o número do pacote e dados aleatórios.
            client_socket.sendto(msg.encode(), server_addr)  # Envia a mensagem para o servidor.
            pac_env_not_confirm += 1  # Incrementa o contador de pacotes enviados e não confirmados.
            print(f"Pacote {seq_num} enviado")
            seq_num += 1  # Incrementa o número do pacote a ser enviado.
            
        try:
            ack_data, _ = client_socket.recvfrom(BUFFER_SIZE) # Recebe resposta do servidor
            decoded_msg = ack_data.decode()
            print(f"Mensagem recebida do servidor: {decoded_msg}")  # Debugging
            
            parts = decoded_msg.split("|")
            if len(parts) != 3:
                print(f"Erro: Mensagem inesperada recebida: {decoded_msg}")
            else:
                ack, ack_num, rwnd = parts
                ack_num = int(ack_num)
                rwnd = int(rwnd)
                if ack == "ACK":
                    print(f"Server confirmou até {ack_num}")

                pac_env_not_confirm -= (ack_num - (seq_num - pac_env_not_confirm))+1
                
                if cwnd < ssthresh:
                    cwnd *= 2  # Se cwnd ainda for menor que ssthresh, o crescimento é exponencial (multiplica por 2).
                else:
                    cwnd += 1
                    
                cwnd = min(cwnd, rwnd)  # Limita cwnd ao tamanho da janela de recebimento.
            

        
        except socket.timeout:  # Se o tempo de espera expirar, reenvie os pacotes.
            print("Tempo de espera expirou, reenviando pacotes.")
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1
            pac_env_not_confirm = 0


create_client()