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


## Etapa 3B - Utilizando máximos e mínimos de janelas para realizar o downsampling

Nessa etapa queremos diminuir as incongruências observadas por um stride bruto. Pois o que está acontecendo e alguns casos é o fenômeno de **aliasing** em uns sinais, estamos perdendo muitas informações  inportantes

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
significativa os ganhos de performance obtidos na Etapa 3A.814.218 ms

## Etapa 3C - Downsampling no espectro de frequência

No domínio temporal, fazia sentido nós usarmos máximos e mínimos para redesenhar um sinal com menor resolução mas mantendo o visual. Porém no domínio da frequência, a preocupação é uma só:

```
No domínio do tempo, preservar mínimo e máximo por janela faz sentido visualmente.
No domínio da frequência, o mais importante é não perder picos espectrais.
```

Após a redução temporal das Etapas 3A e 3B, o maior volume restante no
payload passou a estar associado ao domínio da frequência.

Para um sinal com:

- taxa de amostragem: 44100 Hz;
- duração: 10 s;
- número de amostras: 441000;

a `rfft()` produz aproximadamente:

220501 bins de frequência

para cada sinal.

Como existem cinco sinais e uma resultante, o frontend recebe mais de um
milhão de valores de magnitude espectral, além do eixo de frequências.

Entretanto, um gráfico com poucos milhares de pixels não consegue
representar individualmente centenas de milhares de bins.

A Etapa 3C tem como objetivo criar uma representação espectral reduzida
destinada exclusivamente à visualização.

A FFT original continuará sendo calculada com resolução completa.

Somente a representação enviada ao frontend será reduzida.

Para isso utilizaremos a abordagem de máximo por janela, pois queremos preservar os picos de frequência de cada sinal

## Etapa 3C — Downsampling da representação espectral

Após as Etapas 3A e 3B, a representação temporal já estava limitada a
aproximadamente 5.000 pontos por sinal.

Entretanto, o domínio da frequência continuava sendo transmitido em
resolução completa.

Para um sinal de 44.100 Hz com duração de 10 segundos:

- amostras temporais: 441.000;
- bins produzidos pela rFFT: 220.501.

Foi implementado um downsampling espectral vetorizado.

O espectro é dividido em janelas e, para cada janela, é selecionado o
índice correspondente à maior magnitude através de `argmax`.

O mesmo índice é utilizado para recuperar a frequência correspondente,
preservando o par:

frequência <-> magnitude

A FFT continua sendo calculada utilizando todas as amostras originais.
A redução ocorre exclusivamente na representação destinada ao frontend.

### Redução

No cenário de 44.100 Hz × 10 s:

| Domínio | Original | Enviado | Redução |
|---|---:|---:|---:|
| Tempo | 441.000 | ~5.002 | 98,87% |
| Frequência | 220.501 | 5.000 | 97,73% |

### Benchmark backend

Para 44.100 Hz × 10 s:

| Métrica | Média | Mediana |
|---|---:|---:|
| Geração | 49,562 ms | 50,714 ms |
| Cálculo resultante | 0,531 ms | 0,492 ms |
| Downsampling temporal | 2,200 ms | 2,066 ms |
| Downsampling espectral | 1,083 ms | 1,096 ms |
| FFT | 26,645 ms | 26,134 ms |
| FFT resultante | 5,118 ms | 4,770 ms |
| TOTAL view | 91,286 ms | 92,309 ms |

O custo adicional do downsampling espectral ficou próximo de 1 ms,
demonstrando que a implementação vetorizada possui custo muito baixo em
relação à economia obtida posteriormente na serialização e visualização.

### Benchmark frontend

Para 44.100 Hz × 10 s:

| Métrica | Média | Mediana |
|---|---:|---:|
| Até headers | 169,00 ms | 170,50 ms |
| Body + JSON parse | 30,88 ms | 29,00 ms |
| TOTAL sendData | 199,88 ms | 203,00 ms |
| Bokeh | 18,25 ms | 15,50 ms |
| TOTAL atualizarAPI | 218,50 ms | 217,50 ms |

