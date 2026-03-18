import socket
import queue

from vssproto.simulation.packet_pb2 import Environment


def vision_listener_process(vision_ip, vision_port, vision_queue):
    """
    Escuta a visão em um processo separado e coloca os dados recebidos em uma fila para processamento posterior.
    Isso evita bloqueios na thread principal e permite que a visão seja processada de forma assíncrona.
    """
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_in.bind((vision_ip, vision_port))

    print(f"Vision listener started on {vision_ip}:{vision_port}")

    while True:
        try:
            data, _ = sock_in.recvfrom(1024)

            environment_data = Environment()  # Protocolo de Profobuf
            environment_data.ParseFromString(data)  # Tradução Protobuf

            while not vision_queue.empty():  # Verifica se a Queue está vazia, se não:
                try:
                    vision_queue.get_nowait(
                        environment_data
                    )  # Remove os dados da fila e finaliza o While.
                except queue.Empty:  # Se estiver vazia, saimos do While e adicionamos os novos dados na fila.
                    break  # (Sai do While)
            vision_queue.put(environment_data)  # Adiciona os novos dados fresquinhos...

        except Exception as e:
            print(f"Error in vision listener: {e}")
            break
