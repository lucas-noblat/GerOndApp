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

## Benchmark do backend (ETAPA 2)

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

## ETAPA 2D - Correção matemática!

### Conclusão Etapa 2D - A substituição de linspace por arange(N)/Fs 

Corrigiu a discretização temporal, garantindo Δt = 1/Fs e eliminando a inclusão indevida do endpoint. Os benchmarks não indicaram alteração significativa de desempenho; a principal contribuição da etapa foi a correção matemática e a simplificação do modelo de amostragem.

## Etapa 2E — FFT otimizada para sinais reais

### Rate: 1000 × duração: 1        nº amostras = 1000

| Medida                       | Média      | Mediana    |
|-----------------------------|-----------:|-----------:|
| Geração                     | 1.562 ms   | 1.755 ms   |
| Inicialização resultante    | 0.033 ms   | 0.036 ms   |
| Cálculo resultante          | 0.021 ms   | 0.024 ms   |
| FFT                         | 0.595 ms   | 0.669 ms   |
| FFT Resultante              | 0.122 ms   | 0.122 ms   |
| tolist                      | 0.699 ms   | 0.762 ms   |
| tolist resultante           | 0.147 ms   | 0.157 ms   |
| TOTAL view                  | 3.357 ms   | 3.769 ms   |

### Rate: 44100 × duração: 1       nº amostras = 44100

     | Medida                       | Média      | Mediana    |
     |-----------------------------|-----------:|-----------:|
     | Geração                     | 23.242 ms  | 22.695 ms  |
     | Inicialização resultante    | 0.068 ms   | 0.059 ms   |
     | Cálculo resultante          | 0.194 ms   | 0.105 ms   |
     | FFT                         | 7.144 ms   | 6.495 ms   |
     | FFT Resultante              | 1.489 ms   | 1.490 ms   |
     | tolist                      | 21.728 ms  | 20.198 ms  |
     | tolist resultante           | 3.948 ms   | 3.665 ms   |
**| TOTAL view                  | 58.402 ms  | 55.202 ms  |**

### Rate: 44100 × duração: 10      nº amostras = 441000
#### Execuções estáveis

| Medida                       | Média      | Mediana    |
|-----------------------------|-----------:|-----------:|
| Geração                     | 282.151 ms | 281.892 ms |
| Inicialização resultante    | 1.605 ms   | 1.428 ms   |
| Cálculo resultante          | 3.794 ms   | 3.780 ms   |
| FFT                         | 118.178 ms | 116.803 ms |
| FFT Resultante              | 23.305 ms  | 23.351 ms  |
| tolist                      | 182.748 ms | 180.712 ms |
| tolist resultante           | 37.404 ms  | 36.130 ms  |
| TOTAL view                  | 655.082 ms | 647.312 ms |


A implementação original utilizava a FFT complexa completa (`fft`) e
posteriormente descartava as frequências negativas através de uma
máscara.

Como todos os sinais processados pelo GerOndApp são reais no domínio
temporal, foi utilizada a transformada específica para entradas reais
(`rfft`) juntamente com `rfftfreq`.

A alteração eliminou:

- cálculo explícito da metade negativa do espectro;
- vetor completo de frequências negativas;
- criação da máscara booleana;
- cópias realizadas durante a aplicação da máscara.

Nos benchmarks com 441.000 amostras, o tempo das FFTs dos cinco sinais
caiu aproximadamente de 250–300 ms para cerca de 110–130 ms.

A FFT da resultante caiu de aproximadamente 50 ms para cerca de 23 ms.

Considerando execuções estáveis, a redução no custo da FFT ficou próxima
de 50%, produzindo redução de aproximadamente 25–30% no tempo total da
view.

Após essa otimização, a FFT deixou de ser o principal gargalo do backend.
A geração dos sinais e a conversão dos arrays NumPy para listas Python
passaram a representar as maiores parcelas do tempo de processamento.

## Etapa 2E.3 — Normalização do espectro de Fourier

Após a substituição da FFT convencional (`fft`) pela transformada para sinais reais (`rfft`), foi realizada também a normalização da magnitude do espectro.

### Problema