Em comparação com a Etapa 3B, cuja latência típica estava próxima de
955 ms, a Etapa 3C reduziu a latência end-to-end para aproximadamente
218 ms, redução próxima de 77%.

O payload do cenário pesado caiu de aproximadamente 33 MB para 4,5 MB,
representando redução próxima de 86%.

A redução do volume espectral teve impacto particularmente grande na
serialização, parsing do JSON e atualização do Bokeh.

### Pendências matemáticas

A implementação atual ainda não trata explicitamente:

- o bin DC (0 Hz);
- os bins restantes quando o número total de bins não é divisível pelo
  número de janelas.

Essas correções têm como objetivo principal aumentar a fidelidade
matemática da representação e não devem produzir ganho relevante de
performance.

### Resolvendo as pendências --- Finalização do downsampling no domínio da frequência

#### Objetivo

A Etapa 3C teve como objetivo reduzir a quantidade de pontos enviados ao
frontend no domínio da frequência sem perder os picos relevantes do
espectro.

Diferentemente do domínio do tempo, no qual foi utilizado o método
mínimo/máximo por janela, no espectro de frequência interessa
principalmente preservar o maior valor de magnitude existente em cada
região. Por isso foi criada a função `reduzir_freq_max()`.

A implementação divide o vetor de magnitudes em janelas e utiliza
`argmax(..., axis=1)` para localizar, de forma vetorizada com NumPy, o
índice do maior pico de cada janela. Os índices locais são convertidos
para índices absolutos do vetor original e usados para recuperar tanto a
frequência quanto sua magnitude correspondente.

------------------------------------------------------------------------

#### Tratamento da sobra da última janela

A divisão do espectro em janelas nem sempre utiliza exatamente todos os
pontos disponíveis.

O número de pontos processáveis pelas janelas completas é calculado por:

``` python
n_util = tam_janela * n_janelas
```

Quando:

``` python
n_util < n
```

existem amostras restantes no final do vetor. Ignorar essa região
significaria descartar uma parte do espectro e poderia eliminar um pico
relevante localizado justamente nas frequências finais.

Por isso, a sobra passou a ser analisada separadamente:

``` python
indices_max_sobra = n_util + argmax(magnitude_sem_dc[n_util:])
indices_max_abs = append(indices_max_abs, indices_max_sobra)
```

O `argmax()` encontra o maior valor dentro da região restante. Como esse
índice é local à sobra, soma-se `n_util` para obter sua posição absoluta
no vetor reduzido sem DC.

Assim, mesmo quando o tamanho do vetor não é divisível exatamente pelo
número de janelas, a região final do espectro continua representada.

##### Consequência visual

A sobra pode produzir uma ligação visual mais evidente no final do
gráfico, pois apenas o maior ponto dessa região é preservado e o Bokeh
conecta os pontos sucessivos com uma linha.

Esse comportamento é uma consequência da representação reduzida e não
caracteriza, por si só, erro no cálculo da FFT. Nesta etapa foi
priorizada a preservação da informação espectral relevante, sem
introduzir tratamento exclusivamente cosmético para essa ligação.

------------------------------------------------------------------------

#### Preservação explícita do componente DC

O primeiro elemento do espectro corresponde à frequência de `0 Hz`, isto
é, ao componente DC.

Como esse ponto possui significado matemático específico, ele não deve
competir com outras frequências dentro de uma janela de downsampling.
Caso fosse tratado como um ponto comum, um DC de grande magnitude
poderia fazer com que outro pico da primeira janela fosse descartado.

Por isso, o DC passou a ser separado antes da redução:

``` python
x_freq_dc = xFreq[0]
magnitude_dc = magnitude[0]

xFreq_sem_dc = xFreq[1:]
magnitude_sem_dc = magnitude[1:]
```

Como um ponto da capacidade máxima de saída passa a ser reservado ao DC:

``` python
n_janelas = max_pontos - 1
```

O downsampling é então realizado apenas sobre os vetores sem o
componente DC. Ao final, o DC é reinserido na primeira posição:

