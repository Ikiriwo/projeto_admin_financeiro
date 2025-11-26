# 💰 Sistema Administrativo-Financeiro

Sistema web para gestão financeira com CRUD de Pessoas, Classificações e Contas, além de processamento inteligente de notas fiscais com IA.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-2.3.3-green) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)

---

## 🎯 Funcionalidades

- **Pessoas**: Gerenciamento de Fornecedores, Clientes e Faturados
- **Classificações**: Gestão de Receitas e Despesas
- **Contas**: Movimentos financeiros (A Pagar / A Receber)
- **Upload de Notas Fiscais**: Extração automática de dados com IA (Google Gemini)
- **Sistema RAG**: Consultas inteligentes ao banco de dados
- **Interface Responsiva**: Bootstrap 4 com design moderno

---

## 🚀 Quick Start

### Opção 1: Docker (Recomendado)

```bash
# 1. Clonar e configurar
git clone <URL_DO_REPOSITORIO>
cd projeto_admin_financeiro-1

# 2. Iniciar
docker-compose up -d

# 3. Acessar
http://localhost:5000
```

### Opção 2: Instalação Local

```bash
# 1. Ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar
python app.py
```

---

## ⚙️ Configuração da API Gemini

Na primeira execução, você será direcionado para a página de **Configurações** onde poderá:

1. **Inserir sua chave API** do Google Gemini
2. **Validar automaticamente** - o sistema testa se a chave funciona
3. **Salvar com segurança** - chave armazenada localmente no `.env`

### Como obter a chave API:

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave e configure no sistema

**Segurança:**
- ✅ Arquivo `.env` protegido no `.gitignore`
- ✅ Chave nunca é exposta no código ou Git
- ✅ Validação em tempo real antes de salvar

---

## 📁 Estrutura

```
projeto_admin_financeiro-1/
├── app.py                 # Aplicação principal Flask
├── config_manager.py      # Gerenciador de configurações
├── models/                # Modelos de banco de dados (SQLAlchemy)
├── routes/                # Blueprints Flask (API + Web)
├── frontend/              # Interface web (templates + static)
├── agents/                # Processamento de documentos com IA
├── rag_system/            # Sistema RAG para consultas inteligentes
├── scripts/               # Scripts de gerenciamento do banco
│   ├── clear_database.py  # Limpar banco via CMD
│   ├── populate_database.py # Popular com dados de teste
│   └── README.md          # Documentação dos scripts
├── docs/                  # Documentação técnica
└── uploads/               # Arquivos enviados
```

---

## 🛠️ Scripts de Gerenciamento

```bash
# Limpar todos os dados do banco
python scripts/clear_database.py

# Popular com dados de teste (250+ registros)
python scripts/populate_database.py

# Limpar e popular do zero
python scripts/populate_database.py --clear

# Verificar status do banco
python scripts/populate_database.py --status
```

Veja mais em [`scripts/README.md`](scripts/README.md)

---

## 🔌 API Endpoints

### Pessoas
- `GET /api/pessoas` - Listar
- `POST /api/pessoas` - Criar
- `PUT /api/pessoas/<id>` - Atualizar
- `DELETE /api/pessoas/<id>` - Excluir (lógico)

### Classificações
- `GET /api/classificacoes` - Listar
- `POST /api/classificacoes` - Criar
- `PUT /api/classificacoes/<id>` - Atualizar
- `DELETE /api/classificacoes/<id>` - Excluir (lógico)

### Movimentos
- `GET /api/movimentos` - Listar
- `POST /api/movimentos` - Criar
- `PUT /api/movimentos/<id>` - Atualizar
- `DELETE /api/movimentos/<id>` - Excluir (lógico)

### RAG
- `POST /api/rag/ask` - Fazer pergunta ao sistema inteligente
- `GET /api/rag/status` - Status do sistema

---

## 📊 Banco de Dados

### Configuração PostgreSQL

**Docker:**
```bash
# Já configurado no docker-compose.yml
docker-compose up -d
```

**Local:**
```bash
# Criar banco
psql -U postgres
CREATE DATABASE admin_financeiro;
```

### Arquivo .env

```env
# Banco de Dados
DATABASE_URL=postgresql://postgres:senha@localhost:5432/admin_financeiro

# Google Gemini API
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.0-flash
```

---

## 🛠️ Tecnologias

- **Backend**: Python 3.11, Flask 2.3.3, SQLAlchemy
- **Banco**: PostgreSQL 17 com pgvector
- **IA**: Google Generative AI (Gemini)
- **Frontend**: Bootstrap 4, jQuery, Font Awesome
- **DevOps**: Docker, Docker Compose

---

## 📖 Documentação Adicional

- **[Scripts](scripts/README.md)** - Gerenciamento do banco de dados
- **[Deploy](docs/MANUAL_DEPLOY.md)** - Produção (PythonAnywhere, Vercel, Render)
- **[RAG](docs/README_RAG.md)** - Sistema de consultas inteligentes
- **[Changelog](docs/CHANGELOG.md)** - Histórico de mudanças

---

## 🔒 Segurança

### Boas Práticas Implementadas:

- ✅ Chaves API no `.env` (protegido no `.gitignore`)
- ✅ Interface web para configuração segura
- ✅ Validação antes de salvar credenciais
- ✅ Configuração via interface (não precisa editar arquivos)

### ⚠️ NUNCA faça:

```bash
# ❌ ERRADO - Nunca commite o .env
git add .env
git commit -m "Adiciona configurações"
```

### ✅ Configure pelo sistema:

1. Inicie a aplicação
2. Acesse a página de Configurações
3. Insira sua chave API do Google Gemini
4. Sistema valida e salva automaticamente

---

## 🎓 Projeto Acadêmico

Este sistema foi desenvolvido como projeto acadêmico N2, implementando:

- ✅ CRUD completo de Pessoas, Classificações e Contas
- ✅ Exclusão lógica (STATUS: ATIVO/INATIVO)
- ✅ Filtros e buscas avançadas
- ✅ Interface responsiva e moderna
- ✅ Processamento de documentos com IA
- ✅ Sistema RAG para consultas inteligentes
- ✅ API REST completa
- ✅ Preparado para deploy em produção

---

## 📞 Suporte

- 📘 [Manual de Deploy](docs/MANUAL_DEPLOY.md)
- 📚 [Documentação do RAG](docs/README_RAG.md)
- 🛠️ [Scripts de Gerenciamento](scripts/README.md)

---

## ✨ Autor

**Projeto Acadêmico N2** - Sistema Administrativo-Financeiro

**🚀 Pronto para deploy!**
