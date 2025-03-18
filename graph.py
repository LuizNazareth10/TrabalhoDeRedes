import matplotlib.pyplot as plt
import numpy as np

def plot_packet_loss(loss_times):
    """
    Plota o número de pacotes perdidos ao longo do tempo.
    
    :param loss_times: Lista com os tempos em que pacotes foram perdidos.
    """
    if not loss_times:
        print("Nenhum pacote perdido.")
        return
    
    plt.figure(figsize=(10, 5))
    plt.hist(loss_times, bins=30, alpha=0.7, color='red')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Número de Pacotes Perdidos")
    plt.title("Pacotes Perdidos vs. Tempo")
    plt.grid()
    plt.show()

def plot_cwnd(cwnd_values, time_values):
    """
    Plota a evolução do tamanho da janela de congestionamento (cwnd).
    
    :param cwnd_values: Lista com valores da janela de congestionamento ao longo do tempo.
    :param time_values: Lista de tempos correspondentes.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(time_values, cwnd_values, marker="o", linestyle="-", label="cwnd")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Tamanho da Janela de Congestionamento")
    plt.title("Evolução da Janela de Congestionamento (cwnd) vs. Tempo")
    plt.legend()
    plt.grid()
    plt.show()


def plot_latency_vs_loss(loss_rates, avg_latencies):
    """
    Plota a latência média conforme a taxa de perda aumenta.
    
    :param loss_rates: Lista de taxas de perda simuladas.
    :param avg_latencies: Lista de latências médias correspondentes.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(loss_rates, avg_latencies, marker="o", linestyle="-", color="purple")
    plt.xlabel("Taxa de Perda (%)")
    plt.ylabel("Latência Média (s)")
    plt.title("Latência Média vs. Taxa de Perda")
    plt.grid()
    plt.show()



def plot_retransmissions(retransmit_times):
    """
    Plota a quantidade de retransmissões ao longo do tempo.
    
    :param retransmit_times: Lista de tempos em que retransmissões ocorreram.
    """
    if not retransmit_times:
        print("Nenhuma retransmissão registrada.")
        return
    
    plt.figure(figsize=(10, 5))
    plt.hist(retransmit_times, bins=30, alpha=0.7, color='blue')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Número de Retransmissões")
    plt.title("Retransmissões vs. Tempo")
    plt.grid()
    plt.show()


def plot_vazão(receive_times, interval=1):
    """
    Plota a vazão ao longo do tempo.
    
    receive_times: Dicionário {seq_num: tempo_de_recebimento}
    interval: Janela de tempo (segundos) para calcular a vazão.
    """
    min_time = min(receive_times.values())
    max_time = max(receive_times.values())

    time_bins = list(range(int(min_time), int(max_time) + interval, interval))
    packet_counts = [0] * len(time_bins)

    for t in receive_times.values():
        bin_index = int((t - min_time) // interval)
        packet_counts[bin_index] += 1

    plt.figure(figsize=(10, 5))
    plt.plot(time_bins, packet_counts, marker="o", linestyle="-")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Pacotes Recebidos por Segundo")
    plt.title("Vazão vs. Tempo")
    plt.grid()
    plt.show()

