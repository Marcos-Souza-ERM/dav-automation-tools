# DAV Automation Tools

Ambiente Docker padronizado para desenvolvimento e ferramentas de automação da equipe, com o objetivo principal de **reduzir o tempo de configuração e ambientalização de novos integrantes**.

O projeto fornece uma base Docker com as principais dependências e ferramentas necessárias para os projetos da equipe. Dessa forma, um novo integrante não precisa realizar manualmente a instalação e configuração de ferramentas como Python, Java, Node.js, Tesseract, PostgreSQL Client e outras dependências comuns.

Além da função principal de **padronização do ambiente de desenvolvimento**, o repositório também disponibiliza uma ferramenta independente para **processamento de documentos utilizando OCR**, executada através de uma imagem Docker específica.

A configuração do ambiente de desenvolvimento é integrada ao **VS Code Dev Containers**, permitindo que os projetos da equipe sejam executados em um ambiente padronizado.

---

# 🎯 Objetivo

O principal objetivo do `dav-automation-tools` é **padronizar e simplificar a ambientalização de novos integrantes da equipe**.

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
5. Clonar o repositório;
6. Configurar o `.devcontainer` no projeto que deseja executar;
7. Abrir o projeto no Dev Container.

O restante do ambiente de desenvolvimento é criado automaticamente pelo Docker.

Além disso, o repositório possui uma ferramenta de OCR que pode ser executada independentemente do Dev Container, utilizando uma imagem Docker própria.

---

# 🏗️ Arquitetura

O projeto possui duas funcionalidades principais:

```text
                         DAV Automation Tools
                                  │
                ┌─────────────────┴─────────────────┐
                │                                   │
                ▼                                   ▼
       Ambiente de Desenvolvimento             Ferramenta OCR
                │                                   │
                │ .devcontainer                     │ Dockerfile.ocr
                │                                   │
                ▼                                   ▼
        Dockerfile principal                  dav-automation-ocr
                │                                   │
                ▼                                   ▼
       Imagem de desenvolvimento             Processamento de
                │                             documentos
                │                                   │
                ▼                                   ▼
        Projetos da equipe                 documentos/ → output/
```

## Ambiente de desenvolvimento

A imagem principal funciona como uma **imagem base de desenvolvimento compartilhada**.

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

A estrutura atual do repositório inclui tanto os arquivos utilizados para a ambientalização quanto os arquivos relacionados ao OCR:

```text
dav-automation-tools/
│
├── documentos/
│   └── Teste-de-OCR-Exemplo.pdf
│
├── ocr/
│   └── app.py
│
├── output/
│   └── Teste-de-OCR-Exemplo.txt
│
├── Dockerfile
├── Dockerfile.ocr
├── README.md
├── requirements.txt
└── run-ocr.ps1
```

## Principais arquivos e diretórios

### `Dockerfile`

Define a imagem base utilizada pelos projetos da equipe para desenvolvimento.

Essa é a imagem relacionada à **ambientalização dos novos integrantes** e ao uso através do VS Code Dev Containers.

---

### `Dockerfile.ocr`

Define a imagem Docker utilizada especificamente para execução da ferramenta de OCR.

A imagem é construída com:

```bash
docker build -f Dockerfile.ocr -t dav-automation-ocr .
```

Depois de construída, ela pode ser executada independentemente do ambiente de desenvolvimento.

---

### `ocr/app.py`

É o código responsável pela execução do processo de OCR.

O processamento utiliza os arquivos disponibilizados no diretório:

```text
documentos/
```

e grava os resultados no diretório:

```text
output/
```

A execução ocorre dentro do container `dav-automation-ocr`, evitando a necessidade de configurar manualmente o ambiente de OCR na máquina do desenvolvedor.

---

### `documentos/`

Diretório utilizado para armazenar os arquivos que serão processados pelo OCR.

Exemplo:

```text
documentos/
└── Teste-de-OCR-Exemplo.pdf
```

Novos PDFs ou imagens podem ser adicionados nesse diretório antes da execução do OCR.

---

### `output/`

Diretório utilizado para armazenar os resultados gerados pelo OCR.

Exemplo:

```text
output/
└── Teste-de-OCR-Exemplo.txt
```

Como esse diretório é montado como volume do Docker, os resultados ficam disponíveis diretamente na máquina do desenvolvedor após o término da execução.

---

### `requirements.txt`

Contém as dependências Python utilizadas pelos projetos que utilizam o ambiente de desenvolvimento.

