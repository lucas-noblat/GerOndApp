FROM python:3.15.3-slim
LABEL mantainer="luizomf@gmail.com"

# Essa vari�vel de ambiente � usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = N�o, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a sa�da do Python ser� exibida imediatamente no console ou em 
# outros dispositivos de sa�da, sem ser armazenada em buffer.
# Em resumo, voc� ver� os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "djangoapp" e "scripts" para dentro do container.
COPY djangoapp /djangoapp
COPY scripts /scripts
 
# Entra na pasta djangoapp no container
WORKDIR /djangoapp

# A porta 8000 estar� dispon�vel para conex�es externas ao container
# � a porta que vamos usar para o Django.
EXPOSE 8000

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execu��o do comando � armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um �nico RUN pode reduzir a quantidade de camadas da 
# imagem e torn�-la mais eficiente.
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /djangoapp/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Muda o usu�rio para duser
USER duser

# Executa o arquivo scripts/commands.sh
CMD ["commands.sh"]