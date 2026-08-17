## Metodologia de otimização

A otimização do GerOndApp foi conduzida utilizando profiling e
benchmarking, evitando alterações baseadas apenas em percepção subjetiva
de desempenho.

### Profiling

Profiling é o processo de identificar onde uma aplicação consome seus
recursos, permitindo localizar gargalos de processamento e memória.

Nesta etapa, o backend do GerOndApp foi instrumentado utilizando
`time.perf_counter()`, separando o processamento da requisição `sendData`
em diferentes regiões:

- geração dos sinais;
- cálculo das FFTs;
- inicialização da resultante;
- operações da resultante;
- conversão dos arrays NumPy para listas Python (`tolist`);
- FFT da resultante;
- conversão da resultante para listas.

O objetivo do profiling é responder:

> Onde o GerOndApp está gastando tempo?

### Benchmark

Benchmark é um teste controlado utilizado para medir e comparar o
desempenho da aplicação.

Foram definidos cenários utilizando diferentes taxas de amostragem e
durações, mantendo os mesmos parâmetros ao comparar versões do código.

Exemplo:

- taxa de amostragem: 44.100 Hz;
- duração: 10 segundos;
- número de amostras: 441.000.

O objetivo do benchmark é responder:

> Quanto tempo o GerOndApp leva para realizar determinada operação e
> quanto esse tempo mudou após uma otimização?

### Baseline

O baseline corresponde ao desempenho da implementação antes das
otimizações e serve como referência para comparações posteriores.

Após cada subetapa de otimização, os mesmos cenários de benchmark são
executados novamente e comparados com o baseline.

Podemos ainda definir uma baseline para cada etapa do processo de otimização

A metodologia utilizada pode ser resumida pelo ciclo:

Profiling → identificação do gargalo → otimização → benchmark →
comparação → novo profiling.

# Benchmark do backend (ETAPA 2A)

## BASELINE etapa 0 (2A)

### 1. Rate: 1000 X duracao: 1 $\hspace{1cm}$      nº amostras = 1000

Geração:*                  2.353 ms

Inicialização resultante:   0.026 ms 

Calculo resultante:         0.032 ms 

FFT:                        0.800 ms

FFT Resultante:             0.094 ms 

tolist:                     0.441 ms

tolist resultante:          0.087 ms


**Total view:                 4.005 ms**
---
### 2. Rate: 44100 X duracao: 1    $\hspace{1cm}$     nº amostras = 44100

Geração:                    23.859 ms

Inicialização resultante:   0.124 ms 

Calculo resultante:         0.557 ms 

FFT:                        14.727 ms

FFT Resultante:             2.976 ms 

tolist:                     16.944 ms

tolist resultante:          3.276 ms

**TOTAL view:                 62.710 ms**
---
### 3. Rate: 44100 X duracao: 10   $\hspace{1cm}$     nº amostras = 441000

Geração:                    314.106 ms

Inicialização resultante:   1.664 ms

Calculo resultante:         12.702 ms 

FFT:                        235.746 ms

FFT Resultante:             41.895 ms 

tolist:                     172.469 ms

tolist resultante:          35.420 ms

TOTAL view:                 814.218 ms
---



## BASELINE etapa 1 (2B concluída)

### 1. Rate: 1000 X duracao: 1     $\hspace{1cm}$     nº amostras = 1000

Geração:                    2.388 ms

Inicialização resultante:   0.022 ms 

Calculo resultante:         0.013 ms 

FFT:                        0.638 ms

FFT Resultante:             0.117 ms 

tolist:                     0.344 ms

tolist resultante:          0.068 ms

**TOTAL view:                 3.741 ms**
---

### 2. Rate: 44100 X duracao: 1     $\hspace{1cm}$    nº amostras = 44100

Geração:                    23.915 ms

Inicialização resultante:   0.097 ms 

Calculo resultante:         0.167 ms 

FFT:                        17.500 ms

FFT Resultante:             3.003 ms
 
tolist:                     20.129 ms

tolist resultante:          3.220 ms

**TOTAL view:                 68.225 ms**
---

### 3. Rate: 44100 X duracao: 10   $\hspace{1cm}$     nº amostras = 441000

Geração:                    308.129 ms

Inicialização resultante:   1.401 ms 

Calculo resultante:         3.571 ms

FFT:                        225.459 ms

FFT Resultante:             42.383 ms 

tolist:                     165.666 ms

tolist resultante:          32.523 ms

**TOTAL view:                 779.308 ms**
---

### CONCLUSÃO ETAPA 2B — Remoção de cópias NumPy redundantes
- array(...) removidos de sinais já ndarray
- return array(sinal) → return sinal
- return array(soma_sub * mult_div) → expressão direta
- comportamento preservado
- ganho de tempo: modesto / variável
- ganho de clareza e memória: real

## BASELINE 2C

### Rate: 1000 X duracao: 1    $\hspace{1cm}$       nº amostras = 1000

Geração:                    1.362 ms

Inicialização resultante:   0.024 ms 

Calculo resultante:         0.016 ms 

FFT:                        0.727 ms

FFT Resultante:             0.108 ms 

tolist:                     0.423 ms

tolist resultante:          0.088 ms

TOTAL view:                 3.094 ms
--- 

### Rate: 44100 X duracao: 1   $\hspace{1cm}$      nº amostras = 44100

Geração:                    21.534 ms

Inicialização resultante:   0.050 ms 

Calculo resultante:         0.111 ms 

FFT:                        17.336 ms

FFT Resultante:             2.821 ms 

tolist:                     17.022 ms

tolist resultante:          3.235 ms

TOTAL view:                 62.659 ms
---

### Rate: 44100 X duracao: 10    $\hspace{1cm}$    nº amostras = 441000

Geração:                    310.012 ms

Inicialização resultante:   1.415 ms 

Calculo resultante:         5.122 ms 

FFT:                        229.884 ms

FFT Resultante:             47.334 ms 

tolist:                     196.946 ms

tolist resultante:          40.338 ms

TOTAL view:                 836.481 ms

### Conclusão Etapa 2C — Compartilhamento do vetor temporal

Foi identificado que todos os sinais utilizavam os mesmos parâmetros
globais de taxa de amostragem e duração, porém cada função geradora
construía independentemente seu próprio vetor temporal.

A implementação foi refatorada para criar um único vetor temporal por
requisição, posteriormente compartilhado entre todos os sinais.

Além da redução de operações redundantes, a alteração separou a definição
do domínio temporal da geração das formas de onda.

Nos benchmarks, o ganho isolado foi relativamente pequeno e sujeito à
variabilidade entre execuções. Para 44.100 amostras foi observada redução
de aproximadamente 8% no tempo total da view. Para 441.000 amostras, a
geração dos sinais apresentou redução aproximada de 5%, embora a
variabilidade entre execuções impeça atribuir com precisão todo o ganho à
alteração.

A principal vantagem da etapa foi, portanto, tanto computacional quanto
arquitetural: todos os sinais passaram a compartilhar explicitamente o
mesmo domínio temporal.