As dependências específicas de cada aplicação continuam sendo responsabilidade do projeto que está sendo desenvolvido.

---

# 🐳 Conteúdo da imagem de desenvolvimento

O `Dockerfile` principal instala as principais ferramentas necessárias ao ambiente:

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

## 2. Clonar o `dav-automation-tools`

O repositório deve ser clonado em uma posição compatível com o `docker-compose.yml` utilizado pelos projetos.

Exemplo:

```text
workspace/

├── dav-automation-tools/
│   ├── Dockerfile
│   ├── Dockerfile.ocr
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

Todo projeto que utilizar o ambiente de desenvolvimento deverá possuir um diretório `.devcontainer`.

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

O `docker-compose.yml` deve utilizar o `dav-automation-tools` como contexto de build.

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

# 🔍 Ferramenta de OCR

Além de fornecer a base de desenvolvimento, o `dav-automation-tools` possui uma ferramenta específica para processamento de documentos através de OCR.

O OCR é executado em um **container separado**, utilizando o `Dockerfile.ocr`.

Essa separação permite que a ferramenta seja utilizada sem depender do ambiente de desenvolvimento do projeto.

## Estrutura do OCR

```text
dav-automation-tools/

├── documentos/
│   └── Teste-de-OCR-Exemplo.pdf
│
├── ocr/
│   └── app.py
│
├── output/
│   └── Teste-de-OCR-Exemplo.txt
│
└── Dockerfile.ocr
```

O fluxo de processamento é:

```text
documentos/
     │
     │ PDF / imagem
     ▼
dav-automation-ocr
     │
     │ ocr/app.py
     ▼
Processamento OCR
     │
     ▼
output/
     │
     └── arquivo .txt
```

Os arquivos de entrada devem ser colocados em:

```text
documentos/
```

Os resultados serão disponibilizados em:

```text
output/
```

---

# 🐳 Construindo a imagem do OCR

Na raiz do repositório, execute:

```bash
docker build -f Dockerfile.ocr -t dav-automation-ocr .
```

Esse comando cria a imagem:

```text
dav-automation-ocr
```

---

# ▶️ Executando o OCR

Depois de construir a imagem, os arquivos presentes em `documentos/` podem ser processados utilizando volumes Docker.

## Git Bash / terminal compatível

```bash
docker run --rm \
    -v "C:/Users/usuario/DAV/dav-automation-tools/documentos:/app/documentos" \
    -v "C:/Users/usuario/DAV/dav-automation-tools/output:/app/output" \
    dav-automation-ocr
```

> O caminho `C:/Users/usuario/DAV/dav-automation-tools` deve ser ajustado de acordo com o local onde o repositório foi clonado.

---

## PowerShell (recomendado)

No PowerShell, estando na raiz do projeto:

```powershell
docker run --rm `
    -v "${PWD}\documentos:/app/documentos" `
    -v "${PWD}\output:/app/output" `
    dav-automation-ocr
```

O comando monta:

```text
./documentos → /app/documentos
./output     → /app/output
```

Dessa forma, o container consegue ler os documentos da máquina local e gravar os resultados diretamente no diretório `output/`.

---

# 🆕 Executando o projeto pela primeira vez

Para um novo usuário, o fluxo completo para utilizar o OCR é:

## 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

## 2. Entrar no projeto

```bash
cd dav-automation-tools
```

## 3. Colocar os arquivos para OCR

Copie os PDFs ou imagens que deseja processar para:

```text
.\documentos\
```

Por exemplo:

```text
documentos/
├── documento-1.pdf
├── documento-2.pdf
└── imagem.png
```

## 4. Construir a imagem OCR

```bash
docker build -f Dockerfile.ocr -t dav-automation-ocr .
```

## 5. Executar o OCR

No PowerShell:

```powershell
docker run --rm `
    -v "${PWD}\documentos:/app/documentos" `
    -v "${PWD}\output:/app/output" `
    dav-automation-ocr
