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
        self.bb = py_trees.blackboard.Client(name="Vision_Manager")

        # 2 Passo: Registrar os Contratos Globais (Chaves)
        self.bb.register_key(key="ball_position", access=py_trees.common.Access.WRITE)
        self.bb.register_key(key="robot_position", access=py_trees.common.Access.WRITE)
        self.bb.register_key(
            key="robot_orientation", access=py_trees.common.Access.WRITE
        )

        # 3 Passo: Definir estado inicial seguro
        self.bb.ball_position = None
        self.bb.robot_position = None
        self.bb.robot_orientation = 0.0

    def update_from_vision(
        self, dados: Dict[str, tuple[float | None, float | None]]
    ) -> None:
        """
        Recebe um dicionário de visão e publica na BlackBoard.

        Args:

            dados: Um dicionário que DEVE possuir, independente do caso, as seguinte chaves:
                'ball_position':     apontando para uma tupla com 2 posições -> float ou None,
                'robot_position':    apontando para uma tupla com 2 posições -> float ou None,
                'robot_orientation': um único valor -> float ou None.
        """
        if dados is None:
            # Caso a visão tenha falhado:
            self.bb.ball_position = None
            self.bb.robot_position = None
            self.bb.robot_orientation = 0.0
            return

        # Publica os dados na BlackBoard
        self.bb.ball_position = dados.get("ball_position", (None, None))
        self.bb.robot_position = dados.get("robot_position", (None, None))
        self.bb.robot_orientation = dados.get("robot_orientation", None)
