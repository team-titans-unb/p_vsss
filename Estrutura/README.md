# ⚙️ Estrutura e Mecânica - VSSS

Todo o desenvolvimento ativo de CAD, modelagem 3D e montagem do nosso robô é realizado no **Autodesk Fusion**.

Devido às limitações de versionamento de arquivos binários no Git, utilizamos este repositório apenas para armazenar **versões estáveis (releases)** e arquivos prontos para manufatura/impressão.

## 🔗 Como acessar o projeto no Fusion

Para visualizar o projeto completo, histórico de modificações ou contribuir com a modelagem da mecânica:

1. Crie uma conta na [Autodesk](https://www.autodesk.com/) (recomenda-se usar o e-mail institucional para a licença educacional).
2. Solicite o convite para o nosso projeto no Fusion Team enviando uma mensagem no nosso canal de comunicação ou entrando em contato com os diretores de mecânica.
3. [Link de visualização pública do CAD atual] *(Opcional: O Fusion permite gerar um link de visualização na web que você pode colocar aqui para quem só quer "olhar" o robô em 3D sem ter conta).*

## 📂 Organização desta pasta

Aqui no GitHub, você encontrará apenas arquivos estáticos das versões finalizadas do robô:

* `/STL`: Peças isoladas e otimizadas, prontas para fatiamento e impressão 3D.
* `/STEP`: Montagem completa do robô em formato universal, ideal para a equipe de software consultar medidas, encaixes e geometria.
* `/Documentacao`: Desenhos técnicos, cálculos de torque, escolha de motores e relatórios de montagem.

## 🛠️ Fluxo de Trabalho
1. Todo novo design é desenhado no Fusion.
2. Ao finalizar uma versão estrutural do robô (ex: "Chassi V2"), o responsável exporta o `.STEP` da montagem e os novos `.STL`.
3. É feito um *Commit* e um *Pull Request* atualizando os arquivos nesta pasta.
