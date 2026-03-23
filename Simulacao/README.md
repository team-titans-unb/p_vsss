# 🎮 Simulação VSSS - TITANS

A simulação é o laboratório onde o futuro do VSSS da TITANS ganha vida. É aqui que os próximos grandes passos do nosso projeto estão sendo dados. 

Antes de colocarmos os robôs no campo físico, é neste ambiente virtual que testamos novas estratégias de jogo, calibramos nossa visão computacional, ajustamos o controle PID dos motores e desenvolvemos a inteligência artificial do time. Cada linha de código validada aqui representa a evolução direta da nossa equipe para as próximas competições.

---

## ⚙️ Como funciona o nosso ambiente?

Para simular o jogo, nós utilizamos o **Webots** em conjunto com o **TraveSim** (um ambiente de simulação específico para o IEEE VSSS). 

Para manter nosso repositório organizado e leve, **não armazenamos os arquivos do TraveSim diretamente aqui**. Em vez disso, criamos um script automatizado que baixa e compila a versão mais recente do simulador diretamente na sua máquina.

### 📋 Pré-requisitos
Antes de rodar a simulação, certifique-se de ter instalado:
1. **[CoppeliaSim](https://www.coppeliarobotics.com/)**: O software de simulação principal.
2. Ferramentas de compilação básicas (geralmente já vêm no Linux, como `make` e `gcc`).

---

## 🚀 Como Configurar e Rodar

Siga o passo a passo abaixo para preparar o ambiente na sua máquina pela primeira vez:

### 1. Abra o mundo no Simulador
1. Abra o CoppeliaSim
2. Vá em `File -> Open Scene` 
3. Abra o mundo "oneRobot.ttt", em `Simulacao/worlds`.



### 2. Aperte o Play
1. Aperte no botão PLAY(Start/resume simulation) 
2. Rode o código "main.py" em `Simulacao/vsss_simulado`.
3. Veja a mágica acontecer!!

