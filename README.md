<div align="center">
  <img src=".Docs/Imgs/LogoTitans.png" alt="Logo da Equipe TITANS" width="200"/>

  # 🤖 VSSS - Robô de Futebol Autônomo
  **Equipe TITANS de Robótica | FCTE - Universidade de Brasília (UnB)**

  ![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-success)
  ![Linguagem](https://img.shields.io/badge/Linguagem-C%2B%2B%20%7C%20Python-blue)
  ![Hardware](https://img.shields.io/badge/Hardware-ESP32-orange)
  ![CAD](https://img.shields.io/badge/CAD-Fusion_360-red)
</div>

---

## ⚽ Sobre o Projeto
Este repositório contém o código-fonte, esquemas eletrônicos e documentação mecânica dos robôs da categoria **VSSS (Very Small Size Soccer)** da equipe TITANS. 

A categoria VSSS consiste em partidas de futebol de robôs autônomos de 3 contra 3. Cada robô deve caber em um cubo de 7.5 x 7.5 x 7.5 cm e não possui controle humano durante o jogo. Toda a estratégia, controle PID, visão computacional e comunicação sem fio operam em conjunto para que o time marque gols e defenda sua área.

<div align="center">
  <img src="[z]" alt="Robô VSSS em ação" width="600"/>
</div>

---

## 🗺️ Arquitetura do Repositório
Para facilitar o desenvolvimento multidisciplinar, nosso projeto está dividido nas seguintes áreas:

* 📂 **`/src`**: Código principal, incluindo a inteligência artificial, controle de trajetória e estratégias de jogo.
* 📂 **`/visao`**: Scripts de visão computacional (processamento da imagem da câmera sobre o campo).
* 📂 **`/eletronica`**: Esquemas de firmware, projetos de PCB e códigos para o microcontrolador (ESP32).
* 📂 **`/Estrutura`**: Versões estáveis (Releases) do projeto 3D (.STEP e .STL). *O desenvolvimento ativo de CAD ocorre no Autodesk Fusion.* (Veja o [README de Estrutura](./Estrutura/README.md) para acesso).

---

## 🛠️ Tecnologias Utilizadas
* **Software/Estratégia:** C++, Python, OpenCV.
* **Controle e Otimização:** Algoritmos de controle (PID) e planejamento de rotas.
* **Hardware:** Microcontrolador ESP32, módulos de rádio, motores DC com encoder.
* **Mecânica:** Autodesk Fusion (Modelagem 3D) e Impressão 3D.

---

## 🚀 Como Começar (Setup Local)

### Pré-requisitos
Antes de começar, você precisará ter instalado em sua máquina:
* [Git](https://git-scm.com/)
* [Python 3.x](https://www.python.org/) ou Compilador C++
* [CMake](https://cmake.org/) (se aplicável)

### Instalação
1. Clone este repositório:
   ```bash
   git clone [https://github.com/](https://github.com/)[SEU_USUARIO_OU_ORGANIZACAO]/[NOME_DO_REPOSITORIO].git
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd [NOME_DO_REPOSITORIO]
   ```
3. Instale as dependências necessárias (Exemplo para Python):
   ```bash
   pip install -r requirements.txt
   ```
4. Siga as instruções específicas de compilação dentro da pasta de cada subsistema (ex: `/src` ou `/visao`).

---

## 🤝 Como Contribuir
Ficamos felizes com o interesse em contribuir com a TITANS! Para garantir a organização do código:

1. Crie uma *branch* para a sua feature ou correção: `git checkout -b feature/minha-feature`
2. Faça os *commits* de forma clara e descritiva: `git commit -m "feat: Adiciona novo filtro de imagem"`
3. Envie para o repositório remoto: `git push origin feature/minha-feature`
4. Abra um **Pull Request (PR)** e aguarde a revisão dos líderes do projeto.

*(Se você for da equipe de Mecânica, lembre-se de ler o [Guia do Fusion 360](./Estrutura/README.md) antes de alterar as peças).*

---

## 📞 Equipe e Contatos
Desenvolvido com 💙 pela **Equipe TITANS**.

* **Instagram:** [@titans_robotica](LINK_AQUI)
* **Email:** [EMAIL_DA_EQUIPE]
* **Local:** FCTE - Universidade de Brasília (UnB), Campus Gama.

---
*Licença MIT - Sinta-se livre para usar, estudar e modificar este projeto.*
