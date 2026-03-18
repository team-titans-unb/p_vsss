#!/bin/bash
echo "Iniciando a configuração do ambiente de Simulação..."

# Clona o TraveSim se a pasta não existir
if [ ! -d "travesim" ]; then
  echo "Clonando o TraveSim..."
  git clone https://github.com/futebol-mini/travesim.git
else
  echo "Pasta travesim já existe. Atualizando..."
  cd travesim
  git pull
  cd ..
fi

# Compila o TraveSim
echo "Compilando o TraveSim..."
cd travesim
make

echo "Configuração concluída! Abra o mundo no Webots."
