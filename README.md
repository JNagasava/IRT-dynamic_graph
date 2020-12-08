# IRT-dynamic_graph
Aplicação que faz a simulação da curva característica e de informação do item, a partir do modelo de **Teoria de Resposta ao Item** (TRI) com 3 parâmetros.

## Descrição

Esta aplicação, a qual foi desenvolvida em python, tem como função representar graficamente a curva característica e de informação do item a partir do modelo de 3 parâmetros da TRI. 

* **Modelo de 3 parâmetros**

<p align="center">
<img src="https://latex.codecogs.com/gif.latex?\dpi{90}&space;\huge&space;P(\theta)&space;=&space;c&space;&plus;&space;\frac{1&space;-&space;c}{1&space;&plus;&space;e^{-a(\theta-b)}}" title="\huge P(\theta) = c + \frac{1 - c}{1 + e^{-a(\theta-b)}}" />
  </p>

* **Informação do Item**

<p align="center">
  <img src="https://latex.codecogs.com/gif.latex?\dpi{90}&space;\huge&space;I(\theta)&space;=&space;a^{2}&space;\frac{(P(\theta)&space;-&space;c)^{2}}{(1&space;-&space;c)^{2}}&space;\frac{Q(\theta)}{P(\theta)}" title="\huge I(\theta) = a^{2} \frac{(P(\theta) - c)^{2}}{(1 - c)^{2}} \frac{Q(\theta)}{P(\theta)}" />
  </p>

As curvas são geradas de forma dinâmica a partir da variação dos parâmetros *a* (*discriminante do item*), *b* (*dificuldade do item*) e *c* (*acerto ao acaso*). 

Além de gerar as curvas, é possível utilizar um segundo modelo para comparação.

## Demo

Pela demosntração a seguir, é possível ter uma noção dos recursos e funcionalidades que a aplicação tem:

<p align="center">
  <img src="https://github.com/JNagasava/IRT-dynamic_graph/blob/main/assets/demo.gif"/>
</p>

## Execução

Para a execução dos arquivo, é necessário fazer o upload dos arquivos (*basta clicar em Code na parte superior da página e em seguida clicar em download zip*).

Já dentro da pasta com os arquivos, execute o seguinte comando no terminal para baixar as bibliotecas que a aplicação utiliza:

```
pip install requirements.txt
```

Por fim, para iniciar a aplicação, basta executar o seguinte comando:

```
python main.py
```

## Executáveis

Caso o seu interesse seja apenas utilizar a aplicação em seu estado original (sem a modificação de nenhum parâmetro ou *feature*), baixe o executável abaixo, de acordo com o seu sistema operacional:

* [windows (opção 1)](https://github.com/JNagasava/IRT-dynamic_graph/blob/main/executables/simulador_TRI_windows_x64.exe)
* [windows (opção 2)](https://github.com/JNagasava/IRT-dynamic_graph/blob/main/executables/Simulador_TRI.zip)
* [linux](https://github.com/JNagasava/IRT-dynamic_graph/blob/main/executables/irt_graph)

*Obs.: Na opção 1 do windows será baixado somente o executável (dependendo do ambiente, a execução pode ser mais lenta). Na opção 2 será baixado o diretório junto com as bibliotecas utilizadas (esta opção é mais rápida).*

## Ambiente de Desenvolvimento utilizado

* ubuntu 18.04 LTS x86_64
* Python 3.7.9