A Transformada Discreta de Fourier não retorna diretamente a amplitude física do sinal.

Para uma senoide de amplitude `A`, contendo `N` amostras e cuja frequência coincide exatamente com um bin da FFT, a magnitude bruta dos coeficientes associados à senoide é aproximadamente:

$$
|X[k]| \approx \frac{N A}{2}
$$

Por exemplo:

- Número de amostras: `N = 1000`
- Amplitude da senoide: `A = 1`

A FFT não normalizada pode apresentar aproximadamente:

$$
|X[k]| \approx 500
$$


Isso não está relacionado à frequência de Nyquist e não representa uma amplitude real de 500.

O valor surge porque a DFT é uma soma das contribuições das `N` amostras e, para um sinal real, a contribuição de uma senoide aparece originalmente dividida entre as frequências positiva e negativa.

---

### Nyquist × normalização

É importante separar os dois conceitos.

#### Frequência de Nyquist

A frequência de Nyquist determina a maior frequência que pode ser representada sem aliasing:
$$
f_{Nyquist} = \frac{F_s}{2}
$$
Para:

$$
F_s = 44100 \text{ Hz}
$$

temos:

$$
f_{Nyquist} = 22050 \text{ Hz}
$$

Portanto, Nyquist está relacionado ao **eixo de frequências** do espectro.

### Normalização

A normalização determina como interpretar a **magnitude dos coeficientes da FFT**.

O objetivo adotado no GerOndApp é utilizar um espectro unilateral de amplitude, de forma que uma senoide de amplitude `A` apresente aproximadamente um pico de magnitude `A` em sua frequência correspondente.

---

### Primeira normalização

Após calcular a `rfft`:

```python
fft_sinal = fft.rfft(sinal)
```

## Etapa 2F - Serialização, parser e renderização no navegador

Agora chegamos provavelmente à etapa com maior potencial de reduzir a latência percebida pelo usuário. Até a 2E estivemos tornando o cálculo mais rápido. Na 2F, a pergunta muda para:

$$
\text{Depois que o NumPy terminou, por que ainda demora tanto para o gráfico aparecer?}
$$

E a resposta está no caminho completo:
```

NumPy ndarray
     ↓
.tolist()
     ↓
objetos Python
     ↓
DRF serializa JSON
     ↓
~136 MB de texto
     ↓
HTTP
     ↓
browser recebe
     ↓
response.json()
     ↓
objetos/arrays JavaScript
     ↓
Bokeh recebe os dados
     ↓
renderização
```

A principal regra da 2F será:


$$
\text{Antes de tentar serializar 136 MB mais rápido, vamos descobrir por que estamos enviando 136 MB.}
$$

### Etapa 2F.1 - Medindo a latência completa

Até o presente momento já sabemos o tempo que o backend demora para fazer os cálculos, a etapa 2 inteira foi atacando essa parte dos cálculos e da limpeza do código inútil em si.

Agora iremos tratar da parte após os calculos medidos, então iremos entender pq o tempo de calculo no backend e o tempo de percepção dos usuários

### Diagnóstico da Etapa 2F.1

A instrumentação end-to-end demonstrou que o tempo de processamento
medido dentro da view Django representa apenas uma pequena parcela da
latência percebida pelo usuário em sinais grandes.

Para 441.000 amostras, enquanto o processamento numérico da view havia
sido reduzido anteriormente para aproximadamente 650 ms em execuções
estáveis, o frontend apresentou mediana próxima de 10,4 segundos até o
fim da atualização síncrona dos dados no Bokeh.

A decomposição mostrou aproximadamente:

- 7,3 s até o recebimento dos headers;
- 0,8 s para consumir o corpo da resposta;
- 0,5 s para executar `JSON.parse`;
- 1–2 s para atualizar os `ColumnDataSource` do Bokeh.

O elevado tempo anterior ao recebimento dos headers indica que existe
custo significativo após a execução da lógica instrumentada da view,
provavelmente relacionado à renderização/serialização da resposta pelo
Django REST Framework, além de possíveis overheads do servidor.

A resposta para 441.000 amostras possui aproximadamente 136 MB, o que
também explica os custos posteriores de transferência, parsing e
renderização.

