# Deploy no Render - Guia Completo

Este guia detalha o processo de deploy da aplicação no Render.

## Pré-requisitos

1. Conta no [Render](https://render.com) (pode usar conta gratuita)
2. Repositório do projeto no GitHub/GitLab
3. Chave API do Google Gemini

---

## Opção 1: Deploy Automático (Recomendado)

### Passo 1: Preparar o Repositório

Certifique-se de que os seguintes arquivos estão no repositório:
- `render.yaml` ✓ (criado)
- `build.sh` ✓ (criado)
- `requirements.txt` ✓ (atualizado com gunicorn)
- `app.py` ✓ (configurado para usar PORT do ambiente)

### Passo 2: Fazer Push para o GitHub

```bash
git add .
git commit -m "Configuração para deploy no Render"
git push origin main
```

### Passo 3: Conectar ao Render

1. Acesse [dashboard.render.com](https://dashboard.render.com)
2. Clique em **"New +"** → **"Blueprint"**
3. Conecte seu repositório GitHub/GitLab
4. Selecione o repositório do projeto
5. O Render detectará automaticamente o `render.yaml`

### Passo 4: Configurar Variáveis de Ambiente

O Render solicitará as variáveis de ambiente necessárias:

- **GEMINI_API_KEY**: Sua chave da API do Google Gemini
- **GEMINI_MODEL**: `gemini-2.0-flash` (já configurado)

### Passo 5: Deploy

1. Clique em **"Apply"**
2. Aguarde o build e deploy (pode levar alguns minutos)
3. O Render criará automaticamente:
   - Web Service (aplicação Flask)
   - PostgreSQL Database

---

## Opção 2: Deploy Manual

Se preferir configurar manualmente:

### Passo 1: Criar PostgreSQL Database

1. No dashboard do Render, clique em **"New +"** → **"PostgreSQL"**
2. Preencha:
   - **Name**: `admin-financeiro-db`
   - **Database**: `admin_financeiro`
   - **User**: `postgres`
   - **Region**: Oregon (Free)
   - **Plan**: Free
3. Clique em **"Create Database"**
4. Aguarde a criação (1-2 minutos)
5. **Copie a "Internal Database URL"** (usaremos depois)

### Passo 2: Criar Web Service

1. No dashboard, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório
3. Preencha:
   - **Name**: `admin-financeiro`
   - **Region**: Oregon (Free)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

### Passo 3: Configurar Variáveis de Ambiente

Na seção "Environment Variables", adicione:

```
PYTHON_VERSION=3.11.0
FLASK_ENV=production
GEMINI_API_KEY=sua_chave_api_aqui
GEMINI_MODEL=gemini-2.0-flash
DATABASE_URL=<cole_a_internal_database_url_aqui>
```

**IMPORTANTE**: Use a "Internal Database URL" copiada do passo 1.

### Passo 4: Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o build e deploy (5-10 minutos)
3. O Render instalará dependências e iniciará a aplicação

---

## Verificação Pós-Deploy

### 1. Verificar Status do Serviço

No dashboard do Render:
- **Web Service**: Status deve estar "Live" (verde)
- **Database**: Status deve estar "Available" (verde)

### 2. Acessar a Aplicação

A URL será algo como:
```
https://admin-financeiro.onrender.com
```

### 3. Verificar Logs

Se houver problemas, verifique os logs:
1. Clique no seu Web Service
2. Vá para a aba **"Logs"**
3. Procure por erros em vermelho

### 4. Testar Funcionalidades

Acesse as páginas principais:
- `/` - Dashboard
- `/pessoas` - CRUD de Pessoas
- `/classificacoes` - CRUD de Classificações
- `/contas` - CRUD de Contas
- `/rag` - Sistema RAG (IA)

---

## Configurações Importantes

### Porta da Aplicação

O Render define automaticamente a variável `PORT`. A aplicação já está configurada para usar:

```python
port = int(os.environ.get('PORT', 5000))
```

### Banco de Dados

O Render fornece a `DATABASE_URL` automaticamente quando você usa a configuração "fromDatabase" no `render.yaml`.

### Persistência de Dados

- **Banco de dados**: Persistente (dados não são perdidos)
- **Uploads**: No plano gratuito, arquivos podem ser perdidos após reiniciar. Para produção, considere usar:
  - Amazon S3
  - Cloudinary
  - Google Cloud Storage

---

## Troubleshooting

### Problema: "Application failed to respond"

**Causa**: A aplicação não está iniciando corretamente

**Solução**:
1. Verifique os logs
2. Certifique-se de que `DATABASE_URL` está configurado
3. Verifique se todas as dependências do `requirements.txt` foram instaladas

### Problema: "Module not found"

**Causa**: Dependência faltando no `requirements.txt`

**Solução**:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Atualizar dependências"
git push
```

### Problema: "Database connection failed"

**Causa**: `DATABASE_URL` incorreto ou banco não criado

**Solução**:
1. Verifique se o PostgreSQL está "Available"
2. Copie novamente a "Internal Database URL"
3. Atualize a variável `DATABASE_URL` no Web Service
4. Faça um redeploy manual

### Problema: Tabelas não existem

**Causa**: Banco novo, tabelas não foram criadas

**Solução**:
O `app.py` cria as tabelas automaticamente no primeiro acesso. Mas você pode forçar:

1. Acesse o Shell do Render:
   - Dashboard → Web Service → Shell
2. Execute:
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
   ```

### Problema: "API Key inválida" (Gemini)

**Causa**: `GEMINI_API_KEY` não configurado ou inválido

**Solução**:
1. Obtenha uma nova chave em [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Atualize a variável de ambiente
3. Redeploy

---

## Limites do Plano Gratuito

O plano gratuito do Render tem algumas limitações:

- **Web Service**:
  - 750 horas/mês
  - Suspende após 15 minutos de inatividade
  - Reinicia ao receber requisição (pode levar 30-60 segundos)

- **PostgreSQL**:
  - 1 GB de armazenamento
  - Conexões limitadas
  - Backups não inclusos

- **Banda**:
  - 100 GB/mês

### Recomendação para Produção

Para uso em produção, considere upgrade para planos pagos:
- **Web Service**: $7/mês (sem suspensão)
- **PostgreSQL**: $7/mês (backups automáticos)

---

## Atualizações e Redeploy

### Deploy Automático

O Render faz deploy automático quando você faz push para o branch `main`:

```bash
git add .
git commit -m "Atualização da aplicação"
git push origin main
```

### Deploy Manual

No dashboard do Render:
1. Acesse seu Web Service
2. Clique em **"Manual Deploy"** → **"Deploy latest commit"**

---

## Comandos Úteis

### Acessar Shell do Container

```bash
# No dashboard do Render
Web Service → Shell
```

### Ver Logs em Tempo Real

```bash
# No dashboard do Render
Web Service → Logs → Enable "Auto-scroll"
```

### Reiniciar Serviço

```bash
# No dashboard do Render
Web Service → Manual Deploy → Restart
```

---

## Checklist de Deploy

Antes de fazer deploy, verifique:

- [ ] `requirements.txt` contém `gunicorn`
- [ ] `build.sh` tem permissão de execução
- [ ] `render.yaml` está configurado corretamente
- [ ] Variáveis de ambiente estão definidas
- [ ] `.gitignore` não está bloqueando arquivos importantes
- [ ] Código está no GitHub/GitLab
- [ ] PostgreSQL foi criado no Render
- [ ] `GEMINI_API_KEY` é válida

---

## Monitoramento

### Logs de Aplicação

Verifique regularmente os logs para identificar problemas:
- Erros de conexão com banco
- Falhas de API
- Requisições lentas

### Métricas

No dashboard do Render você pode ver:
- CPU usage
- Memory usage
- Request count
- Response time

---

## Backup do Banco de Dados

### Manual (Plano Gratuito)

1. Instale o PostgreSQL Client localmente
2. Use o comando:
   ```bash
   pg_dump -h <host> -U <user> -d <database> > backup.sql
   ```

### Automático (Plano Pago)

Os planos pagos incluem backups automáticos diários.

---

## Migração de Dados

Se você já tem dados localmente:

1. Exporte do banco local:
   ```bash
   pg_dump -U usuario -d admin_financeiro > dados_local.sql
   ```

2. Importe para o Render:
   ```bash
   psql -h <render_host> -U <render_user> -d admin_financeiro < dados_local.sql
   ```

---

## Recursos Adicionais

- [Documentação oficial do Render](https://render.com/docs)
- [Deploy de aplicações Python no Render](https://render.com/docs/deploy-flask)
- [PostgreSQL no Render](https://render.com/docs/databases)

---

**Última atualização**: Novembro 2025
**Versão**: 1.0.0
