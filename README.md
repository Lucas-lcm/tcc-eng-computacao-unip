# Trabalho de conclução se curso Engenharia de Computação
Trabalho de conclução se curso, para o bacharelado em Engenharia de Computação pela Universidade Paulista, onde tivemos que integrar hardware e software

# Objetivo e contexto:
## 1.2.1. Objetivo Geral
  Esta monografia tem por objetivo realizar um levantamento, fornecer um
  diagnóstico e sugerir um tratamento viável para patologias asfálticas através do
  uso da tecnologia da visão computacional.
## 1.2.2. Objetivos Específicos
  Para se atingir o Objetivo Geral, é necessário:
  - Realizar uma revisão bibliográfica, em forma de um referencial teórico,
  sobre as tecnologias que serão utilizadas, abordando aspectos técnicos;
  - Propor soluções técnicas, sustentáveis e economicamente viáveis para
  corrigir as patologias identificadas, considerando as especificidades de
  cada caso estudado; e
  - Avançar no conhecimento sobre o tema, por meio da documentação dos
  resultados, da discussão crítica sobre as práticas adotadas e das
  recomendações para futuros estudos e intervenções.

## Contexto
  A visão computacional é uma área dentro de inteligência artificial que possui
  grande impacto em vários setores da sociedade. A capacidade da máquina enxergar
  objetos de interesse em uma imagem e produzir uma resposta de classificação ou
  detecção de elementos é de suma importância no contexto de automação. As técnicas
  de visão computacional permitem, através de etapas de tratamento de imagem e do
  uso de classificadores, oferecer respostas a diversos problemas que se apresentam.
  Esta monografia objetiva, levantar, diagnosticar e propor tratamento de patologias
  asfálticas por meio da visão computacional, que analisará imagens dos mais diversos
  pavimentos, para identificação de patologias presentes no mesmo, com o intuito de
  informar o melhor tratamento, assim criando um cenário mais eficaz e pragmático no
  trabalho de manutenção de vias de pavimento.

## Hardware
  Utilizamos para montagem da nossa solução:
  - ESP32;
  - Sensor ultrasônico;
  - RASPBERRY PI3;
  - RASPBERRY CAM;
  - Placa CI para integrar os componentes.

## Software
  De forma resumida, temos dois códigos principais:
  - Código de configuração do ESP32 em C++ Arduino <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg" height="40" width="40" />
  - Código que controla a solução IOT em Python <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="40" width="40" />
  Além disso, utilizei as APIs do Google Cloud, para enviar os dados de análise para o Drive, e também as APIs do RoboFlow para realizar a análise das patologias.
