from communication.sims import sim


class CoppeliaMotorAdapter:
    def __init__(self, clientID, motorE_handle, motorD_handle):
        """
        Guarda as chaves de acesso aos motores do Coppelia.
        """
        self.clientID = clientID
        self.motorE = motorE_handle
        self.motorD = motorD_handle

    def send_velocities(self, vl, vr):
        """
        Envia as velocidades instantaneamente usando opmode_oneshot.
        """
        # Roda Esquerda
        sim.simxSetJointTargetVelocity(
            self.clientID, self.motorE, vl, sim.simx_opmode_oneshot
        )
        # Roda Direita
        sim.simxSetJointTargetVelocity(
            self.clientID, self.motorD, vr, sim.simx_opmode_oneshot
        )

    def stop_motors(self):
        """Útil para quando o jogo pausa ou o código é encerrado."""
        self.send_velocities(0, 0)
