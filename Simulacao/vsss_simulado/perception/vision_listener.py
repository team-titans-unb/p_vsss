import multiprocessing
import queue
import time
import math

from common.math_utils import wrap_angle
from config.config import _coppelia_ip, _coppelia_vision_port
from communication.sims import sim
from communication.connect_to_coppelia import connect_to_coppelia


def vision_listener_process(vision_queue: multiprocessing.Queue):
    """
    Escuta a visão em um processo separado e coloca os dados recebidos em uma fila para processamento posterior.
    Isso evita bloqueios na thread principal e permite que a visão seja processada de forma assíncrona.

    Args:
        vision_queue (multiprocessing.Queue): Queue (fila) onde ficarão os dados brutos enviados pelo CoppeliaSim.
    """

    clientID, robot, _, _, ball = connect_to_coppelia(
        _coppelia_ip, _coppelia_vision_port
    )

    # 1. ATUALIZAR DADOS DO MUNDOintegral_counter
    sim.simxGetObjectPosition(clientID, robot, -1, sim.simx_opmode_streaming)
    sim.simxGetObjectPosition(clientID, ball, -1, sim.simx_opmode_streaming)
    sim.simxGetObjectOrientation(clientID, robot, -1, sim.simx_opmode_streaming)

    while True:
        try:
            # Colhe os dados do CoppeliaSim rapidamente,
            status_robot, robotPos = sim.simxGetObjectPosition(
                clientID, robot, -1, sim.simx_opmode_buffer
            )
            status_ball, ballPos = sim.simxGetObjectPosition(
                clientID, ball, -1, sim.simx_opmode_buffer
            )
            status_ori, robotOri = sim.simxGetObjectOrientation(
                clientID, robot, -1, sim.simx_opmode_buffer
            )
            # print(
            #    f"DEBUG: Status robo: {status_robot} | Status bola: {status_ball} | status ori: {status_ori} | sim: {sim.simx_return_ok}"
            # )
            if (
                status_robot == sim.simx_return_ok
                and status_ball == sim.simx_return_ok
                and status_ori == sim.simx_return_ok
            ):
                dados = {
                    "robot_position": robotPos,
                    "ball_position": ballPos,
                    "robot_orientation": wrap_angle(robotOri[2] - math.pi / 2),
                }  # Transforma os dados em um dicionário.

                while (not vision_queue.empty()):  # Verifica se a Queue está vazia, se não:
                    try:
                        vision_queue.get_nowait()  # Remove os dados da fila e finaliza o While.
                    except queue.Empty:  # Se estiver vazia, saimos do While e adicionamos os novos dados na fila.
                        break  # (Sai do While)
                vision_queue.put(dados)  # Adiciona os novos dados fresquinhos...

            time.sleep(0.005)

        except Exception as e:
            print(f"Error in vision listener: {e}")
            break