```

Após a execução, os resultados estarão disponíveis em:

```text
output/
```

---

# 🔄 Diferença entre o ambiente de desenvolvimento e o OCR

É importante diferenciar as duas imagens Docker existentes no projeto.

| Imagem                      | Dockerfile       | Finalidade                                               |
| --------------------------- | ---------------- | -------------------------------------------------------- |
| Ambiente de desenvolvimento | `Dockerfile`     | Ambientalização e desenvolvimento dos projetos da equipe, vai conter as bibliotecas e as linguagens de programação necessárias para o desenvolvimento. |
| OCR                         | `Dockerfile.ocr` | Processamento automatizado de documentos                 |

A imagem principal não deve ser confundida com a imagem de OCR.

O **objetivo principal do projeto continua sendo a padronização e automatização da ambientalização dos integrantes da equipe**. O OCR é uma ferramenta adicional disponibilizada no mesmo repositório para automatizar o processamento de documentos.

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
sua-pasta/

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

## O OCR não gera arquivos no `output/`

Verifique:

1. Se existem arquivos dentro de `documentos/`;
2. Se a imagem `dav-automation-ocr` foi construída;
3. Se o volume `output` foi montado corretamente;
4. Se o comando foi executado a partir da raiz do projeto.

Para conferir os arquivos:

```powershell
Get-ChildItem .\documentos
Get-ChildItem .\output
```

Caso necessário, reconstrua a imagem:

```bash
docker build -f Dockerfile.ocr -t dav-automation-ocr .
```

E execute novamente:

```powershell
docker run --rm `
    -v "${PWD}\documentos:/app/documentos" `
    -v "${PWD}\output:/app/output" `
    dav-automation-ocr
```

---

## Quero reconstruir a imagem de desenvolvimento

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

O fluxo esperado para um novo integrante utilizando a função principal do projeto é:

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

O OCR possui um fluxo independente:

```text
1. Clonar dav-automation-tools
        ↓
2. Colocar documentos em documentos/
        ↓
3. Construir Dockerfile.ocr
        ↓
4. Criar imagem dav-automation-ocr
        ↓
5. Executar o container
        ↓
6. OCR processa os documentos
        ↓
7. Resultados disponíveis em output/
```

---

# 💡 Conceito do projeto

O principal objetivo do `dav-automation-tools` é **reduzir o esforço necessário para ambientalizar novos integrantes e manter ambientes de desenvolvimento consistentes entre os projetos da equipe**.

O repositório funciona como uma **base compartilhada de ferramentas e ambiente de desenvolvimento**, mas também reúne automações auxiliares, como o processamento de documentos através de OCR.

A separação de responsabilidades é:

```text
dav-automation-tools

        │
        ├── Ambientalização
        │       │
        │       ├── Python
        │       ├── Java
        │       ├── Node.js
        │       ├── Tesseract
        │       ├── PostgreSQL Client
        │       └── Ferramentas comuns
        │
        └── Automação OCR
                │
                ├── Dockerfile.ocr
                ├── ocr/app.py
                ├── documentos/
                └── output/
```

A parte de ambientalização continua sendo a **finalidade principal do projeto**, enquanto o OCR funciona como uma ferramenta complementar que pode ser executada de forma independente.

Dessa forma, a equipe consegue:

* Reduzir o tempo de preparação de novas máquinas;
* Padronizar os ambientes de desenvolvimento;
* Evitar configurações manuais diferentes entre integrantes;
* Centralizar ferramentas comuns utilizadas pelos projetos;
* Executar o processamento de documentos em um ambiente Docker isolado;
* Facilitar a reprodução do processo de OCR em diferentes máquinas.

---

# 📌 Convenções recomendadas

Para novos projetos que utilizarem o ambiente de desenvolvimento, recomenda-se manter:

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

O `devcontainer.json` deve utilizar:

```json
"service": "app"
```

e:

```json
"workspaceFolder": "/workspace"
```

Para a ferramenta de OCR, recomenda-se manter a seguinte estrutura:

```text
dav-automation-tools/

├── documentos/
├── ocr/
├── output/
├── Dockerfile.ocr
└── run-ocr.ps1
```

Os arquivos de entrada devem ser colocados em `documentos/` e os resultados gerados devem ser armazenados em `output/`.

---

# 👥 Manutenção

Este projeto deve ser tratado como a **base compartilhada dos ambientes de desenvolvimento e ferramentas de automação da equipe**.

Alterações no `Dockerfile` podem afetar todos os projetos que utilizam essa imagem. Por isso, recomenda-se validar as alterações antes de disponibilizá-las para utilização geral.

Alterações no `Dockerfile.ocr` ou no código localizado em `ocr/app.py` devem ser testadas com documentos de exemplo antes de serem disponibilizadas para uso geral.

A separação entre `Dockerfile` e `Dockerfile.ocr` deve ser mantida para evitar que alterações específicas do OCR impactem desnecessariamente o ambiente principal de desenvolvimento.
