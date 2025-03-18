import socket
import random
import time
from graph import plot_cwnd, plot_retransmissions

def create_client():
    HOST = "127.0.0.1"
    PORT = 8080
    BUFFER_SIZE = 1024
    TOTAL_PACKETS = 10000
    TIMEOUT = 0.3  # Tempo limite para receber um ACK (em segundos)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (HOST, PORT)
    client_socket.settimeout(TIMEOUT)  # Define o timeout para a recepção de ACK

    seq_num = 0
    cwnd = 1
    ssthresh = 16
    pac_env_not_confirm = {}  # Dicionário para armazenar pacotes enviados e não confirmados (seq_num: data)
    next_ack_expected = 0 # Próximo número de ACK esperado
    start_time = time.time()
    cwnd_values = []
    time_values = []
    retransmit_times = []


    while seq_num <= TOTAL_PACKETS or pac_env_not_confirm:
        # Envia pacotes dentro da janela de congestionamento
        while pac_env_not_confirm and list(pac_env_not_confirm.keys())[0] < next_ack_expected:
            del pac_env_not_confirm[list(pac_env_not_confirm.keys())[0]]

        while len(pac_env_not_confirm) < cwnd and seq_num <= TOTAL_PACKETS:
            msg = f"{seq_num}|Dados_{random.randint(1000, 9999)}"
            client_socket.sendto(msg.encode(), server_addr)
            pac_env_not_confirm[seq_num] = msg.encode()
            print(f"Pacote {seq_num} enviado")
            seq_num += 1

        try:
            ack_data, _ = client_socket.recvfrom(BUFFER_SIZE)
            decoded_msg = ack_data.decode()
            print(f"Mensagem recebida do servidor: {decoded_msg}")

            parts = decoded_msg.split("|")
            if len(parts) == 3 and parts[0] == "ACK":
                ack_num = int(parts[1])
                rwnd = int(parts[2])
                print(f"Server confirmou até {ack_num}")

                # Remove pacotes confirmados da janela de não confirmados
                acked_packets = [seq for seq in list(pac_env_not_confirm.keys()) if seq <= ack_num]
                for acked_seq in acked_packets:
                    del pac_env_not_confirm[acked_seq]
                    if acked_seq >= next_ack_expected:
                        next_ack_expected = acked_seq + 1

                if cwnd < ssthresh:
                    cwnd += len(acked_packets) # Incrementa cwnd pelo número de ACKs recebidos (Slow Start)
                else:
                    cwnd += 1 # Incrementa cwnd linearmente (Congestion Avoidance)

                cwnd = min(cwnd, rwnd)

                print(f"Janela de congestionamento: {cwnd}, ssthresh: {ssthresh}")
                cwnd_values.append(cwnd)
                time_values.append(time.time() - start_time)


        except socket.timeout:
            print("Tempo de espera expirou, reenviando pacotes não confirmados.")
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1
            # Reenvia todos os pacotes não confirmados
            for seq, data in pac_env_not_confirm.items():
                print(f"Reenviando pacote {seq}")
                client_socket.sendto(data, server_addr)
            cwnd_values.append(cwnd)
            retransmit_times.append(time.time() - start_time)
            time_values.append(time.time() - start_time)



        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break

    print("Todos os pacotes foram enviados (ou tentativas de envio realizadas).")


    
    print('tamanho time values:',len(time_values), 'tamanho cwndvalues:', len(cwnd_values))
    plot_cwnd(cwnd_values, time_values)  # Tamanho da Janela de Congestionamento vs. Tempo
    plot_retransmissions(retransmit_times)  # Tempo de Retransmissão vs. Número de Pacotes Enviados

    
    client_socket.close()

def create_client_sem_controle():
    HOST = "127.0.0.1"
    PORT = 8080
    BUFFER_SIZE = 1024
    TOTAL_PACKETS = 10000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (HOST, PORT)

    seq_num = 0

    while seq_num <= TOTAL_PACKETS:
        msg = f"{seq_num}|Dados_{random.randint(1000, 9999)}"
        client_socket.sendto(msg.encode(), server_addr)
        print(f"Pacote {seq_num} enviado")
        seq_num += 1

    # Envia uma mensagem de término de envio
    time.sleep(5)
    end_msg = "-1|Todos os pacotes foram enviados"
    client_socket.sendto(end_msg.encode(), server_addr)
    print("Mensagem de término de envio enviada.")

    print("Todos os pacotes foram enviados.")
    client_socket.close()

create_client()