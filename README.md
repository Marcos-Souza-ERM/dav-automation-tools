# DAV Automation Tools

Ambiente Docker padronizado para desenvolvimento de projetos Python, com o objetivo de **reduzir o tempo de configuração de novos integrantes da equipe**.

Este projeto fornece uma imagem Docker com as principais dependências e ferramentas necessárias para os projetos da equipe. Dessa forma, um novo integrante não precisa realizar manualmente a instalação de Python, Java, Node.js, Tesseract, PostgreSQL Client e outras ferramentas.

A configuração é integrada ao **VS Code Dev Containers**, permitindo que o ambiente de desenvolvimento seja iniciado diretamente dentro do projeto que está sendo desenvolvido.

---

## 🎯 Objetivo

O objetivo deste projeto é padronizar e simplificar a criação de ambientes de desenvolvimento.

Sem este projeto, a entrada de um novo integrante pode exigir:

* Instalação e configuração do Python;
* Instalação do Java;
* Instalação do Node.js;
* Instalação do Tesseract OCR;
* Instalação do PostgreSQL Client;
* Configuração de variáveis de ambiente;
* Instalação manual das dependências Python;
* Configurações específicas do VS Code;
* Ajustes diferentes entre máquinas.

Com o `dav-automation-tools`, a ideia é que o integrante precise apenas:

1. Ter o Git instalado;
2. Ter o Docker instalado e em execução;
3. Ter o VS Code instalado;
4. Instalar a extensão **Dev Containers**;
5. Clonar este repositório;
6. Configurar o `.devcontainer` no projeto que deseja executar;
7. Abrir o projeto no Dev Container.

O restante do ambiente é criado automaticamente pelo Docker.

---

# 🏗️ Arquitetura

O projeto funciona como uma **imagem base de desenvolvimento compartilhada**.

O fluxo é:

```text
Projeto do desenvolvedor
        │
        │ .devcontainer/devcontainer.json
        │
        ▼
docker-compose.yml
        │
        │ build
        ▼
dav-automation-tools
        │
        │ Dockerfile
        ▼
Imagem Docker de desenvolvimento
        │
        ├── Python 3.13
        ├── Java 17
        ├── Node.js 22
        ├── Tesseract OCR
        ├── PostgreSQL Client
        ├── Git
        ├── Curl
        └── Outras ferramentas do ambiente
```

O projeto que está sendo desenvolvido continua responsável pelas suas próprias dependências Python.

Por exemplo:

```text
Projeto A
├── requirements.txt
└── .devcontainer/
    ├── docker-compose.yml
    ├── docker.env
    └── devcontainer.json
```

Ao executar o Dev Container, o comando:

```json
"postCreateCommand": "pip install --no-cache-dir -r /workspace/requirements.txt"
```

instala automaticamente as dependências específicas daquele projeto.

---

# 📁 Estrutura do repositório

Este repositório possui atualmente a seguinte estrutura:

```text
dav-automation-tools/
├── saida_imagens/
├── saida_texto/
├── Dockerfile
├── ocr_pdf.py
└── README.md
```

## Principais arquivos

### `Dockerfile`

Define a imagem base utilizada pelos projetos.

A imagem atualmente utiliza:

```dockerfile
FROM python:3.13-slim-bookworm
```

Além do Python, são instaladas ferramentas utilizadas pelos projetos da equipe.

### `ocr_pdf.py`

Exemplo de utilização do ambiente para processamento de documentos PDF utilizando OCR.

O script:

1. Abre um arquivo PDF;
2. Processa cada página;
3. Converte cada página do PDF em uma imagem;
4. Salva as imagens em `saida_imagens/`;
5. Executa OCR utilizando PaddleOCR;
6. Extrai os textos encontrados;
7. Salva o resultado em `saida_texto/resultado.txt`.

### `saida_imagens/`

Diretório utilizado pelo exemplo de OCR para armazenar as imagens geradas a partir das páginas do PDF.

### `saida_texto/`

Diretório utilizado para armazenar os resultados textuais gerados pelo OCR.

---

# 🐳 Conteúdo da imagem Docker

O `Dockerfile` instala as principais ferramentas necessárias ao ambiente:

