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
        self.data.register_key(key="ball_position", access=py_trees.common.Access.WRITE)
        self.data.register_key(
            key="robot_position", access=py_trees.common.Access.WRITE
        )
        self.data.register_key(
            key="robot_orientation", access=py_trees.common.Access.WRITE
        )

        # 3 Passo: Definir estado inicial seguro
        self.data.ball_position = [0, 0, 0]
        self.data.robot_position = [0, 0, 0]
        self.data.robot_orientation = 0

    def update(self, dados: Dict[str, tuple[float | None, float | None]]) -> None:
        """
        Recebe um dicionário de visão e publica na BlackBoard.

        Args:

            dados: Um dicionário que DEVE possuir, independente do caso, as seguinte chaves:
                'ball_position':     apontando para uma tupla com 2 posições -> float ou None,
                'robot_position':    apontando para uma tupla com 2 posições -> float ou None,
                'robot_orientation': um único valor -> float ou None.
        """

        self.data.ball_position = dados.get("ball_position", None)
        self.data.robot_position = dados.get("robot_position", None)
        self.data.robot_orientation = dados.get("robot_orientation", None)