``` python
xFreqReduzido = insert(xFreqReduzido, 0, x_freq_dc)
magnitudeReduzida = insert(magnitudeReduzida, 0, magnitude_dc)
```

Dessa maneira, o componente de `0 Hz` é sempre preservado
explicitamente.

------------------------------------------------------------------------

#### Correção de inconsistência de índices após a remoção do DC

Durante a implementação do tratamento do DC foi identificado um erro
importante.

Após criar:

``` python
magnitude_sem_dc = magnitude[1:]
```

a matriz de blocos ainda estava sendo construída a partir do vetor
original:

``` python
mag_blocos = magnitude[:n_util].reshape(n_janelas, tam_janela)
```

Entretanto, os índices encontrados posteriormente eram aplicados sobre
`magnitude_sem_dc`.

Isso criava um deslocamento de uma posição entre o vetor usado pelo
`argmax()` e o vetor utilizado para recuperar as magnitudes e
frequências. Como consequência, em um teste com uma senoide pura de
`1 Hz`, o pico principal podia desaparecer do espectro reduzido.

A implementação correta passou a utilizar o mesmo vetor sem DC durante
todo o processo:

``` python
mag_blocos = magnitude_sem_dc[:n_util].reshape(
    n_janelas,
    tam_janela
)
```

O tratamento da sobra também foi mantido sobre `magnitude_sem_dc`,
garantindo consistência entre os índices calculados e os dados
recuperados.

Após essa correção, o pico esperado da senoide voltou a aparecer
corretamente em sua frequência correspondente.

------------------------------------------------------------------------

#### Validação matemática

Um dos testes utilizados foi uma senoide aproximadamente nas seguintes
condições:

``` text
Forma:       Senoidal
Amplitude:   1
Frequência:  1 Hz
Fase:        0°
Offset:      0
Duração:     1 s
Rate:        41000 Hz
```

Com `41000` amostras em `1 s`, a resolução em frequência é:

``` text
Δf = rate / N
Δf = 41000 / 41000
Δf = 1 Hz
```

Portanto, era esperado que o espectro apresentasse seu pico principal
exatamente em `1 Hz`.

Após a correção da inconsistência de índices, esse comportamento foi
recuperado.

O limite superior do espectro aparece próximo de `20500 Hz`, o que
também está de acordo com a frequência de Nyquist:

``` text
f_Nyquist = rate / 2
f_Nyquist = 41000 / 2
f_Nyquist = 20500 Hz
```

Esses testes ajudaram a confirmar a coerência matemática da
implementação.

------------------------------------------------------------------------

#### Resíduos numéricos próximos de zero

Mesmo para uma senoide matematicamente pura, a FFT pode apresentar
magnitudes extremamente pequenas em frequências que teoricamente
deveriam possuir magnitude zero, por exemplo valores da ordem de:

``` text
10^-16
10^-17
10^-18
```

Esses valores são resíduos decorrentes da representação numérica em
ponto flutuante e não representam componentes espectrais fisicamente
significativos.

Foi decidido não aplicar um limiar artificial para zerá-los.

Essa escolha mantém o resultado numérico produzido pelo cálculo e evita
adicionar uma etapa puramente cosmética ao processamento. Para os
objetivos atuais do GerOndApp, esses valores podem ser considerados
praticamente zero.

------------------------------------------------------------------------

## Estado final da Etapa 3C

Ao final da etapa, o downsampling do espectro passou a possuir:

-   preservação do maior pico de cada janela;
-   processamento vetorizado utilizando NumPy;
-   tratamento da região restante quando o vetor não é perfeitamente
    divisível;
-   preservação explícita do componente DC;
-   consistência entre os índices calculados e os vetores sem DC;
-   preservação dos pares frequência/magnitude correspondentes;
-   manutenção dos resíduos naturais de ponto flutuante sem tratamento
    cosmético.

Com isso, a **Etapa 3C pode ser considerada concluída**.

------------------------------------------------------------------------

## Sobre a necessidade de um novo benchmark

