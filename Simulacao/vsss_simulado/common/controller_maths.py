import math

from config.config import v_max


def speed_control(U, omega):
    """
    Essa função calcula o valor final de cada roda do robô, baseado na velocidade linear (U) e no omega.

    Args:
        U: Velocidade linear do robô. Ele andará nessa velocidade quando omega = 0.
        omega: Saída do controlador (PD). É a diferença que as velocidades das rodas devem ter para compensar o erro atual.
    """

    vr = (2 * U + omega * 7.5) / 3
    vl = (2 * U - omega * 7.5) / 3

    # Encontra o fator de escala necessário
    max_speed = max(abs(vr), abs(vl))
    if max_speed > v_max:
        scale_factor = v_max / max_speed
        vr *= scale_factor
        vl *= scale_factor

    if math.isnan(vr) or math.isnan(vl):
        vr, vl = 0, 0

    return int(vl), int(vr)
