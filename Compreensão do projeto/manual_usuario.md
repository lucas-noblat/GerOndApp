# Manual do Usuário — GerOndApp

# 1. Introdução

Bem-vindo ao **GerOndApp**! Este aplicativo web foi desenvolvido para que você possa **criar, manipular e visualizar sinais** de forma interativa e didática.

Com ele, você pode:

- Gerar sinais básicos: **senoidal**, **quadrado**, **triangular** e **ruído branco**  
- Ajustar parâmetros como amplitude, frequência, fase, offset, duração e duty  
- Combinar vários sinais por meio de operações (soma, subtração, multiplicação, divisão) para obter uma **sinal resultante**  
- Visualizar o comportamento desse sinal no **domínio do tempo**  
- Calcular e exibir seu espectro de frequência usando a **Transformada de Fourier**  
- Interagir com os gráficos (zoom, panorâmica, salvar imagem etc)  
- Alternar entre sinais ativos ou inativos para focar no que deseja analisar  

Este manual foi criado para guiá-lo desde o uso mais básico até os recursos mais avançados, sem exigir conhecimentos técnicos profundos em processamento de sinais, mas com foco no que você precisa para usar o sistema com confiança.

---


# 2. Requisitos de sistema / ambiente

Para ter a melhor experiência usando o GerOndApp, verifique se seu ambiente atende as seguintes condições:

## 2.1 Navegador / dispositivo

- Use navegadores modernos e atualizados: **Google Chrome**, **Mozilla Firefox**, **Microsoft Edge** são recomendados.  
- O aplicativo é construído para roda no navegador — não requer instalação local.  
- Em dispositivos **móveis**, é exigido que o celular esteja em **modo horizontal** (paisagem); em modo vertical, aparece um aviso de rotação para melhor visualização.  
- É recomendado utilizar telas com dimensão mínima razoável — telas muito estreitas podem comprometer a legibilidade dos controles e gráficos.

## 2.2 Conexão com o backend / servidor

- O GerOndApp depende de comunicação com o servidor para gerar sinais e calcular transformadas — portanto, requer **conexão com internet** ou servidor backend ativo.  
- O servidor backend deve estar em funcionamento (API pronta para atender requisições) para que o frontend receba os dados e exiba os gráficos.

## 2.3 Recursos do sistema

- O sistema de gráficos (via Bokeh) faz uso de recursos de processamento e memória no navegador — computadores muito antigos ou dispositivos com pouca RAM podem apresentar lentidão com sinais muito complexos ou muitos sinais ao mesmo tempo.  
- Recomenda-se que o navegador não esteja com muitas abas pesadas abertas simultaneamente para evitar degradação do desempenho.

## 2.4 Cache / versões de arquivos estáticos

- Durante o uso e desenvolvimento, pode ser necessário **limpar o cache do navegador** (Ctrl+F5, aba anônima etc) para garantir que últimas versões de CSS/JS sejam carregadas.  
- Em ambientes de produção, o servidor deve estar configurado para servir corretamente os arquivos estáticos (CSS, JS) para evitar erros de carregamento.

---


# 3. Visão geral da interface

Nesta seção, você conhecerá os componentes visuais da aplicação e como navegar entre eles.

## 3.1 Layout principal

A interface é dividida em áreas funcionais:

- **Barra superior / cabeçalho**  
 Mostra logos dos patrocinadores e título da aplicação.  

- **Aba esquerda / lateral**  
  Contém as abas para configurações adicionais, seleção de unidades e parâmetros globais: por exemplo, duração geral do experimento, taxa de amostragem (rate).  

- **Área central do gráfico**  
  É onde são visualizados dois gráficos principais:  
  1. Gráfico do sinal no domínio do tempo  
  2. Gráfico do espectro de frequência (Transformada de Fourier)  

- **Aba direita (painel de entrada de sinais)**  
  Local em que você define os parâmetros dos sinais (Amplitude, Frequência etc), seleciona qual sinal está ativo, aplica operações, etc.