As alterações finais da Etapa 3C foram predominantemente de **corretude
matemática**, especialmente:

1.  inclusão da sobra da última janela;
2.  separação e reinserção do componente DC;
3.  correção da referência de `magnitude` para `magnitude_sem_dc`.

Essas mudanças não alteram a arquitetura de desempenho estabelecida
anteriormente. O processamento continua baseado em operações vetorizadas
do NumPy, e as operações adicionais envolvem apenas uma pequena região
de sobra, a preservação de um único ponto DC e ajustes de indexação.

Por esse motivo, **não é necessário repetir toda a bateria formal de
benchmarks da Fase 3 apenas para validar essas correções**. Os
benchmarks anteriores continuam representativos da mudança de desempenho
obtida pelo downsampling.

Um teste de desempenho adicional poderia ser executado futuramente como
validação final ou regressão antes do deploy, mas não é necessário
tratá-lo como um novo marco de otimização.

O principal critério de conclusão desta parte foi a corretude do
espectro após a redução.

------------------------------------------------------------------------

## Resultado geral da Fase 3

Com a conclusão da Etapa 3C, o GerOndApp passa a manter os vetores
completos no backend para os cálculos necessários, enquanto envia ao
frontend representações reduzidas apropriadas para visualização.

No domínio do tempo:

``` text
vetor completo
      ↓
janelas
      ↓
mínimo + máximo
      ↓
representação visual reduzida
```

No domínio da frequência:

``` text
FFT completa
      ↓
preservação do DC
      ↓
janelas
      ↓
maior magnitude
      ↓
tratamento da sobra
      ↓
representação espectral reduzida
```

Essa separação permite que o backend continue trabalhando com a
resolução necessária para os cálculos enquanto o frontend recebe somente
a quantidade de dados necessária para uma representação visual útil.

Além de melhorar o comportamento da aplicação com sinais de alta taxa de
amostragem e longa duração, essa arquitetura prepara o GerOndApp para
uma próxima etapa importante: trabalhar com sinais externos e sinais
reais, como arquivos WAV, sem exigir que todas as amostras sejam
transferidas e renderizadas diretamente pelo navegador.


## Observação adicional --- Influência do hardware nos benchmarks

Durante os testes de desempenho do GerOndApp, a mesma versão da
aplicação foi executada em dois computadores com capacidades de
processamento bastante diferentes. Essa comparação foi útil para separar
ganhos obtidos pela arquitetura do software daqueles decorrentes apenas
de hardware mais potente.

### Cenário analisado

O principal cenário utilizado para comparação foi:

-   Taxa de amostragem: `44.100 Hz`
-   Duração: `10 s`
-   Amostras temporais: `441.000`
-   Pontos temporais enviados ao frontend: `~5.000`
-   Bins da FFT original: `220.501`
-   Pontos espectrais enviados ao frontend: `~5.000`

Ou seja, a lógica executada foi a mesma nos dois computadores. A
diferença observada veio essencialmente da capacidade de processamento
de cada máquina.

### Comparação do backend

No computador de maior desempenho utilizado na faculdade, o backend
apresentou aproximadamente:

|  Métrica             |   PC da faculdade
| -------------------- |-----------------
| TOTAL view           |         \~92 ms
| Geração dos sinais   |          \~51 ms
| FFT dos sinais       |          \~26 ms
| FFT da resultante    |           \~5 ms

No computador pessoal utilizado como ambiente de desenvolvimento mais
limitado:

|Métrica                |PC pessoal
|  -------------------- |------------
|  TOTAL view           |     \~476 ms
|  Geração dos sinais   |     \~296 ms
|  FFT dos sinais       |     \~122 ms
|  FFT da resultante    |     \~25 ms

Dessa forma, para o cenário de `44.100 Hz × 10 s`, o backend do
computador pessoal apresentou tempo aproximadamente:

`476 / 92 ≈ 5,2 vezes maior`

Isso mostra que, após as otimizações de redução de dados, o desempenho
do backend passou a depender muito mais diretamente da capacidade de CPU
para geração dos sinais e execução das FFTs.

