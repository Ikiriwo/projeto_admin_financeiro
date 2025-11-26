# 🚀 Deploy no PythonAnywhere - Guia Completo

Este guia explica como fazer o deploy do sistema no PythonAnywhere, incluindo a melhor abordagem para popular o banco de dados.

---

## 📋 Abordagem Recomendada para Dados de Teste

### ✅ **Abordagem Híbrida** (RECOMENDADA)

Para um projeto acadêmico/demonstração, recomendo:

1. **Popular dados inicialmente** no deploy via console
2. **Manter painel admin** para resetar dados se necessário

### Por quê?

| Aspecto | Dados Pré-Inseridos | Botão na Interface |
|---------|---------------------|-------------------|
| **Demonstração imediata** | ✅ Sim | ❌ Precisa executar primeiro |
| **Pronto para avaliar** | ✅ Sim | ❌ Avaliador precisa configurar |
| **Controle sobre dados** | ⚠️ Manual | ✅ Interface amigável |
| **Proteção contra erros** | ✅ Estável | ⚠️ Pode ser executado múltiplas vezes |
| **Facilidade para reset** | ⚠️ Via console | ✅ Via interface |

**Resultado:** Sistema já funcional + painel admin para manutenção = **Melhor dos dois mundos!**

---

## 🎯 Estratégia de Deploy

### Fase 1: Deploy Inicial
1. Fazer deploy do código
2. Configurar banco de dados
3. **Popular dados via console** (uma vez)
4. Sistema pronto para uso

### Fase 2: Manutenção (Opcional)
- Usar painel `/admin` para resetar dados se necessário
- Protegido por senha (`ADMIN_PASSWORD`)

---

## 📦 Passo a Passo - Deploy no PythonAnywhere

### 1. Criar Conta no PythonAnywhere

