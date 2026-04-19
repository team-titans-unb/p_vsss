from typing import Dict
import py_trees


class VSSSBlackBoardManager:
    """
    Essa classe inicia a BlackBoard do sistema, local onde ficarão os dados mais recentes [filtrados] do ambiente.
    """

    def __init__(self):
        """
        Essa classe inicia a BlackBoard do sistema, local onde ficarão os dados mais recentes [filtrados] do ambiente.        
        """
        # 1 Passo: Criar o cliente
        self.data = py_trees.blackboard.Client(name="Vision_Manager")

        # 2 Passo: Registrar os Contratos Globais (Chaves)

        for i in range(1, 4):
            self.data.register_key(key=f"/robot_{i}/robot_position", access=py_trees.common.Access.WRITE) 
            self.data.register_key(key=f"/robot_{i}/robot_orientation", access=py_trees.common.Access.WRITE)
            self.data.register_key(key=f"/robot_{i}/ball_position", access=py_trees.common.Access.WRITE) 
        
            # 3 Passo: Definir estado inicial seguro
            
            self.data.set(f"/robot_{i}/robot_position", None)
            self.data.set(f"/robot_{i}/robot_orientation", None)
            self.data.set(f"/robot_{i}/ball_position", None)


    def update(
        self, robot_name: str, dados: Dict[str, tuple[float | None, float | None]]
    ) -> None:
        """
        Recebe um dicionário de visão e publica na BlackBoard.

        Args:

            dados: Um dicionário que DEVE possuir, independente do caso, as seguinte chaves:
                'ball_position':     apontando para uma tupla com 2 posições -> float ou None,
                'robot_position':    apontando para uma tupla com 2 posições -> float ou None,
                'robot_orientation': um único valor -> float ou None.
            robot_name: Nome do robô que está atualizando seus dados. Deve ser igual ao que está registrado na BlackBoard.
        """

        self.data.set(f"{robot_name}/ball_position", dados.get("ball_position", None))
        self.data.set(f"{robot_name}/robot_orientation", dados.get("robot_orientation", None))
        self.data.set(f"{robot_name}/robot_position", dados.get("robot_position", None))
    
    def update_ball(self, ball_position: tuple[float, float] | None) -> None:
        """
        Recebe a posição da bola em formato de tupla e publica na BlackBoard.

        Args:
            ball_pos(tupla): Uma tupla com duas posições (ball_x, ball_y).
        """

        self.data.ball_position = ball_position
