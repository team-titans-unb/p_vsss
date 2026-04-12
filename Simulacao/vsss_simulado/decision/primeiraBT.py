import py_trees
import random
import time

class simulacao:
    def __init__(self):
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_v = 10
        self.ball_x = 50.0
        self.ball_y = 50.0
        self.ball_visible = True

    def update_robot(self):
        self.robot_x += random.choice([-1, 0, 1]) * self.robot_v
        self.robot_y += random.choice([-1, 0, 1]) * self.robot_v

    def robot_engine(self):
        self.robot_v = 0

    def robot_state(self):
        return {
            "x": self.robot_x,
            "y": self.robot_y
        }
    def ball_state(self):
        return {
            "visible": self.ball_visible,
            "x": self.ball_x,
            "y": self.ball_y
        }

class IsBallVisible(py_trees.behaviour.Behaviour):
    def __init__(self, simu, name="Verificar_Visibilidade_da_Bola"):
        super().__init__(name) # chama o construtor da classe pai
        self.simu = simu

    def update(self):
        self.ball_info = self.simu.ball_state()

        if self.ball_info.get("visible"):
            print("bola foi encontrada")
            return py_trees.common.Status.SUCCESS
        
        print("bola não foi encontrada")
        return py_trees.common.Status.FAILURE
    
class MoveToBall(py_trees.behaviour.Behaviour):
    def __init__(self, simu, name="Ir_Para_A_Bola"):
        super().__init__(name)
        self.simu = simu 

    def update(self):
        # chama a função que atualiza a mov do robo na simulacao
        self.simu.update_robot()

        pos = self.simu.robot_state()
        print(f"o robo esta se movendo em x: {pos['x']} y: {pos['y']}")

        return py_trees.common.Status.RUNNING

class StopRobot(py_trees.behaviour.Behaviour):
    def __init__(self, simu, name="Parar_Motores"):
        super().__init__(name)
        self.simu = simu

    def update(self):
        self.simu.robot_engine()
        print("motores desligados")

        return py_trees.common.Status.SUCCESS


class BehaviourTree:    
    def __init__(self, simu):
        self.simu = simu
        
        #cria os nós de comportamento
        self.is_ball_visible = IsBallVisible(simu)
        self.move_to_ball = MoveToBall(simu)
        self.stop_robot = StopRobot(simu)
        
        # cria a sequência: bola visível E mover
        self.sequence = py_trees.composites.Sequence(
            name="Seguir_Bola",
            memory=False
        )
        self.sequence.add_children([self.is_ball_visible, self.move_to_ball])
        
        # cria o fallback: tenta sequência, se falhar para motores
        self.root = py_trees.composites.Selector(
            name="Estrategia_Principal",
            memory=False
        )
        self.root.add_children([self.sequence, self.stop_robot])

        # cria a árvore de comportamento
        self.tree = py_trees.trees.BehaviourTree(root=self.root)
        self.tree.setup(timeout=15)
    
    def run(self, iterations=10):
        for i in range(iterations):
            self.tree.tick()
            
            # Exibe a árvore com status em tempo real
            print(f"\n{'='*60}")
            print(f"Iteração {i+1}/{iterations}")
            print(f"{'='*60}")
            print(py_trees.display.unicode_tree(self.root, show_status=True))
            
            time.sleep(2)

if __name__ == "__main__":
    sim = simulacao()
    bt = BehaviourTree(sim)
    bt.run()     