A Etapa 2F.1 demonstra, portanto, que o principal gargalo atual não está
mais concentrado no processamento NumPy. O volume e a representação dos
dados transferidos entre backend e frontend passaram a dominar a
latência percebida.

Isso motiva a próxima subetapa: eliminar informações redundantes do
payload antes de considerar otimizações do mecanismo de serialização.


### Etapa 2F.2A — Remoção de eixos redundantes no payload

Após as etapas anteriores, todos os sinais passaram a compartilhar o
mesmo vetor temporal e o mesmo eixo de frequências.

Entretanto, a resposta da API ainda enviava `x` e `xFreq` individualmente
para cada um dos cinco sinais e para a resultante.

A estrutura anterior era conceitualmente:

S1 → x, y, xFreq, yFreq  
S2 → x, y, xFreq, yFreq  
...  
Resultante → x, y, xFreq, yFreq

A resposta foi reorganizada para:

- um único `x`;
- um único `xFreq`;
- cinco pares `y/yFreq`;
- um par `y/yFreq` para a resultante.

Nenhuma amostra foi removida e nenhuma informação matemática foi perdida.

#### Resultados

Para 441.000 amostras, o tamanho da resposta caiu aproximadamente de
136 MB para 85 MB, correspondendo a uma redução de cerca de 37%.

A mediana da latência total medida no frontend caiu aproximadamente de
10,38 s para 6,96 s, uma redução próxima de 33%.

O tempo até o recebimento dos headers caiu aproximadamente 35%, e o
tempo necessário para consumir e interpretar o corpo da resposta caiu
cerca de 40%.

A conversão de arrays NumPy para listas Python também caiu de
aproximadamente 220 ms para cerca de 127 ms no cenário pesado.

A otimização demonstrou que uma parcela significativa da latência do
GerOndApp era causada por dados redundantes no payload, e não pelo
processamento numérico propriamente dito.

Mesmo após a redução, a resposta de aproximadamente 85 MB continua
muito grande, indicando que serialização, transferência, parsing e
renderização permanecem como os principais gargalos da aplicação.

###
 Etapa 2F.2B — Geração única do eixo de frequências

Após a Etapa 2F.2A, o GerOndApp já enviava apenas um único vetor
`xFreq` no payload.

Entretanto, a função `transformada_fourier()` ainda executava
`rfftfreq()` individualmente para cada um dos cinco sinais e novamente
para a resultante.

Como todos os sinais compartilham:

- a mesma taxa de amostragem;
- o mesmo número de amostras;
- a mesma duração;

o eixo de frequências é idêntico para todos eles.

A implementação foi então reorganizada para gerar `xFreq` uma única vez
por requisição.

A função `transformada_fourier()` passou a ter uma responsabilidade mais
específica:

- calcular `rfft`;
- normalizar a magnitude;
- retornar apenas o resultado espectral.

O eixo de frequências passou a ser gerado separadamente a partir de:

$$
N = \text{número de amostras}
$$


e:

$$
\Delta t = \frac{1}{F_s}
$$


Essa alteração não modifica o contrato da API nem o tamanho do payload.
Seu objetivo principal é eliminar cálculos redundantes, reduzir
alocações temporárias e melhorar a organização arquitetural do código.

### Resultados da Etapa 2F.2B

A geração do eixo de frequências foi removida da função
`transformada_fourier()` e passou a ocorrer uma única vez por requisição.

A mudança não alterou o formato da resposta da API e, portanto, não
produziu redução significativa do payload ou da latência de rede.

No cenário de 441.000 amostras, a mediana do tempo da FFT dos cinco sinais
caiu aproximadamente de 122,75 ms para 113,08 ms, uma redução próxima de
8%.

O tempo total da view caiu de aproximadamente 574,51 ms para 568,78 ms,
redução próxima de 1%.

A latência end-to-end permaneceu praticamente inalterada, em torno de
6,95 segundos, confirmando que o gargalo dominante continua associado ao
volume de dados serializados, transferidos, interpretados e renderizados.

Apesar do ganho modesto de desempenho, a alteração eliminou cálculos
redundantes e tornou explícita a existência de um único domínio de
frequências compartilhado entre todos os sinais.

