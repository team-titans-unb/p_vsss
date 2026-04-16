import math


def wrap_angle(angle: float) -> float:
    """
    Essa função coloca qualquer valor de orientação (em radianos) no intervalo [-pi, pi]. Busca o caminho mais curto para o resultado final.

    Args:
        angle (float): A angulação que você queira colocar no intervalo [-pi, pi].

    Returns:
        float: Um ângulo em radianos, no intervalo [-pi, pi].

    Exemple:
        >>> wrap_angle(3*pi)
        pi

        >>> wrap_angle(0.5*pi)
        0.5*pi

        >>> wrap_angle(1.5*pi)
        -0.5*pi

        obs: Perceba como girar 1.5*pi é como girar -0.5*pi, portanto a função retornou o caminho mais curto para um mesmo resultado final.
    """
    return (angle + math.pi) % (2 * math.pi) - math.pi


def euclidean_distance(coords: tuple[float, float, float, float]) -> float:
    """
    Essa função retorna a distância euclidiana entre dois pontos.

    Args:
        coords (tupla): Uma tupla com 4 valores (x1, y1, x2, y2), referente as coordenas.
    """
    x1, y1, x2, y2 = coords
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
