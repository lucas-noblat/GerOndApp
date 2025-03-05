# Documentação das Funções Backend - GerOndApp

O **GerOndApp** é uma aplicação para geração, visualização e manipulação de sinais no domínio do tempo e da frequência. Abaixo está a documentação de cada função disponível no código.

---

## 1. Funções de Visualização (Plotagem)

### 1.1. `plotar`
Plota um sinal no domínio do tempo usando a biblioteca Matplotlib.

#### Entradas:
- **`vetor_tempo`**: Vetor de tempo correspondente ao sinal (`numpy array`).
- **`sinal`**: Sinal a ser plotado (`numpy array`).
- **`nome`**: Título do gráfico (`string`).
- **`largura`**: Largura da figura em pixels (`int`, padrão: 1280).
- **`altura`**: Altura da figura em pixels (`int`, padrão: 720).
- **`legenda`**: Legenda do gráfico (`string`, opcional).
- **`salvar_como`**: Nome do arquivo para salvar o gráfico (`string`, opcional).

#### Saída:
Exibe o gráfico na tela e, se fornecido, salva o gráfico como uma imagem.

---

### 1.2. `plotar_sinais_bokeh`
Plota até 6 sinais em um único gráfico interativo usando a biblioteca Bokeh.

#### Entradas:
- **`vetor_x`**: Vetor de valores para o eixo x (tempo ou frequência, `numpy array`).
- **`lista_vetores_y`**: Lista de vetores de valores para o eixo y (amplitude ou magnitude, lista de `numpy arrays`).
- **`titulo`**: Título do gráfico (`string`, padrão: "Sinais").
- **`x_label`**: Rótulo do eixo x (`string`, padrão: "Tempo (s)").
- **`y_label`**: Rótulo do eixo y (`string`, padrão: "Amplitude").
- **`largura`**: Largura do gráfico em pixels (`int`, padrão: 1280).
- **`altura`**: Altura do gráfico em pixels (`int`, padrão: 400).
- **`is_spectrum`**: Se `True`, ajusta os limites do eixo x usando o Teorema de Nyquist (`bool`, padrão: `False`).

#### Saída:
Exibe um gráfico interativo no Jupyter Notebook ou em uma janela do navegador.

---

## 2. Funções Matemáticas para Criar Sinais

### 2.1. `sinal_senoidal`
Gera um sinal senoidal.

#### Entradas:
- **`amplitude`**: Amplitude do sinal (`float`).
- **`frequencia`**: Frequência do sinal em Hz (`float`).
- **`taxa_amostragem`**: Taxa de amostragem em amostras por segundo (`float`, padrão: 1000).
- **`duracao`**: Duração do sinal em segundos (`float`, padrão: 1).
- **`fase`**: Fase inicial do sinal em radianos (`float`, padrão: 0).
- **`offset`**: Deslocamento vertical do sinal (`float`, padrão: 0).

#### Saída:
- **`vetor_tempo`**: Vetor de tempo correspondente ao sinal (`numpy array`).
- **`s`**: Sinal senoidal gerado (`numpy array`).

---

### 2.2. `sinal_triangular`
Gera um sinal triangular.

#### Entradas:
- **`amplitude`**: Amplitude do sinal (`float`).
- **`frequencia`**: Frequência do sinal em Hz (`float`).
- **`taxa_amostragem`**: Taxa de amostragem em amostras por segundo (`float`, padrão: 1000).
- **`duracao`**: Duração do sinal em segundos (`float`, padrão: 1).
- **`fase`**: Fase inicial do sinal em radianos (`float`, padrão: 0).
- **`offset`**: Deslocamento vertical do sinal (`float`, padrão: 0).
- **`duty`**: Parâmetro que controla a forma do sinal triangular (`float`, padrão: 0).

#### Saída:
- **`vetor_tempo`**: Vetor de tempo correspondente ao sinal (`numpy array`).
- **`triangular`**: Sinal triangular gerado (`numpy array`).

---

### 2.3. `sinal_quadrado`
Gera um sinal quadrado.

#### Entradas:
- **`amplitude`**: Amplitude do sinal (`float`).
- **`frequencia`**: Frequência do sinal em Hz (`float`).
- **`taxa_amostragem`**: Taxa de amostragem em amostras por segundo (`float`, padrão: 1000).
- **`duracao`**: Duração do sinal em segundos (`float`, padrão: 1).
- **`fase`**: Fase inicial do sinal em radianos (`float`, padrão: 0).
- **`offset`**: Deslocamento vertical do sinal (`float`, padrão: 0).
- **`duty`**: Ciclo de trabalho do sinal quadrado (`float`, padrão: 0.5).

#### Saída:
- **`vetor_tempo`**: Vetor de tempo correspondente ao sinal (`numpy array`).
- **`sinal_quadrado`**: Sinal quadrado gerado (`numpy array`).

---

### 2.4. `ruido_branco`
Gera um ruído branco.

#### Entradas:
- **`amplitude`**: Amplitude do ruído (`float`).
- **`num_componentes`**: Número de componentes (amostras) no ruído (`int`).
- **`duracao`**: Duração do ruído em segundos (`float`, padrão: 1).
- **`offset`**: Deslocamento vertical do ruído (`float`, padrão: 0).
- **`freq_inicial`**: Frequência inicial (`float`, padrão: 0).
- **`freq_final`**: Frequência final (`float`, padrão: 0).

#### Saída:
- **`vetor_tempo`**: Vetor de tempo correspondente ao ruído (`numpy array`).
- **`ruido`**: Sinal de ruído branco gerado (`numpy array`).

---

## 3. Transformada de Fourier

### 3.1. `transformada_fourier`
Calcula a Transformada de Fourier de um sinal no domínio do tempo.

#### Entradas:
- **`vetor_tempo`**: Vetor de tempo correspondente ao sinal (`numpy array`).
- **`sinal`**: Sinal no domínio do tempo (`numpy array`).
- **`retornar_magnitude`**: Se `True`, retorna a magnitude. Se `False`, retorna os valores complexos (`bool`, padrão: `True`).

#### Saída:
- **`freqs`**: Vetor de frequências correspondente à Transformada de Fourier (`numpy array`).
- **`fft_resultado`**: Magnitude ou valores complexos da Transformada de Fourier (`numpy array`).

---

## 4. Função para Gerar Sinais

### 4.1. `gerar_sinal`
Gera um sinal com base no tipo especificado.

#### Entradas:
- **`tipo_sinal`**: Tipo de sinal a ser gerado (`string`, opções: 'a' para senoidal, 'b' para quadrado).
- **`amplitude`**: Amplitude do sinal (`float`).
- **`frequencia`**: Frequência do sinal em Hz (`float`).
- **`duracao`**: Duração do sinal em segundos (`float`).
- **`offset`**: Deslocamento vertical do sinal (`float`).

#### Saída:
- **`sinal_criado`**: Sinal gerado (`numpy array`).

---

## 5. Função para Aplicar Operações entre Séries

### 5.1. `aplicar_operacoes`
Aplica operações matemáticas entre séries de sinais ativas.

#### Entradas:
- **`series_ativas`**: Lista de séries de sinais (lista de `numpy arrays`).
- **`operacoes`**: Lista de operações a serem aplicadas (lista de `strings`, opções: '+', '-', '*', '/').

#### Saída:
- **`serie_resultante`**: Sinal resultante após as operações (`numpy array`).

---

## Considerações Finais
Este documento cobre todas as funções disponíveis no código do **GerOndApp**. Para mais detalhes ou dúvidas sobre a implementação, consulte o código fonte ou entre em contato. 😊