1. Acesse [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Crie uma conta gratuita (Beginner)
3. Faça login

### 2. Configurar Banco de Dados PostgreSQL

**Opção A: PostgreSQL Externo (Recomendado)**

Use um serviço gratuito como [ElephantSQL](https://www.elephantsql.com/):

```bash
# Exemplo de DATABASE_URL
DATABASE_URL=postgresql://usuario:senha@servidor.db.elephantsql.com/banco
```

**Opção B: MySQL do PythonAnywhere**

```python
# No PythonAnywhere Dashboard:
# Databases → Create a new MySQL database
DATABASE_URL=mysql://usuario:senha@usuario.mysql.pythonanywhere-services.com/usuario$nomedobanco
```

### 3. Upload do Código

**Opção A: Via Git (Recomendado)**

```bash
# No console do PythonAnywhere
cd ~
git clone https://github.com/seu-usuario/projeto_admin_financeiro-1.git
cd projeto_admin_financeiro-1
```

**Opção B: Upload Manual**

1. Dashboard → Files
2. Upload arquivos .zip
3. Extrair no diretório

### 4. Criar Ambiente Virtual

```bash
# No console do PythonAnywhere
cd ~/projeto_admin_financeiro-1
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
nano .env
```

Adicione:
```env
# Banco de Dados
DATABASE_URL=postgresql://usuario:senha@servidor.elephantsql.com/banco

# Google Gemini API
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.0-flash

# Senha Admin (IMPORTANTE: Altere!)
ADMIN_PASSWORD=senha_segura_aqui
```

Salve com `Ctrl+O`, `Enter`, `Ctrl+X`

### 6. Criar Tabelas do Banco

```bash
# No console, com venv ativado
python
```

```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Tabelas criadas!")
exit()
```

### 7. 🎯 **POPULAR BANCO DE DADOS** (IMPORTANTE!)

**Execute AGORA para ter dados de demonstração:**

```bash
# Ainda no console, com venv ativado
python scripts/populate_database.py
```

Você verá:
```
======================================================================
📊 POPULAÇÃO DO BANCO DE DADOS
======================================================================

📝 Inserindo dados de teste...

   ✓ Bloco 1 executado
   ✓ Bloco 2 executado
   ...

📊 Estatísticas:
   • Pessoas: 80
   • Classificacoes: 40
   • Parcelas: 80
   • Movimentos: 5
   • Relacionamentos: 5

======================================================================
✅ BANCO DE DADOS POPULADO COM SUCESSO!
======================================================================
```

**Pronto! Sistema com dados de demonstração! 🎉**

### 8. Configurar Web App

1. Dashboard → Web
2. Add a new web app
3. Manual configuration → Python 3.11
4. Configurar:

**WSGI Configuration File:**
```python
import sys
import os
from dotenv import load_dotenv

# Adicionar projeto ao path
path = '/home/seu_usuario/projeto_admin_financeiro-1'
if path not in sys.path:
    sys.path.append(path)

# Carregar .env
project_folder = os.path.expanduser(path)
load_dotenv(os.path.join(project_folder, '.env'))

# Importar aplicação
from app import app as application
```

**Virtualenv:**
```
/home/seu_usuario/projeto_admin_financeiro-1/venv
```

**Static files:**
```
URL: /static/
Directory: /home/seu_usuario/projeto_admin_financeiro-1/frontend/static
```

### 9. Reload e Testar

1. Clique em "Reload" no topo da página
2. Acesse: `https://seu_usuario.pythonanywhere.com`
3. **Sistema já com dados! Pronto para demonstrar!**

---

## 🔧 Painel Administrativo

Após o deploy, você pode gerenciar os dados via interface:

### Acessar Painel Admin

```
https://seu_usuario.pythonanywhere.com/admin
```

### Funcionalidades:

1. **Ver Status do Banco**
   - Quantidade de registros em cada tabela
   - Total geral

2. **Popular Banco** (Adicionar)
   - Insere 250+ registros
   - Não remove dados existentes

3. **Resetar e Popular**
   - Limpa tudo
   - Insere dados novos

4. **Limpar Banco**
   - Remove todos os dados
   - Use com cuidado!

### Senha Padrão

```
Usuário: (não tem)
Senha: admin123
```

**⚠️ IMPORTANTE:** Altere a senha em produção via variável `ADMIN_PASSWORD` no `.env`

---

## 🎓 Para Avaliação Acadêmica

### Checklist antes de apresentar:

- [ ] Sistema no ar no PythonAnywhere
- [ ] **Dados já populados** (250+ registros)
- [ ] Chave API do Gemini configurada
- [ ] RAG funcionando com as perguntas de teste
- [ ] Todas as páginas carregando (Pessoas, Classificações, Contas, RAG)
- [ ] Link do projeto funcional

### Apresentação para Professor:

1. **Acesse o link** - Sistema já está com dados
2. **Demonstre CRUD** - Dados já carregados nas tabelas
3. **Teste o RAG** - Faça perguntas sobre os dados existentes
4. **Mostre painel admin** (opcional) - Capacidade de reset se necessário

**Vantagem:** Professor não precisa configurar nada! Sistema já funcional! ✅

---

## 🆘 Troubleshooting

### Erro: "DisallowedHost"

```python
# No app.py, adicione:
app.config['ALLOWED_HOSTS'] = ['seu_usuario.pythonanywhere.com']
```

### Erro: "No such table"

```bash
# Criar tabelas novamente
python
from app import app, db
with app.app_context():
    db.create_all()
exit()
```

### Banco sem dados

```bash
# Executar script de população
python scripts/populate_database.py
```

### Resetar dados via console

```bash
# Limpar e popular novamente
python scripts/populate_database.py --clear
```

---

## 📊 Comandos Úteis

```bash
# Ver status dos dados
python scripts/populate_database.py --status

# Popular (adicionar dados)
python scripts/populate_database.py

# Resetar (limpar + popular)
python scripts/populate_database.py --clear

# Acessar console Python
python
from app import app, db
with app.app_context():
    # seus comandos aqui
    pass
```

---

## ✅ Checklist Final

Deploy completo:
- [ ] Código no PythonAnywhere
- [ ] Ambiente virtual configurado
- [ ] Dependências instaladas
- [ ] Banco de dados configurado
- [ ] Tabelas criadas
- [ ] **Dados populados (250+ registros)**
- [ ] WSGI configurado
- [ ] Arquivos estáticos configurados
- [ ] Web app recarregado
- [ ] Site funcionando
- [ ] RAG testado e funcionando

---

## 🎉 Conclusão

**Abordagem Recomendada:**

1. ✅ **Popular dados uma vez** no deploy inicial
2. ✅ **Sistema já funcional** ao acessar
3. ✅ **Painel admin disponível** para manutenção
4. ✅ **Perfeito para demonstração acadêmica**

**Resultado:** Sistema profissional, pronto para demonstrar, com controle total sobre os dados!

---

**Dúvidas?** Consulte a [documentação do PythonAnywhere](https://help.pythonanywhere.com/)