### Comparação end-to-end

Também foi medida a latência percebida pelo usuário, incluindo backend,
serialização, transferência, parsing do JSON e atualização dos gráficos
Bokeh.

No computador da faculdade:

  |Métrica                  |  Valor típico
  |------------------------ |--------------
  |Backend                  |       \~92 ms
  |Até receber os headers   |      \~170 ms
  |TOTAL sendData           |      \~203 ms
  |Bokeh                    |     \~15,5 ms
  |TOTAL atualizarAPI       |      \~218 ms

No computador pessoal:

  |Métrica                  |  Valor típico
  |------------------------ |--------------
  |Backend                  |      \~476 ms
  |Até receber os headers   |      \~602 ms
  |TOTAL sendData           |      \~619 ms
  |Bokeh                    |       \~29 ms
  |TOTAL atualizarAPI       |      \~648 ms

Portanto, enquanto o backend foi aproximadamente `5,2×` mais lento no
computador pessoal, a experiência completa percebida pelo usuário foi
aproximadamente:

`648 / 218 ≈ 3× mais lenta`

Isso ocorre porque nem todas as etapas dependem igualmente da CPU. O
cálculo numérico apresenta grande diferença entre as máquinas, enquanto
etapas como parsing do JSON, gerenciamento da resposta HTTP e
atualização do Bokeh ficaram relativamente próximas após a redução do
payload.

### Interpretação

Essa comparação revelou uma mudança importante no perfil de desempenho
do GerOndApp.

Antes das otimizações, grande parte da latência era causada por
desperdícios arquiteturais, como:

-   múltiplas requisições para uma única alteração;
-   envio repetido de eixos idênticos;
-   serialização de arrays completos;
-   envio de centenas de milhares de pontos ao navegador;
-   atualização do Bokeh com resolução muito superior à necessária para
    visualização.

Após as Etapas 3A, 3B e 3C, esses gargalos foram fortemente reduzidos.

No cenário atual, o pipeline se aproxima de:

``` text
Gerar os sinais completos
        ↓
Executar FFTs completas
        ↓
Calcular a resultante
        ↓
Reduzir apenas a representação visual
        ↓
Serializar poucos milhares de pontos
        ↓
Enviar ao frontend
        ↓
Atualizar o Bokeh
```

Dessa forma, o custo principal voltou a estar associado a operações
matemáticas legítimas, principalmente:

-   geração dos sinais;
-   cálculo das FFTs dos sinais;
-   cálculo da resultante;
-   FFT da resultante.

Isso é um resultado positivo, pois indica que uma parcela considerável
do overhead evitável da aplicação já foi removida. O tempo de
processamento agora está muito mais relacionado ao trabalho matemático
que o GerOndApp realmente precisa executar.

### Papel dos dois computadores nos testes

Os dois ambientes passaram a cumprir papéis complementares durante o
desenvolvimento.

O computador de maior desempenho, utilizado na faculdade, funciona como
uma referência do potencial da arquitetura quando executada em hardware
mais potente.

Já o computador pessoal, significativamente mais limitado em capacidade
de processamento, funciona como uma espécie de cenário de estresse ou
"pior caso" para os testes de desempenho.

Isso permite avaliar duas perguntas diferentes:

> "Qual desempenho o GerOndApp consegue atingir em uma máquina mais
> potente?"

e:

> "A aplicação continua responsiva quando executada em hardware mais
> limitado?"

No cenário de `44.100 Hz × 10 s`, correspondente a `441.000` amostras
temporais, foram observados aproximadamente:

  Ambiente             Backend   Tempo total percebido
  ----------------- ---------- -----------------------
  PC da faculdade      \~92 ms                \~218 ms
  PC pessoal          \~476 ms                \~648 ms

Portanto, o backend chegou a apresentar uma diferença de
aproximadamente:

`476 / 92 ≈ 5,2×`

entre as duas máquinas.

Entretanto, mesmo no computador mais limitado, todo o ciclo de
atualização da aplicação permaneceu abaixo de aproximadamente `0,7 s`
nesse cenário.

