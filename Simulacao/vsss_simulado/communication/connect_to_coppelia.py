import communication.sims.sim as sim
import sys


def connect_to_coppelia(ip: str, port: int) -> tuple:
    """
    Função utilizada para conectar a porta do Coppelia para enviar comandos.
    """
    sim.simxFinish(-1)
    clientID = sim.simxStart(
        ip, port, True, True, 2000, 5
    )  # Tenta a conexão com o CoppeliaSim

    if clientID != -1:
        print("Conectando ao CoppeliaSim na porta: ", port)
    else:
        print("Falha ao tentar se conectar à porta: ", port)
        sys.exit()

    # Pega os handles (identificadores) dos objetos na cena
    _, robot = sim.simxGetObjectHandle(clientID, "robot01", sim.simx_opmode_blocking)
    _, motorE = sim.simxGetObjectHandle(clientID, "motorL01", sim.simx_opmode_blocking)
    _, motorD = sim.simxGetObjectHandle(clientID, "motorR01", sim.simx_opmode_blocking)
    _, ball = sim.simxGetObjectHandle(clientID, "ball", sim.simx_opmode_blocking)

    # print(f"DEBUG: s_rob: {s_rob} | s_motE: {s_motE} | s_motD: {s_motD} | s_ball: {s_ball}")

    return (clientID, robot, motorE, motorD, ball)
