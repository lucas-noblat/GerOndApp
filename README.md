# GerOndApp

O **GerOndApp** é uma aplicação web para **geração, manipulação e visualização de sinais** (senoidais, triangulares, quadrados, ruído branco). Projetado para ser utilizado em contexto educacional e de pesquisa, o sistema oferece uma interface interativa, permitindo ao usuário customizar sinais e analisá-los tanto no domínio do tempo quanto da frequência.

🌐 **Acesse o projeto através do site da ReNOMO (FURG) via domínio oficial:**
https://gerond.renomo.org.br

---

## 🚀 Funcionalidades Principais

- **Geração de Sinais Personalizados:**
  - Amplitude, frequência, fase, duração e offset configuráveis.
  - Duty cycle para sinais quadrados.
  - Faixa de frequência para ruído branco.

- **Visualização Gráfica Interativa (Bokeh):**
  - Plotagem de sinais no domínio do tempo e frequência.
  - Interface de configuração com atualização dinâmica.

- **Transformações de Sinais:**
  - Inserção de ruído branco.
  - Aplicação e visualização da Transformada de Fourier.
  - Operação (+, -, *, /) entre sinais ativos.

- **API RESTful** para manipulação dos dados de sinais.

---

## 🧰 Tecnologias Utilizadas

- **Backend:** Django 5.x, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript (Vanilla), BokehJS
- **Containerização:** Docker, Docker Compose, Gunicorn
- **Deploy:** NGINX (servidores ReNOMO)
- **Gerenciamento de Variáveis de Ambiente:** django-environ (.env)

---

## ⚙️ Como Executar Localmente

### Pré-requisitos
- Docker + Docker Compose instalados (https://docs.docker.com/get-docker/)
- Python 3.11+ (opcional, para rodar nativamente)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd GerOndApp/Django
```


### Passo 2: Crie o arquivo .env
Copie o arquivo de exemplo para .env:
cp dotenvfiles/.env-example.prod dotenvfiles/.env


Edite o arquivo .env conforme necessário:

```bash
SECRET_KEY=your-secret-key
ENVIRONMENT=development
ALLOWED_HOSTS=127.0.0.1,localhost
BASEHREF=gerond.renomo.org.br
PORT_APP=53900
```

### Passo 3: Build e Suba o Container
```bash
docker-compose build --no-cache
docker-compose up
```

Acesse no navegador:
```bash
http://127.0.0.1:53900
```

### Passo 4: Coletar Arquivos Estáticos (se necessário)
Se precisar forçar a coleta manual dos arquivos estáticos:
```bash
docker-compose run web python manage.py collectstatic --no-input
```

### Passo 5: Estrutura de Diretórios

```bash
GerOndApp/
├── Django/
│ ├── GerOndApp/
│ ├── home/
│ ├── staticfiles/ # Arquivos coletados (não versionar)
│ ├── templates/static/ # Arquivos estáticos (dev)
│ ├── dotenvfiles/.env
│ ├── Dockerfile
│ ├── docker-compose.yml
│ └── requirements.txt
└── README.md
```

## 🐳 Comandos Docker Úteis

### Gerenciamento de Containers
| Comando | Descrição |
|---------|-----------|
| `docker-compose up -d` | Inicia os containers em segundo plano |
| `docker-compose down` | Para e remove os containers |
| `docker-compose ps` | Lista containers em execução |
| `docker-compose logs -f` | Mostra logs em tempo real |

### Build e Rebuild
| Comando | Descrição |
|---------|-----------|
| `docker-compose build` | Build padrão das imagens |
| `docker-compose build --no-cache` | Força rebuild completo |

### Execução de Comandos
| Comando | Descrição |
|---------|-----------|
| `docker-compose exec web bash` | Acessa terminal do container |
| `docker-compose run web python manage.py [comando]` | Executa comandos Django |

### Limpeza
| Comando | Descrição |
|---------|-----------|
| `docker system prune` | Remove containers/redes não utilizadas |
| `docker volume prune` | Remove volumes não utilizados |

### Monitoramento
| Comando | Descrição |
|---------|-----------|
| `docker stats` | Monitora uso de recursos |
| `docker top [container]` | Mostra processos do container |

### ⚠️ Avisos Importantes
- NUNCA adicione seu arquivo .env a um repositório (ele está no .gitignore).

- A pasta staticfiles/ não deve ser versionada (ela será gerada em produção).

- Em produção, os arquivos estáticos serão servidos pelo NGINX da ReNOMO.

- A aplicação roda em ambiente containerizado via Gunicorn.

- O domínio oficial é: https://gerond.renomo.org.br

### 📄 Licença
Projeto desenvolvido pelo Laboratório de Instrumentação e Óptica (LIOc) - FURG.

### ✉️ Contato
Lucas de Alcantara Noblat – Desenvolvedor (lucasan@dcc.ufrj.br)

Everson Rodrigues (ReNOMO/FURG) – Orientador de Deploy e responsável pelos servidores da ReNOMO
