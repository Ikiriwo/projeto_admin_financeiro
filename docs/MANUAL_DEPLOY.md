# Manual de Deploy e Especificações
## Sistema Administrativo-Financeiro

---

## 📋 Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Especificações Técnicas](#especificações-técnicas)
3. [Pré-requisitos](#pré-requisitos)
4. [Configuração Local](#configuração-local)
5. [Deploy com Docker](#deploy-com-docker)
6. [Deploy em Servidores](#deploy-em-servidores)
7. [Credenciais de Acesso](#credenciais-de-acesso)
8. [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
9. [API Endpoints](#api-endpoints)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral do Projeto

Sistema web para gestão administrativo-financeira com funcionalidades CRUD completas para:
- **Pessoas**: Fornecedores, Clientes e Faturados
- **Classificações**: Receitas e Despesas
- **Contas**: Movimentos financeiros (A Pagar / A Receber)
- **RAG**: Sistema de consultas inteligentes com IA

### Tecnologias Utilizadas

**Backend:**
- Python 3.11
- Flask 2.3.3
- SQLAlchemy (ORM)
- PostgreSQL 17
- Google Generative AI (Gemini)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 4.5.2
- Font Awesome 5.15.4
- jQuery 3.5.1

**Infraestrutura:**
- Docker & Docker Compose
- pgvector (para embeddings)

---

## 🔧 Especificações Técnicas

### Funcionalidades Implementadas

#### 1. CRUD de Pessoas
- Gerenciamento de Fornecedores, Clientes e Faturados
- Busca e filtros avançados
- Exclusão lógica (STATUS: ATIVO/INATIVO)
- Validação de CPF/CNPJ único

#### 2. CRUD de Classificações
- Gestão de Receitas e Despesas
- Filtros por tipo
- Exclusão lógica
- Ordenação por colunas

#### 3. CRUD de Movimentos de Contas
- Registro de contas A Pagar e A Receber
- Relacionamento com Pessoas e Classificações
- Busca por múltiplos critérios
- Visualização detalhada

#### 4. Recomendações de Layout (Implementadas)
✅ Tabela vazia inicialmente
✅ Carregamento por busca ou "TODOS"
✅ Botão "TODOS" carrega apenas registros ATIVOS
✅ Ordenação por colunas (clicáveis)
✅ Busca por múltiplos elementos
✅ Ações: Editar / Excluir (lógico)
✅ Campo STATUS oculto no CREATE (padrão: ATIVO)
✅ Campo STATUS oculto no UPDATE
✅ DELETE altera STATUS para INATIVO

---

## 📦 Pré-requisitos

### Para Execução Local
- Python 3.11+
- PostgreSQL 17+
- pip (gerenciador de pacotes Python)
- Chave API do Google Gemini

### Para Execução com Docker
- Docker 20.10+
- Docker Compose 2.0+

---

## 🚀 Configuração Local

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd projeto_admin_financeiro-1
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```env
# Configuração do Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/financeiro

# Configuração PostgreSQL
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=financeiro

# API Google Gemini
GEMINI_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=gemini-2.0-flash
```

### 5. Inicializar o Banco de Dados

```bash
# Criar as tabelas
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()

# Popular com dados de teste
psql -U usuario -d financeiro -f scripts/seed_database.sql
```

### 6. Executar a Aplicação

```bash
python app.py
```

Acesse: `http://localhost:5000`

---

## 🐳 Deploy com Docker

### 1. Configurar .env

Certifique-se de que o arquivo `.env` está configurado corretamente.

### 2. Build e Executar

```bash
# Build das imagens
docker-compose build

# Iniciar os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar os serviços
docker-compose down
```

### 3. Acessar o Banco de Dados

```bash
# Conectar ao PostgreSQL
docker-compose exec db psql -U usuario -d financeiro

# Popular com dados de teste
docker-compose exec db psql -U usuario -d financeiro -f /scripts/seed_database.sql
```

### 4. Verificar Status

```bash
# Verificar containers em execução
docker-compose ps

# Verificar logs específicos
docker-compose logs web
docker-compose logs db
```

---

## 🌐 Deploy em Servidores

### A. Backend Python (PythonAnywhere)

1. **Criar conta** em [PythonAnywhere](https://www.pythonanywhere.com)

2. **Upload do código**:
   ```bash
   # Via Git
   cd ~
   git clone <URL_DO_REPOSITORIO>
   cd projeto_admin_financeiro-1
   ```

3. **Configurar ambiente virtual**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 financeiro
   pip install -r requirements.txt
   ```

4. **Configurar Web App**:
   - Painel → Web → Add a new web app
   - Framework: Flask
   - Python version: 3.11
   - Source code: `/home/seuusuario/projeto_admin_financeiro-1`
   - Working directory: `/home/seuusuario/projeto_admin_financeiro-1`
   - WSGI file: Configurar com:
     ```python
     import sys
     path = '/home/seuusuario/projeto_admin_financeiro-1'
     if path not in sys.path:
         sys.path.append(path)

     from app import app as application
     ```

5. **Configurar variáveis de ambiente** no PythonAnywhere

6. **Configurar banco de dados PostgreSQL** (usar serviço externo como ElephantSQL)

### B. Frontend JavaScript (Vercel)

Como o frontend está integrado ao Flask, o deploy completo deve ser feito no PythonAnywhere.
Para deploy separado:

1. Extrair os arquivos estáticos
2. Configurar CORS no backend
3. Atualizar URLs das APIs
4. Deploy via Vercel CLI

### C. Backend JavaScript/Node.js (Render)

Se migrar para Node.js:

1. Criar conta no [Render](https://render.com)
2. New → Web Service
3. Conectar repositório
4. Configurar:
   - Build Command: `npm install`
   - Start Command: `node server.js`
   - Environment Variables: configurar variáveis

---

## 🔐 Credenciais de Acesso

### Banco de Dados

```
Host: localhost (local) ou <host_cloud> (produção)
Port: 5432
Database: financeiro
Username: usuario
Password: senha
```

### Aplicação Web

**Login Padrão:**
- Não há sistema de autenticação implementado no momento
- Acesso direto às páginas:
  - Home: `/`
  - Pessoas: `/pessoas`
  - Classificações: `/classificacoes`
  - Contas: `/contas`
  - RAG: `/rag`

### API Gemini

Obter chave em: [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: pessoas

```sql
id              SERIAL PRIMARY KEY
tipo            VARCHAR(50)        -- FORNECEDOR, CLIENTE, FATURADO
razao_social    VARCHAR(255)
cpf_cnpj        VARCHAR(20) UNIQUE
status          VARCHAR(20)        -- ATIVO, INATIVO
data_cadastro   TIMESTAMP
```

### Tabela: classificacao

```sql
id              SERIAL PRIMARY KEY
tipo            VARCHAR(50)        -- RECEITA, DESPESA
descricao       VARCHAR(255)
status          VARCHAR(20)        -- ATIVO, INATIVO
data_cadastro   TIMESTAMP
```

### Tabela: movimento_contas

```sql
id                      SERIAL PRIMARY KEY
tipo                    VARCHAR(50)        -- APAGAR, ARECEBER
parcela_id              INTEGER (FK)
fornecedor_cliente_id   INTEGER (FK → pessoas)
faturado_id             INTEGER (FK → pessoas)
valor                   FLOAT
status                  VARCHAR(20)        -- ATIVO, INATIVO
data_movimento          TIMESTAMP
```

### Tabela: parcelas_contas

```sql
id              SERIAL PRIMARY KEY
identificacao   VARCHAR(100) UNIQUE
numero_nota     VARCHAR(50)
data_emissao    DATE
data_vencimento DATE
valor_total     FLOAT
data_cadastro   TIMESTAMP
```

---

## 🔌 API Endpoints

### Pessoas

```
GET    /api/pessoas                    - Listar todas
GET    /api/pessoas/<id>               - Obter por ID
POST   /api/pessoas                    - Criar nova
PUT    /api/pessoas/<id>               - Atualizar
DELETE /api/pessoas/<id>               - Excluir (lógico)
```

**Query Params:**
- `tipo`: FORNECEDOR, CLIENTE, FATURADO
- `incluir_inativos`: true/false

### Classificações

```
GET    /api/classificacoes             - Listar todas
GET    /api/classificacoes/<id>        - Obter por ID
POST   /api/classificacoes             - Criar nova
PUT    /api/classificacoes/<id>        - Atualizar
DELETE /api/classificacoes/<id>        - Excluir (lógico)
```

**Query Params:**
- `tipo`: RECEITA, DESPESA
- `incluir_inativos`: true/false

### Movimentos

```
GET    /api/movimentos                 - Listar todos
GET    /api/movimentos/<id>            - Obter por ID
POST   /api/movimentos                 - Criar novo
PUT    /api/movimentos/<id>            - Atualizar
DELETE /api/movimentos/<id>            - Excluir (lógico)
```

**Query Params:**
- `tipo`: APAGAR, ARECEBER
- `incluir_inativos`: true/false

### RAG (Sistema Inteligente)

```
POST   /api/rag/ask                    - Fazer pergunta
GET    /api/rag/examples               - Obter exemplos
GET    /api/rag/status                 - Status do sistema
POST   /api/rag/index                  - Indexar documentos
```

---

## 🐛 Troubleshooting

### Problema: Erro ao conectar ao banco de dados

**Solução:**
1. Verificar se o PostgreSQL está rodando
2. Conferir credenciais no `.env`
3. Verificar se o banco de dados foi criado
4. Testar conexão: `python teste_conexao_db.py`

### Problema: Erro "Module not found"

**Solução:**
```bash
pip install -r requirements.txt
```

### Problema: Porta 5000 já em uso

**Solução:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Problema: Erro ao popular banco de dados

**Solução:**
1. Verificar se as tabelas existem
2. Limpar dados anteriores (se necessário):
   ```sql
   TRUNCATE TABLE movimento_contas CASCADE;
   TRUNCATE TABLE classificacao CASCADE;
   TRUNCATE TABLE pessoas CASCADE;
   ```
3. Executar novamente o script SQL

### Problema: Docker não inicia

**Solução:**
```bash
# Limpar containers e volumes
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Página não carrega estilos/scripts

**Solução:**
1. Verificar se os arquivos estão em `frontend/static/`
2. Limpar cache do navegador
3. Verificar console do navegador para erros 404

---

## 📞 Suporte

Para dúvidas e problemas:
1. Verificar este manual
2. Consultar logs da aplicação
3. Revisar documentação do Flask/SQLAlchemy
4. Verificar issues no GitHub do projeto

---

## 📝 Notas Finais

- **Backup**: Sempre fazer backup do banco de dados antes de alterações
- **Segurança**: Em produção, usar HTTPS e autenticação
- **Monitoramento**: Configurar logs e monitoramento de erros
- **Performance**: Considerar cache para consultas frequentes

---

**Última atualização**: Dezembro 2024
**Versão**: 1.0.0
**Projeto Acadêmico N2** - Sistema Administrativo-Financeiro
