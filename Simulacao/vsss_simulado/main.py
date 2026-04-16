import time
import math
import signal
import sys
import queue
import multiprocessing

from common.math_utils import wrap_angle, euclidean_distance
from common.controller_maths import speed_control

from communication.connect_to_coppelia import connect_to_coppelia
from communication.motor_adapter import CoppeliaMotorAdapter

from config.config import _coppelia_motor_port, _coppelia_ip

from perception.vision_listener import vision_listener_process
from perception.blackboard_manager import VSSSBlackBoardManager

from planning.pd_controller import PDController


class Corobeu:
    def __init__(
        self,
        robot_id,
        vision_queue,
        motor_adapter,
        pd_controller,
        black_board,
        dt,
    ):

        self.robot_id = robot_id

        self.vision_queue = vision_queue
        self.motor_adapter = motor_adapter
        self.pd_controller = pd_controller
        self.black_board = black_board

        self.v_max = 14
        self.v_min = 0
        self.linear_velocity = 8
        self.phi = 0

        self.dt = dt
        self.last_speed_time = time.time()
        self.last_environment_data = None

        signal.signal(signal.SIGINT, self.off)
        signal.signal(signal.SIGTERM, self.off)

    def update_black_board(self) -> None:
        try:
            self.last_environment_data = self.vision_queue.get_nowait()
            self.black_board.update(self.last_environment_data)
            return

        except queue.Empty:
            pass

    def follow_ball(self):
        robot_orientation = 0.0

        while True:
            self.update_black_board()

            robot_position = self.black_board.data.robot_position
            ball_position = self.black_board.data.ball_position
            robot_orientation = self.black_board.data.robot_orientation
            if (
                robot_position is None
                or ball_position is None
                or robot_orientation is None
            ):
                continue

            robot_x, robot_y = robot_position
            ball_x, ball_y = ball_position

            desired_orientation = math.atan2((ball_y - robot_y), (ball_x - robot_x))
            desired_orientation = wrap_angle(desired_orientation)
            robot_orientation = wrap_angle(robot_orientation)

            orientation_error = wrap_angle(desired_orientation - robot_orientation)
            angular_velocity = self.pd_controller.calculate_omega(orientation_error)

            # error_distance = math.sqrt((ball_y - y)**2 + (ball_x - x)**2)
            # error_distance_global = euclidean_distance((robot_x, robot_y, ball_x, ball_y))

            current_time = time.time()
            if current_time - self.last_speed_time >= self.dt:
                vl, vr = speed_control(self.linear_velocity, angular_velocity)

                self.motor_adapter.send_velocities(vl, vr)
                self.last_speed_time = current_time

    def off(self, signum=None, frame=None):
        self.motor_adapter.stop_motors()
        sys.exit()


if __name__ == "__main__":
    # 1. Cria a Queue (fila_de_visao)
    vision_queue = multiprocessing.Queue()

    # 2. Inicia o Lister (Ouvinte)
    listner = multiprocessing.Process(
        target=vision_listener_process,
        args=(vision_queue,),  # Endereço onde o TraveSim envia os dados da visão.
    )
    listner.daemon = True  # Faz o processo fechar sozinho quando você fechar o programa
    listner.start()

    # 3. Inicia o Quadro Negro

    clientID, _, motorE, motorD, _ = connect_to_coppelia(
        _coppelia_ip, _coppelia_motor_port
    )

    black_board = VSSSBlackBoardManager()
    motor_adapter = CoppeliaMotorAdapter(clientID, motorE, motorD)
    pd_controller = PDController(3.5, 0.9, 0.5, 0.033)

    meu_robo = Corobeu(
        robot_id=0,
        vision_queue=vision_queue,  # Passamos a fila aqui!
        motor_adapter=motor_adapter,
        pd_controller=pd_controller,
        black_board=black_board,
        dt=0.033,
    )

    try:
        meu_robo.follow_ball()
    except Exception as e:
        print(f"Uma falha interrompeu o código de controle.\n Erro: {e}")
    finally:
        motor_adapter.stop_motors()