## Etapa 3 - Downsampling (VISUALIZAÇÃO EFICIENTE NO FRONTEND)

O intuito dessa etapa é manter todo o sinal no backend e enviar apenas pontos importantes para representação do sinal no frontend, reduzindo efetivamente o custo para enviar dados ao front

A principal regra desta etapa é:

```
Os dados originais não serão reduzidos. Apenas a representação destinada ao gráfico será reduzida.
```

### 3.1 - O que é downsampling?

Downsampling consiste em **representar uma sequência utilizando uma quantidade menor de amostras.**

É medido uma nova amostra a cada $N$ pontos da amostragem original, esse $N$ representa o fator de redução da amostra.

- Se tivermos 441000 amostras a um fator de 100:

$$441000 \div{100} = 4410 \text{ pontos}$$

- Isso representa uma redução aproximada de:
$$90\%$$

Mas é importante destacar que o **downsampling não deve alterar o sinal original**

## Etapa 3A — Downsampling da representação temporal

Após a redução das redundâncias do payload, foi identificado que o
frontend continuava recebendo todas as amostras temporais dos sinais,
mesmo quando a resolução física do gráfico era muito inferior à quantidade
de pontos transmitidos.

Foi introduzido um limite de pontos destinados exclusivamente à
visualização.

Os sinais originais continuam sendo gerados e processados com resolução
completa. As FFTs e operações da resultante também continuam utilizando
os arrays originais.

Somente após os cálculos é criada uma representação reduzida para envio ao
frontend.

A estratégia inicial utiliza um stride dinâmico:

`passo = max(1, N // MAX_PONTOS_VISUALIZACAO)`

Sinais menores que o limite permanecem inalterados, enquanto sinais
maiores têm apenas sua representação visual reduzida.

### Resultados

Para 44.100 amostras, a quantidade de pontos temporais enviados caiu para
aproximadamente 5.513, redução de 87,5%.

Para 441.000 amostras, foram enviados aproximadamente 5.012 pontos,
redução de 98,86% na representação temporal.

No cenário de 441.000 amostras:

- o payload caiu aproximadamente de 85,36 MB para 32,56 MB;
- o tempo até os headers caiu aproximadamente 48%;
- o tempo de body + parsing caiu aproximadamente 58%;
- o tempo síncrono de atualização do Bokeh caiu aproximadamente 83%;
- a latência total mediana caiu aproximadamente de 6,95 s para 3,07 s.

O backend apresentou ganho menor, aproximadamente 12% no tempo total da
view, pois geração e FFT continuam sendo realizadas com resolução
completa.

Os resultados confirmam que uma parcela dominante da latência percebida
era causada pela transferência e renderização de uma quantidade de pontos
muito superior à resolução necessária para visualização.

### Limitação

O downsampling atual utiliza seleção por stride e pode deixar de preservar
picos ou eventos curtos entre as amostras selecionadas.

Por esse motivo, a implementação da Etapa 3A deve ser considerada uma
baseline de desempenho.

Uma estratégia posterior deverá preservar melhor extremos e características
visuais importantes, utilizando técnicas como agregação min/max por janela
ou níveis de detalhe adaptativos ao zoom.


### Resultado da Etapa 3B

A estratégia de downsampling temporal por stride foi substituída por uma
representação baseada nos valores mínimo e máximo de cada janela.

Cada sinal passou a possuir seu próprio eixo temporal reduzido, permitindo
preservar corretamente as posições dos extremos.

A implementação foi vetorizada com NumPy, utilizando reshape, argmin e
argmax por eixo, evitando loops Python sobre as janelas.

Nos testes com 441.000 amostras, o custo mediano do downsampling foi de
aproximadamente 2,16 ms, representando uma parcela muito pequena do tempo
total da view.

O backend permaneceu próximo de 100 ms no cenário pesado, enquanto a
latência frontend típica permaneceu próxima de 1 segundo no computador
de maior desempenho utilizado nos testes.

A mudança trouxe maior fidelidade visual sem sacrificar de forma
significativa os ganhos de performance obtidos na Etapa 3A.