- **Controles dos sinais**  
  Botões para alternar entre S1, S2, S3, S4, S5.  
  Uma vez selecionado, os parâmetros desse sinal aparecem no painel para edição.

- **Área de interação gráfica**  
  Dentro dos gráficos: você pode interagir (zoom, pan, reset, salvar imagem) conforme funcionalidades do Bokeh habilitadas.

## 3.2 Fluxo de uso típico da interface

1. Abra a aba de entrada de sinais (direita).  
2. Clique em uma aba de sinal (S1, S2…) para selecioná-lo.  
3. Preencha ou ajuste os parâmetros do sinal.  
4. Escolha uma operação (soma, subtração, multiplicação etc) para combiná-lo com a resultante atual.  
5. O gráfico se atualiza para mostrar a onda no tempo e, automaticamente, o espectro de frequência.  
6. Use zoom / pan para inspecionar detalhes.  
7. Se desejar, exporte o gráfico ou reset à visualização original.

---

## 4. Operações de sinais (inserção / alteração)

### 4.1 O que é sinal

No contexto do GerOndApp, um *sinal* é uma função de tempo que pode ser senoidal, quadrada, triangular ou ruído branco.

### 4.2 Campos de configuração

| Campo | Significado | Observações |
|---|---|---|
| Amplitude | Máximo valor (altura) do sinal | ≥ 0 |
| Frequência | Quantos ciclos por segundo (Hz) | Valor real positivo |
| Duração | Tempo de simulação em segundos | valor real > 0 |
| Fase | Deslocamento inicial da onda | valor em graus ou radianos |
| Offset | Valor constante adicionado ao sinal | desloca para cima/baixo |
| Duty | Fração de tempo “alto” para sinais quadrados/triangulares | entre 0 e 1 |

### 4.3 Criar e editar sinais

- Para **criar** um sinal: selecione a aba correspondente (S1, S2, etc), preencha os campos, e envie para que ele apareça no gráfico.  
- Para **editar**: troque valores nos campos (Amplitude, Frequência etc) a aplicação atualizará o sinal automaticamente.  
- Para **ativar / desativar**: há controles para ocultar ou exibir cada sinal individualmente.  
- A **resultante** é obtida combinando os sinais segundo as operações definidas, porém ela é separada em 2 partes: o termo "soma e subtração".

### 4.4 Cálculo da resultante — dois termos

A resultante no GerOndApp é calculada da seguinte maneira:

- Há **cinco sinais** disponíveis para configuração.  
- Internamente, o sistema divide o cálculo da resultante usando **dois termos vetoriais**:

  1. **Termo aditivo** — recebe sinais configurados como **soma** ou **subtração**.  
     - Inicia como um vetor de **zeros**.  
     - Para cada sinal com operação *soma*, ele é somado ao termo aditivo.  
     - Para cada sinal com operação *subtração*, ele é subtraído do termo aditivo.  

  2. **Termo multiplicativo** — recebe sinais configurados como **multiplicação** ou **divisão**.  
     - Inicia como um vetor de **uns** (1), para que a multiplicação inicial não altere o valor.  
     - Cada sinal com operação *multiplicação* é multiplicado nesse termo.  
     - Cada sinal com operação *divisão* divide esse termo.

- Depois de calcular os dois termos, o vetor **resultante** é dado pela multiplicação elemento a elemento:

  > resultante = termo_aditivo × termo_multiplicativo

- Um caso especial: se **nenhum sinal** for marcado como soma ou subtração, o termo aditivo permanece zero para todas as posições.  
  Nesse caso:

  > resultante = 0 × (termo multiplicativo) = **vetor nulo (todos zeros)**

Portanto, para obter um resultado visível, **pelo menos um sinal deve estar configurado como soma ou subtração**. Se todos forem “nenhuma” ou apenas multiplicação/divisão, a resultante será zero.

---



## 5. Transformada de Fourier e espectro