| Componente          | Versão / Origem     |
| ------------------- | ------------------- |
| Python              | 3.13                |
| Java                | OpenJDK 17          |
| Node.js             | 22                  |
| Git                 | Sistema operacional |
| Curl                | Sistema operacional |
| PostgreSQL Client   | Sistema operacional |
| Tesseract OCR       | Sistema operacional |
| Tesseract Português | `tesseract-ocr-por` |

A imagem também configura:

```text
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
PYTHONUNBUFFERED=1
WORKDIR=/workspace
```

O container permanece em execução utilizando:

```dockerfile
CMD ["sleep", "infinity"]
```

Isso permite que o VS Code Dev Containers mantenha o ambiente disponível para desenvolvimento.

---

# 🚀 Como utilizar em um novo projeto

## 1. Pré-requisitos

O computador do desenvolvedor precisa ter:

* Git;
* Docker;
* Visual Studio Code;
* Extensão **Dev Containers** do VS Code.

O Docker precisa estar instalado e funcionando antes de abrir o Dev Container.

---

## 2. Clone o `dav-automation-tools`

O repositório precisa ser clonado em uma posição compatível com o `docker-compose.yml`.

Exemplo:

```text
workspace/
├── dav-automation-tools/
│   ├── Dockerfile
│   ├── ocr_pdf.py
│   └── README.md
│
└── projeto-a/
    ├── requirements.txt
    ├── codigo.py
    └── .devcontainer/
        ├── docker-compose.yml
        ├── docker.env
        └── devcontainer.json
```

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO> dav-automation-tools
```

> Substitua `<URL_DO_REPOSITORIO>` pela URL oficial do repositório.

---

# 📂 Estrutura necessária no projeto

Todo projeto que utilizar o ambiente deverá possuir um diretório `.devcontainer`.

A estrutura esperada é:

```text
projeto-a/
├── requirements.txt
├── ...
└── .devcontainer/
    ├── docker-compose.yml
    ├── docker.env
    └── devcontainer.json
```

O arquivo `docker-compose.yml` deve utilizar o `dav-automation-tools` como contexto de build.

---

# ⚙️ Configuração do `docker-compose.yml`

O `docker-compose.yml` utilizado atualmente deve permanecer conforme a configuração abaixo:

```yaml
services:
  app:
    build:
      context: ../../dav-automation-tools
      dockerfile: Dockerfile

    working_dir: /workspace

    volumes:
      - ..:/workspace

    env_file:
      - ./docker.env

    environment:
      TZ: America/Sao_Paulo
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432

    depends_on:
      postgres:
        condition: service_healthy

    stdin_open: true
    tty: true

  postgres:
    image: postgres:17

    env_file:
      - ./docker.env

    environment:
      TZ: America/Sao_Paulo

    volumes:
      - postgres_data:/var/lib/postgresql/data

    healthcheck:
      test:
        [
          "CMD-SHELL",
          "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_NAME_DATABASE}"
        ]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  postgres_data:
```

### ⚠️ Importante

O seguinte trecho:

```yaml
context: ../../dav-automation-tools
```

faz referência ao diretório onde o repositório `dav-automation-tools` foi clonado.

Por isso, a estrutura de diretórios precisa ser compatível com:

```text
workspace/
├── dav-automation-tools/
└── projeto-a/
    └── .devcontainer/
        └── docker-compose.yml
```

Se o repositório estiver em outro local, o `context` precisará ser ajustado.

---

# 🔐 Configuração do `docker.env`

Cada projeto pode possuir seu próprio arquivo `.devcontainer/docker.env`.

Exemplo:

```env
POSTGRES_DB=nome-do-db

POSTGRES_NAME_DATABASE=nome-do-schema

POSTGRES_USER=postgres

