class PDController:
    """
    Essa classe centraliza o cálculo da velocidade ângular do robô em cada instante dt.
    """

    def __init__(self, kp: float, kd: float, filter_alpha: float, dt: float) -> None:
        """
        Na inicialização da um objeto "PD_Controller", os seguintes argumentos devem ser passados:

        Args:
            kp: O valor da constante proporcional.
            kd: O valor da constante derivativa.
            filter_alpha: A força de filtragem, deve ser entre [1, 0) -> 1: Confiança total no error atual; -> ~0: Confiança total no erro passado.
            dt: Tempo de iteração.
        """
        self.kp = kp
        self.kd = kd
        self.filter_alpha = filter_alpha
        self.filtered_previous_error = 0
        self.dt = dt

    def calculate_omega(self, error: float) -> float:
        """
        Essa função calcula o omega (velocidade ângular) do robô.

        Args:
            error: Quantidade de erro na orientação atual do robô em relação a orientação alvo, no intervalo de [-pi, pi].

        """
        proporcional_term = self.kp * error

        filtered_error = (error * self.filter_alpha) + (
            1 - self.filter_alpha
        ) * self.filtered_previous_error
        derivative_term = (
            self.kd * (filtered_error - self.filtered_previous_error) / self.dt
        )

        self.filtered_previous_error = filtered_error
        omega = proporcional_term + derivative_term
        return omega
