from communication.sims import sim


class CoppeliaMotorAdapter:
    """
    Essa classe centraliza os comandos enviados para os motores do simualdor.
    """

    def __init__(self, clientID, motorE_handle, motorD_handle):
        """
        Essa classe centraliza os comandos enviados para os motores do simualdor.

        Na inicialização, é necessário passar os dados do simulador corretamente.

        Args:
           clientID: clientID
           motorE_handle: motorE
           motorD_handle: motorD

           obs: Todos são retornos da função "connect_to_coppelia".
        """
        self.clientID = clientID
        self.motorE = motorE_handle
        self.motorD = motorD_handle

    def send_velocities(self, vl: int, vr: int):
        """
        Envia as velocidades instantaneamente para os motores do simulador.

        Args:
            vl: Velocidade da roda esquerda.
            vr: Velocidade da roda direita.
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
        """
        Envia velocidade nula (0, 0) para os motores do simulador.
        """
        self.send_velocities(0, 0)
