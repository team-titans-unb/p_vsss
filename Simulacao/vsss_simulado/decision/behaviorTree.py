import py_trees
import math
import time
from common.math_utils import wrap_angle
from common.controller_maths import speed_control


class IsBallVisible(py_trees.behaviour.Behaviour):
    def __init__(self, name="Verificar_Visibilidade_da_Bola"):
        super().__init__(name) # chama o construtor da classe pai

        # acessa a blackboard 
        self.bb = py_trees.blackboard.Client(name="robo_1")

        # registra a chave da posição da bola
        self.bb.register_key(key="ball_position", access=py_trees.common.Access.READ)
        self.bb.register_key(key="robot_position", access=py_trees.common.Access.READ)
        self.bb.register_key(key="robot_orientation", access=py_trees.common.Access.READ)


    def update(self):
        ball_pos = self.bb.ball_position
        #ball_pos = None

        # não enxerga a bola
        if ball_pos is None:
            print("bola não foi encontrada")
            return py_trees.common.Status.FAILURE
        
        print("bola foi encontrada")
        return py_trees.common.Status.SUCCESS
    
class MoveToBall(py_trees.behaviour.Behaviour):
    def __init__(self, motor_adapter, pd_controller, linear_velocity, dt, name="Ir_Para_A_Bola"):
        super().__init__(name)
        self.motor_adapter = motor_adapter
        self.pd_controller = pd_controller
        self.linear_velocity = linear_velocity
        self.dt = dt
        self.last_speed_time = time.time()
        
        self.bb = py_trees.blackboard.Client(name="robo_1")

        self.bb.register_key(key="ball_position", access=py_trees.common.Access.READ)
        self.bb.register_key(key="robot_position", access=py_trees.common.Access.READ)
        self.bb.register_key(key="robot_orientation", access=py_trees.common.Access.READ)

    def update(self):
        robot_position = self.bb.robot_position
        ball_position = self.bb.ball_position
        robot_orientation = self.bb.robot_orientation

        if robot_position is None or ball_position is None or robot_orientation is None:
            return py_trees.common.Status.FAILURE

        # retirei da main
        robot_x, robot_y = robot_position
        ball_x, ball_y = ball_position

        desired_orientation = math.atan2(ball_y - robot_y, ball_x - robot_x)
        desired_orientation = wrap_angle(desired_orientation)
        robot_orientation = wrap_angle(robot_orientation)

        orientation_error = wrap_angle(desired_orientation - robot_orientation)
        angular_velocity = self.pd_controller.calculate_omega(orientation_error)

        current_time = time.time()
        if current_time - self.last_speed_time >= self.dt:
            vl, vr = speed_control(self.linear_velocity, angular_velocity)

            self.motor_adapter.send_velocities(vl, vr)
            self.last_speed_time = current_time

        return py_trees.common.Status.RUNNING

class StopRobot(py_trees.behaviour.Behaviour):
    def __init__(self, motor_adapter, name="Parar_Motores"):
        super().__init__(name)
        self.motor_adapter = motor_adapter

    def update(self):
        self.motor_adapter.stop_motors()
        return py_trees.common.Status.SUCCESS


class BehaviourTree:    
    def __init__(self, motor_adapter, pd_controller, linear_velocity, dt):
        self.isBallVisible = IsBallVisible()
        self.moveToBall = MoveToBall(
            motor_adapter=motor_adapter,
            pd_controller=pd_controller,
            linear_velocity=linear_velocity,
            dt=dt
        )
        self.stopRobot = StopRobot(motor_adapter=motor_adapter)

        self.sequence = py_trees.composites.Sequence(name="Seguir_Bola", memory=False)
        self.sequence.add_children([self.isBallVisible, self.moveToBall])

        self.root = py_trees.composites.Selector(name="Estrategia_Principal", memory=False)
        self.root.add_children([self.sequence, self.stopRobot])

        self.tree = py_trees.trees.BehaviourTree(root=self.root)
        self.tree.setup(timeout=15)

    def tick(self):
        self.tree.tick()


    