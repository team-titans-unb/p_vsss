# 🎮 Simulação VSSS - TITANS

A simulação é o laboratório onde o futuro do VSSS da TITANS ganha vida. É aqui que os próximos grandes passos do nosso projeto estão sendo dados. 

Antes de colocarmos os robôs no campo físico, é neste ambiente virtual que testamos novas estratégias de jogo, calibramos nossa visão computacional, ajustamos o controle PID dos motores e desenvolvemos a inteligência artificial do time. Cada linha de código validada aqui representa a evolução direta da nossa equipe para as próximas competições.

---

## ⚙️ Como funciona o nosso ambiente?

Para simular o jogo, nós utilizamos o **Webots** em conjunto com o **TraveSim** (um ambiente de simulação específico para o IEEE VSSS). 

Para manter nosso repositório organizado e leve, **não armazenamos os arquivos do TraveSim diretamente aqui**. Em vez disso, criamos um script automatizado que baixa e compila a versão mais recente do simulador diretamente na sua máquina.

### 📋 Pré-requisitos
Antes de rodar a simulação, certifique-se de ter instalado:
1. **[Webots](https://cyberbotics.com/)**: O software de simulação principal.
2. Ferramentas de compilação básicas (geralmente já vêm no Linux, como `make` e `gcc`).

---

## 🚀 Como Configurar e Rodar

Siga o passo a passo abaixo para preparar o ambiente na sua máquina pela primeira vez:

### 1. Execute o Script de Instalação
Abra o seu terminal dentro desta pasta (`Simulacao`) e dê permissão de execução ao script de setup (caso ainda não tenha). Depois, execute-o:

```bash
chmod +x setup.sh
./setup.sh
```
*O que esse script faz?* Ele clona o repositório oficial do TraveSim automaticamente para dentro desta pasta e roda o comando `make` para compilar o projeto para o seu sistema operacional.

### 2. Abra o Simulador
1. Abra o **Webots** no seu computador.
2. Vá em `File > Open World...`
3. Navegue até a pasta `Simulacao/travesim/worlds` (que acabou de ser criada pelo script) e abra o arquivo do mundo do TraveSim.

### 3. Rode a Estratégia da TITANS
Com o simulador aberto e o jogo pausado/rodando, você já pode executar os nossos scripts de estratégia que estão aqui na pasta raiz da `Simulacao`.

---

## ⚠️ Nota Importante para Desenvolvedores

Se você rodar o `git status` após usar o script, notará que a pasta `travesim/` não aparece como uma alteração pendente. 

Isso é proposital! Nós adicionamos a regra `travesim/` no nosso arquivo **`.gitignore`**. Dessa forma, você pode compilar e alterar o simulador localmente sem o risco de subir arquivos binários pesados e desnecessários para o GitHub da TITANS. 

**Nesta pasta do GitHub, versionamos apenas os nossos scripts de inteligência e controle.**
