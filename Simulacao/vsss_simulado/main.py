import time
import math
import signal
import sys
import queue
import multiprocessing

from common.math_utils import wrap_angle
from common.controller_maths import speed_control

from communication.connect_to_coppelia import connect_to_coppelia
from communication.motor_adapter import CoppeliaMotorAdapter

from config.config import _coppelia_motor_port, _coppelia_ip

from perception.vision_adapter import vision_listener_process

from planning.pd_controller import PD_Controller


class Corobeu:
    def __init__(
        self, robot_id, COR_DO_TIME, vision_queue, motor_adapter, pd_controller, dt
    ):

        self.robot_id = robot_id

        self.vison_queue = vision_queue
        self.motor_adapter = motor_adapter
        self.pd_controller = pd_controller

        self.v_max = 14
        self.v_min = 0
        self.v_linear = 8
        self.phi = 0

        self.dt = dt
        self.last_speed_time = time.time()
        self.last_environment_data = None

        if COR_DO_TIME == 1:
            self._robot_attr = "robots_blue"
        elif COR_DO_TIME == 0:
            self._robot_attr = "robots_yellow"
        else:
            raise ValueError(
                f"COR_DO_TIME: {COR_DO_TIME} é inválido, altere-o no 'config_ideal.py'."
            )

        signal.signal(signal.SIGINT, self.off)
        signal.signal(signal.SIGTERM, self.off)

    def get_position(
        self,
    ) -> tuple[float, float, float, float, float] | tuple[None, None, None, None, None]:

        try:
            self.last_environment_data = self.vison_queue.get_nowait()
        except queue.Empty:
            pass

        if self.last_environment_data is None:
            return (None, None, None, None, None)

        dados = self.last_environment_data
        robot_x, robot_y, robot_orientation, ball_x, ball_y = (
            dados["robot_position"][0],
            dados["robot_position"][1],
            dados["robot_orientation"],
            dados["ball_position"][0],
            dados["ball_position"][1],
        )
        return (robot_x, robot_y, robot_orientation, ball_x, ball_y)

    def follow_ball(self):
        phi_obs = 0.0

        while True:
            (robot_x, robot_y, phi_obs, ball_x, ball_y) = self.get_position()

            if (
                robot_x is None
                or robot_y is None
                or phi_obs is None
                or ball_x is None
                or ball_y is None
            ):
                continue

            phid = math.atan2((ball_y - robot_y), (ball_x - robot_x))
            phid = wrap_angle(phid)
            phi_obs = wrap_angle(phi_obs)

            error_phi = wrap_angle(phid - phi_obs)
            omega = self.pd_controller.calculate_omega(error_phi)

            # error_distance = math.sqrt((ball_y - y)**2 + (ball_x - x)**2)
            # error_distance_global = math.sqrt((ball_y - y) ** 2 + (ball_x - x) ** 2)

            U = self.v_linear
            current_time = time.time()
            if current_time - self.last_speed_time >= self.dt:
                vl, vr = speed_control(U, omega)

                self.motor_adapter.send_velocities(vl, vr)
                self.last_speed_time = current_time

    def follow_path(self, path_x=0, path_y=0):
        phi_obs = 0

        while True:
            x, y, phi_obs = self.get_position()[0:3]

            if x is None or y is None or phi_obs is None:
                continue

            phid = math.atan2((path_y - y), (path_x - x))
            phid = wrap_angle(phid)
            phi_obs = wrap_angle(phi_obs)

            error_phi = wrap_angle(phid - phi_obs)
            omega = self.pd_controller.calculate_omega(error_phi)

            error_distance = math.sqrt((path_y - y) ** 2 + (path_x - x) ** 2)
            # error_distance_global = math.sqrt((path_y - y) ** 2 + (path_x - x) ** 2)

            U = self.v_linear
            current_time = time.time()

            if current_time - self.last_speed_time >= self.dt:
                vl, vr = speed_control(U, omega)

                self.motor_adapter.send_velocities(vl, vr)
                self.last_speed_time = current_time

            if error_distance <= 0.07:
                self.motor_adapter.send_velocities(0, 0)
                self.off()

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

    print("conexão com o motor abaixo: ")
    clientID, _, motorE, motorD, _ = connect_to_coppelia(
        _coppelia_ip, _coppelia_motor_port
    )

    motor_adapter = CoppeliaMotorAdapter(clientID, motorE, motorD)

    pd_controller = PD_Controller(3.5, 0.9, 0.5, 0.033)

    meu_robo = Corobeu(
        robot_id=0,
        COR_DO_TIME=0,
        vision_queue=vision_queue,  # Passamos a fila aqui!
        motor_adapter=motor_adapter,
        pd_controller=pd_controller,
        dt=0.033,
    )

    try:
        meu_robo.follow_ball()
    except Exception as e:
        print(f"Uma falha interrompeu o código de controle.\n Erro: {e}")
    finally:
        motor_adapter.stop_motors()
