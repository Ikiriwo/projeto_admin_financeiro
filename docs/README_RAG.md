# Sistema RAG - Consulta Inteligente

Sistema de Consulta Inteligente usando RAG (Retrieval-Augmented Generation) para análise de dados financeiros.

## Visão Geral

O sistema RAG implementa duas abordagens para responder perguntas sobre os dados financeiros:

### 1. RAG Simples
- Busca direta no banco de dados usando SQL
- Usa queries otimizadas para recuperar dados relevantes
- LLM (Google Gemini) elabora respostas naturais baseadas nos dados
- **Vantagens**: Rápido, preciso, não requer indexação prévia
- **Use quando**: Precisar de dados estruturados e agregações

### 2. RAG com Embeddings
- Busca semântica usando vetorização (sentence-transformers)
- Encontra documentos similares baseado no significado
- LLM elabora respostas contextualizadas
- **Vantagens**: Entende intenção, busca por similaridade semântica
- **Use quando**: Precisar encontrar informações relacionadas ao contexto

## Instalação

### 1. Dependências

```bash
pip install -r requirements.txt
```

As dependências do RAG incluem:
- `pgvector>=0.2.0` - Extensão PostgreSQL para vetores (opcional)
- `python-dotenv>=1.0.0` - Para carregar variáveis de ambiente

### 2. Configuração

Certifique-se de que o arquivo `.env` contém:

```env
GEMINI_API_KEY=sua_api_key_aqui
GEMINI_MODEL=gemini-2.0-flash
DATABASE_URL=postgresql://postgres:postgres@db:5432/admin_financeiro
```

### 3. Banco de Dados

O sistema criará automaticamente a tabela `document_embeddings` ao iniciar.

## Uso

### Interface Web

Acesse `/rag` no navegador para usar a interface gráfica:

1. **Escolha o método**:
   - RAG Simples: Para consultas sobre dados estruturados
   - RAG Embeddings: Para busca semântica (requer indexação)

2. **Digite sua pergunta**:
   - Exemplo: "Qual o total de despesas dos últimos 30 dias?"
   - Exemplo: "Quais são os maiores fornecedores?"
   - Exemplo: "Mostre notas fiscais relacionadas a manutenção"

3. **Clique em Perguntar** ou pressione Ctrl+Enter

### API REST

#### Fazer uma pergunta

```bash
POST /api/rag/ask
Content-Type: application/json

{
  "question": "Qual o total de despesas dos últimos 30 dias?",
  "method": "simple"
}
```

Resposta:
```json
{
  "success": true,
  "question": "Qual o total de despesas dos últimos 30 dias?",
  "answer": "Nos últimos 30 dias, foram registradas...",
  "method": "RAG_SIMPLE",
  "query_type": "total_periodo",
  "data_retrieved": {...}
}
```

#### Obter exemplos de perguntas

```bash
GET /api/rag/examples
```

#### Verificar status do sistema

```bash
GET /api/rag/status
```

#### Indexar documentos (necessário para RAG Embeddings)

```bash
# Indexar todas as notas fiscais
POST /api/rag/index

# Indexar uma nota específica
POST /api/rag/index/123
```

## Arquitetura

```
rag_system/
├── __init__.py                 # Módulo principal
├── rag_simple.py              # Implementação RAG Simples
├── rag_embeddings.py          # Implementação RAG com Embeddings
└── database_retriever.py      # Recuperador de dados do BD

models/
└── document_embeddings.py     # Modelo para armazenar embeddings

routes/
└── api_routes.py              # Rotas da API RAG

frontend/
├── templates/
│   └── rag.html              # Interface de usuário
└── static/
    └── js/
        └── rag.js            # Lógica da interface
```

## Como Funciona

### RAG Simples

1. **Análise da Pergunta**: Sistema identifica o tipo de consulta (fornecedores, período, classificação, etc.)
2. **Recuperação de Dados**: Executa queries SQL otimizadas no PostgreSQL
3. **Formatação de Contexto**: Organiza os dados em formato legível
4. **Geração de Resposta**: LLM recebe contexto + pergunta e gera resposta natural

### RAG com Embeddings

1. **Indexação** (prévia):
   - Cada nota fiscal é convertida em texto
   - Modelo sentence-transformer gera vetor de 384 dimensões
   - Vetor é armazenado no banco de dados

2. **Busca**:
   - Pergunta do usuário é convertida em vetor
   - Sistema calcula similaridade de cosseno com todos os documentos
   - Retorna top-k documentos mais similares

3. **Geração de Resposta**:
   - LLM recebe documentos relevantes + pergunta
   - Gera resposta baseada no contexto semântico

## Exemplos de Perguntas

### RAG Simples (recomendado para):
- "Qual é o resumo financeiro geral?"
- "Quais são os maiores fornecedores?"
- "Qual o total de despesas dos últimos 30 dias?"
- "Mostre as despesas por classificação"
- "Liste as últimas notas fiscais processadas"

### RAG Embeddings (recomendado para):
- "Encontre notas relacionadas a manutenção de equipamentos"
- "Quais despesas estão relacionadas a recursos humanos?"
- "Mostre gastos similares ao fornecedor X"
- "Documentos sobre insumos agrícolas"

## Performance

### RAG Simples
- **Tempo de resposta**: ~2-3 segundos
- **Precisão**: Alta (dados estruturados)
- **Requer indexação**: Não

### RAG Embeddings
- **Tempo de indexação**: ~1 segundo por documento
- **Tempo de resposta**: ~3-5 segundos
- **Precisão**: Alta (busca semântica)
- **Requer indexação**: Sim (executar uma vez)

## Troubleshooting

### RAG Embeddings não inicializa

1. Verifique se sentence-transformers está instalado:
   ```bash
   pip install sentence-transformers
   ```

2. Verifique os logs do servidor para erros de carregamento do modelo

### Respostas vazias ou incorretas

1. Para RAG Embeddings: certifique-se de que os documentos foram indexados
   ```bash
   curl -X POST http://localhost:5000/api/rag/index
   ```

2. Verifique se há notas fiscais no banco de dados

### Erro de conexão com banco de dados

1. Verifique se o PostgreSQL está rodando
2. Verifique as credenciais no arquivo `.env`
3. Teste a conexão: `python teste_conexao_db.py`

## Próximos Passos

### Melhorias Planejadas

1. **Integração com pgvector**: Usar extensão nativa do PostgreSQL para busca vetorial
2. **Cache de embeddings**: Evitar recalcular embeddings de documentos
3. **Busca híbrida**: Combinar RAG Simples + Embeddings
4. **Reranking**: Melhorar ordenação de resultados
5. **Suporte a mais documentos**: PDFs, imagens, etc.

## Referências

- [Google Gemini API](https://ai.google.dev/)
- [RAG Pattern](https://python.langchain.com/docs/use_cases/question_answering/)
- [pgvector](https://github.com/pgvector/pgvector)

## Licença

Este projeto é parte de um trabalho acadêmico.