### 5.1 O que é

A Transformada de Fourier transforma um sinal do domínio do tempo para o domínio da frequência, revelando quais frequências (componentes) compõem o sinal.  

### 5.2 Uso no GerOndApp

- Após gerar o sinal resultante no tempo, a aplicação calcula sua FFT (Transformada de Fourier Discreta).  
- Exibe um gráfico de magnitude por frequência (eixo x: frequência, eixo y: amplitude).  
- Permite identificar picos — frequências dominantes no sinal.

### 5.3 Limitações e cuidados

- Se a frequência do sinal for maior que metade da taxa de amostragem (teorema de Nyquist), ocorre **aliasing**.  
- A resolução em frequência depende do número de amostras (quanto mais amostras, melhor resolução).  
- Componentes muito próximos podem se mesclar se a janela de tempo for curta.

---

## 6. Interações com gráficos (Bokeh)

Você pode interagir diretamente com os gráficos Bokeh embutidos:

- **Zoom**: use scroll ou ferramentas de zoom da barra.  
- **Pan / mover**: arraste enquanto estiver no modo pan.  
- **Reset**: botão “reset” devolve ao estado original do gráfico.  
- **Salvar / exportar imagem**: botão de exportação — permite baixar o gráfico em formato de imagem (PNG etc).  
- **Seleção de sinais**: é possível ocultar ou destacar algumas linhas para analisar melhor.  

---

## 7. Exemplo passo a passo

1. Selecione **S1**, defina amplitude = 1.0, frequência = 5 Hz, duração = 1 s.  
2. Atualize qualquer parâmetro para gerar o novo sinal.  
3. Se desejar, ative **S2** e defina amplitude = 0.5, frequência = 10 Hz.  
4. Escolha operação “soma” em S1 e S2.  
5. Veja no gráfico de tempo a forma de onda resultante.  
6. Vá ao gráfico de frequência para ver os picos nas frequências 5 Hz e 10 Hz.  
7. Use zoom para ampliar um trecho do gráfico e salvar a imagem.

---

## 8. Erros, limites e advertências

- Frequência muito alta (acima de Nyquist) pode gerar distorções ou “aliasing”.  
- Se você definir *duração* muito curta, pode não haver resolução suficiente em frequência.  
- Valores extremos (ex: duty quase zero) podem causar comportamentos estranhos.  
- Se mudar CSS ou parâmetros, limpe o cache do navegador ou use versão atualizada dos arquivos estáticos.  
- Se o gráfico “desaparecer”, use botão de **reset** para voltar à visualização original.

---

## 9. Perguntas frequentes (FAQ)

**Por que o espectro aparece “liso” sem picos definidos?**  
 → Talvez não haja componentes suficientes ou o sinal foi definido com frequências muito próximas.

**Como recuperar o gráfico padrão?**  
 → Use o botão de reset na interface do Bokeh.

**Como forçar a aplicação de novas versões de CSS?**  
 → Limpe o cache do navegador (Ctrl+F5) ou carregue o site em aba anônima.  

---

## 10. Contato / versão / histórico

- [Versão atual do GerOndApp: v1.0](https://gerondapp.onrender.com)  
- [Repositório](https://github.com/lucas-noblat/GerOndApp) 
- Para dúvidas ou sugestões: lucasan@dcc.ufrj.br
- Histórico de versões (pequenas mudanças):  
  – v1.0: versão inicial com geração de sinais, FFT e interface  
  – v1.1: melhorias no gráfico interativo  
  – v1.2: ajustes de responsividade etc  

---

Você pode usar esse Markdown como base, colar no Docs, ajustar títulos e formatação, inserir imagens (prints) nos locais adequados (por exemplo na seção “Exemplo passo a passo” e “Visão da interface”).  
Quando quiser, posso preparar cada seção uma a uma com textos mais completos + imagens de exemplo. Vamos começar por qual seção você prefere expandir primeiro?
::contentReference[oaicite:0]{index=0}