POSTGRES_PASSWORD=senhaAqui
```

Essas variáveis são utilizadas pelo container da aplicação e pelo PostgreSQL.

### ⚠️ Segurança

O arquivo `docker.env` pode conter credenciais e informações sensíveis.

Recomenda-se **não versionar senhas reais no Git**.

Uma alternativa é manter um arquivo de exemplo:

```text
.devcontainer/
├── docker-compose.yml
├── docker.env
├── docker.env.example
└── devcontainer.json
```

Exemplo:

```env
POSTGRES_DB=nome_do_banco
POSTGRES_NAME_DATABASE=nome_do_banco
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha
```

---

# 🧩 Configuração do `devcontainer.json`

O `devcontainer.json` é responsável por informar ao VS Code como o ambiente deve ser iniciado.

Exemplo:

```json
{
    "name": "Nome do Projeto - Python",

    "dockerComposeFile": [
        "docker-compose.yml"
    ],

    "service": "app",

    "workspaceFolder": "/workspace",

    "postCreateCommand": "pip install --no-cache-dir -r /workspace/requirements.txt",

    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance"
            ],
            "settings": {
                "python.defaultInterpreterPath": "/usr/local/bin/python"
            }
        }
    },

    "remoteUser": "root"
}
```

---

# 📦 Dependências Python

As dependências específicas de cada projeto devem ser declaradas no `requirements.txt` do próprio projeto.

Exemplo:

```text
projeto-a/
├── requirements.txt
├── src/
└── .devcontainer/
```

Quando o Dev Container for criado, o comando abaixo será executado automaticamente:

```bash
pip install --no-cache-dir -r /workspace/requirements.txt
```

Isso permite que diferentes projetos utilizem a mesma imagem base, mas tenham dependências Python diferentes.

Por exemplo:

```text
Projeto A
    └── requirements.txt
        ├── pandas
        ├── pyspark
        └── paddleocr

Projeto B
    └── requirements.txt
        ├── fastapi
        ├── sqlalchemy
        └── requests
```

Ambos podem utilizar o mesmo `dav-automation-tools`.

---

# ▶️ Abrindo o projeto no Dev Container

Depois de configurar os arquivos:

1. Abra o projeto no VS Code;
2. Certifique-se de que a extensão **Dev Containers** está instalada;
3. Pressione `Ctrl + Shift + P`;
4. Execute:

```text
Dev Containers: Reopen in Container
```

O VS Code irá:

1. Ler o `devcontainer.json`;
2. Executar o `docker-compose.yml`;
3. Fazer o build da imagem utilizando o `dav-automation-tools`;
4. Criar o container da aplicação;
5. Criar o container PostgreSQL;
6. Aguardar o PostgreSQL ficar saudável;
7. Montar o projeto em `/workspace`;
8. Instalar as extensões configuradas;
9. Executar o `postCreateCommand`;
10. Instalar as dependências do `requirements.txt`.

Após a conclusão, o desenvolvimento acontece dentro do container.

---

# 🗄️ PostgreSQL

O ambiente também disponibiliza um container PostgreSQL.

O serviço possui:

```yaml
image: postgres:17
```

A aplicação pode acessar o banco utilizando:

```text
Host: postgres
Port: 5432
```

Esses valores são configurados automaticamente pelo `docker-compose.yml`:

```yaml
environment:
  POSTGRES_HOST: postgres
  POSTGRES_PORT: 5432
```

O banco utiliza um volume Docker:

```text
postgres_data
```

Isso permite que os dados do PostgreSQL sejam persistidos mesmo quando o container da aplicação é recriado.

---

# 🔍 Exemplo de OCR

O projeto contém um exemplo de processamento de PDF utilizando:

* PyMuPDF (`fitz`);
* PaddleOCR;
* Tesseract OCR;
* Python.

O arquivo de entrada utilizado atualmente pelo script é:

```text
Teste-de-OCR-Exemplo.pdf
```

O script espera encontrar esse arquivo no diretório de trabalho:

```text
/workspace
```

A execução pode ser feita com:

```bash
python ocr_pdf.py
```

Durante a execução, cada página do PDF é convertida em uma imagem e processada pelo OCR.

A estrutura de saída será:

```text
projeto/
├── Teste-de-OCR-Exemplo.pdf
├── ocr_pdf.py
├── saida_imagens/
│   ├── pagina_1.png
│   ├── ...
│   
│
└── saida_texto/
    └── resultado.txt