Isso é especialmente relevante porque o teste envolve não apenas a
geração de `441.000` amostras, mas também o processamento dos cinco
sinais, cálculo da resultante, execução das FFTs, downsampling e
preparação dos dados que serão enviados ao navegador.

### O hardware passou a evidenciar os gargalos matemáticos

A diferença entre os computadores também ajuda a identificar quais
partes da aplicação são mais sensíveis ao hardware.

No computador pessoal, para `44.100 Hz × 10 s`, os maiores custos
observados foram aproximadamente:

``` text
Geração dos sinais:      ~296 ms
FFT dos sinais:          ~122 ms
FFT da resultante:        ~25 ms
Downsampling temporal:    ~10 ms
Downsampling espectral:   ~3,5 ms
```

Isso mostra que o downsampling introduzido nas Etapas 3B e 3C possui um
custo relativamente pequeno quando comparado ao processamento matemático
completo.

Em outras palavras, gastar alguns milissegundos reduzindo os dados antes
de enviá-los ao frontend proporciona uma economia muito maior
posteriormente, principalmente na serialização, transferência, parsing
do JSON e atualização dos gráficos.

### Impacto das Etapas 3B e 3C

A estratégia adotada passou a separar duas necessidades diferentes:

1.  **Precisão matemática**
2.  **Resolução necessária para visualização**

Os sinais continuam sendo gerados e processados em sua resolução
original no backend.

Por exemplo:

``` text
Rate = 44.100 Hz
Duração = 10 s

441.000 amostras
        ↓
Processamento matemático completo
        ↓
Resultante
        ↓
FFT completa
```

Somente depois desses cálculos ocorre a redução destinada à
visualização:

``` text
DOMÍNIO DO TEMPO

441.000 pontos
        ↓
Downsampling Min/Max
        ↓
~5.000 pontos


DOMÍNIO DA FREQUÊNCIA

220.501 bins
        ↓
Downsampling por máximos
        ↓
~5.000 pontos
```

Assim, o frontend deixa de receber centenas de milhares de pontos que
não possuem utilidade prática para a resolução visual disponível,
enquanto o backend continua mantendo a resolução necessária para os
cálculos.

### Consequência arquitetural

Essa abordagem estabelece uma separação importante no GerOndApp:

``` text
BACKEND
Dados completos
NumPy
Processamento matemático
FFT
Operações entre sinais
        ↓
Redução para visualização
        ↓
FRONTEND
Apenas os dados necessários
para representação gráfica
```

Essa separação será particularmente importante para a futura
implementação da importação de sinais reais, como arquivos WAV.

Um áudio poderá possuir centenas de milhares ou até milhões de amostras.
Não é necessário enviar todas essas amostras ao navegador simplesmente
para desenhar sua forma de onda.

O backend poderá preservar o sinal original para processamento e
análise, enquanto o frontend recebe uma representação reduzida adequada
à visualização.

### Conclusão

Os testes em computadores diferentes foram importantes para demonstrar
que os ganhos obtidos são predominantemente arquiteturais e permanecem
válidos em ambientes com capacidades distintas.

O hardware influencia fortemente o tempo das operações matemáticas,
especialmente geração de sinais e FFT, mas os principais gargalos
relacionados a transporte, serialização e visualização foram
substancialmente reduzidos.

Após as Etapas 3B e 3C, os principais custos deixaram de estar
relacionados ao transporte e à renderização de quantidades excessivas de
dados e passaram a estar concentrados principalmente nas operações
matemáticas necessárias à aplicação.

Isso representa uma mudança importante no perfil de desempenho do
projeto.

O computador mais potente permite observar o potencial da arquitetura,
enquanto o computador pessoal funciona como um ambiente útil de teste de
estresse e de validação da responsividade em hardware mais modesto.

A arquitetura atual também estabelece uma base importante para as
próximas funcionalidades do GerOndApp, especialmente a entrada e análise
de sinais reais: **os dados completos permanecem no backend para
processamento, enquanto apenas a quantidade necessária para visualização
é enviada ao frontend.**