```

O arquivo:

```text
saida_texto/resultado.txt
```

contém o texto reconhecido pelo OCR.

---

# 🛠️ Solução de problemas

## O VS Code não consegue criar o container

Verifique se o Docker está instalado e em execução:

```bash
docker --version
```

Depois:

```bash
docker ps
```

Se o Docker não estiver disponível, inicie o Docker antes de abrir o Dev Container.

---

## Erro relacionado ao `dav-automation-tools`

Verifique se a estrutura dos diretórios está correta:

```text
workspace/
├── dav-automation-tools/
│   └── Dockerfile
│
└── projeto-a/
    └── .devcontainer/
        └── docker-compose.yml
```

O `docker-compose.yml` utiliza:

```yaml
context: ../../dav-automation-tools
```

Portanto, o Docker precisa conseguir encontrar o `Dockerfile` nesse caminho.

---

## O `requirements.txt` não foi encontrado

Verifique se o projeto possui:

```text
projeto-a/
├── requirements.txt
└── .devcontainer/
    └── devcontainer.json
```

O `devcontainer.json` executa:

```bash
pip install --no-cache-dir -r /workspace/requirements.txt
```

---

## O PostgreSQL não inicia

Verifique os valores do:

```text
.devcontainer/docker.env
```

Principalmente:

```env
POSTGRES_DB=
POSTGRES_NAME_DATABASE=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

O healthcheck do PostgreSQL utiliza `POSTGRES_USER` e `POSTGRES_NAME_DATABASE`.

---

## Quero reconstruir a imagem

Quando houver alterações no `Dockerfile`, pode ser necessário reconstruir o container.

No VS Code:

```text
Ctrl + Shift + P
```

Depois execute:

```text
Dev Containers: Rebuild Container
```

---

# 🔄 Fluxo para novos integrantes

O fluxo esperado para um novo integrante é:

```text
1. Instalar Git
        ↓
2. Instalar Docker
        ↓
3. Instalar VS Code
        ↓
4. Instalar extensão Dev Containers
        ↓
5. Clonar dav-automation-tools
        ↓
6. Clonar o projeto da equipe
        ↓
7. Configurar .devcontainer
        ↓
8. Abrir o projeto no VS Code
        ↓
9. "Reopen in Container"
        ↓
10. Docker cria o ambiente
        ↓
11. Dependências Python são instaladas
        ↓
12. Ambiente pronto para desenvolvimento
```

---

# 💡 Conceito do projeto

O principal objetivo do `dav-automation-tools` não é armazenar o código específico de cada aplicação.

Ele funciona como uma **base de ambiente de desenvolvimento compartilhada**.

A separação de responsabilidades é:

```text
dav-automation-tools
        │
        ├── Sistema operacional
        ├── Python
        ├── Java
        ├── Node.js
        ├── Tesseract
        ├── PostgreSQL Client
        └── Ferramentas comuns
                 │
                 ▼
        ┌─────────────────────┐
        │       Projeto A      │
        │ requirements.txt     │
        └─────────────────────┘

                 │
                 ▼

        ┌─────────────────────┐
        │       Projeto B      │
        │ requirements.txt     │
        └─────────────────────┘

                 │
                 ▼

        ┌─────────────────────┐
        │       Projeto C      │
        │ requirements.txt     │
        └─────────────────────┘
```

Dessa forma, a equipe consegue manter uma base de desenvolvimento consistente entre diferentes projetos, reduzindo o tempo necessário para preparar uma nova máquina.

---

# 📌 Convenções recomendadas

Para novos projetos que utilizarem este ambiente, recomenda-se manter:

```text
projeto/
├── requirements.txt
├── código da aplicação
└── .devcontainer/
    ├── docker-compose.yml
    ├── docker.env
    └── devcontainer.json
```

O `docker-compose.yml` deve utilizar o serviço:

```text
app
```

e o container deve utilizar:

```text
/workspace
```

como diretório de trabalho.

O `devcontainer.json` deve utilizar o serviço:

```json
"service": "app"
```

e:

```json
"workspaceFolder": "/workspace"
```

---

# 👥 Manutenção

Este projeto deve ser tratado como a **base compartilhada dos ambientes de desenvolvimento da equipe**.

Alterações no `Dockerfile` podem afetar todos os projetos que utilizam esta imagem. Por isso, recomenda-se validar as alterações antes de disponibilizá-las para utilização geral.
