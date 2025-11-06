"""
Ferramenta para extrair dados de notas fiscais usando a API do Gemini.
"""
import json
import google.generativeai as genai


class ProcessadorDeNotaFiscalTool:
    """Ferramenta para extrair dados de notas fiscais usando a API do Gemini."""

    def __init__(self, invoice_text, model):
        self.invoice_text = invoice_text
        self.model = model

    def executar(self):
        """Extrai dados da nota fiscal e retorna um dicionário JSON."""
        prompt_text = self._criar_prompt()
        return self._processar_resposta(prompt_text)

    def _criar_prompt(self):
        """Cria o prompt para a API do Gemini."""
        return f"""
Extraia os seguintes dados do texto da nota fiscal fornecido.

A saída deve ser um **objeto JSON único e bem formatado**, sem qualquer texto adicional antes ou depois.

A estrutura do JSON deve seguir o seguinte modelo. Para valores decimais, use ponto (.) como separador, não vírgula (,).

Abaixo está a estrutura do JSON, lembre-se que em 'Descricao Produtos' considere somente a descrição do produto sem considerar o codigo do produto.

{{
  "Fornecedor": {{
    "Razao Social": "...",
    "CNPJ": "..."
  }},
  "Faturado": {{
    "Nome": "...",
    "CPF": "..."
  }},
  "Nota Fiscal": "...",
  "Data Emissao": "AAAA-MM-DD",
  "Data de Validade": "AAAA-MM-DD",
  "Descricao Produtos": [
    "Produto",
    "Produto"
  ],
  "Valor Total": 0.0,
  "Quantidade de Parcelas": 0,
  "Classificacao_Despesa": "..."
}}

IMPORTANTE: Use "Classificacao_Despesa" (com underscore) como chave no JSON, não use "Classificacao Despesa".

Categorias para Classificacao_Despesa:
- INSUMOS_AGRICOLAS
- MANUTENCAO_E_OPERACAO
- RECURSOS_HUMANOS
- SERVICOS_OPERACIONAIS
- INFRASTRUTURA_E_UTILIDADES
- ADMINISTRATIVAS
- SEGUROS_E_PROTECAO
- IMPOSTOS_E_TAXAS
- INVESTIMENTOS
- OUTROS

Classifique a despesa de acordo com os produtos na nota fiscal:
- Para itens como 'Sementes', 'Fertilizantes', 'Defensivos Agrícolas', 'Corretivos', classifique como **INSUMOS_AGRICOLAS**.
- Para itens como 'Combustíveis', 'Lubrificantes', 'Peças', 'Parafusos', 'Manutenção de Máquinas', 'Pneus', 'Filtros', 'Correias', 'Ferramentas', 'Utensílios', classifique como **MANUTENCAO_E_OPERACAO**.
- Para itens como 'Mão de Obra Temporária', 'Salários', 'Encargos', classifique como **RECURSOS_HUMANOS**.
- Para itens como 'Frete', 'Transporte', 'Colheita Terceirizada', 'Secagem', 'Armazenagem', 'Pulverização', 'Aplicação', classifique como **SERVICOS_OPERACIONAIS**.
- Para itens como 'Energia Elétrica', 'Arrendamento de Terras', 'Construções', 'Reformas', 'Materiais de Construção', classifique como **INFRASTRUTURA_E_UTILIDADES**.
- Para itens como 'Honorários Contábeis', 'Honorários Advocatícios', 'Despesas Bancárias', 'Despesas Financeiras', classifique como **ADMINISTRATIVAS**.
- Para itens como 'Seguro Agrícola', 'Seguro de Ativos', 'Seguro de Veículos', 'Seguro Prestamista', classifique como **SEGUROS_E_PROTECAO**.
- Para itens como 'ITR', 'IPTU', 'IPVA', 'INCRA-CCIR', 'Impostos', 'Taxas', classifique como **IMPOSTOS_E_TAXAS**.
- Para itens como 'Aquisição de Máquinas', 'Implementos', 'Veículos', 'Imóveis', 'Infraestrutura Rural', classifique como **INVESTIMENTOS**.
- Para todos os outros itens que não se encaixem nas categorias acima, classifique como **OUTROS**.

Texto da nota fiscal:
{self.invoice_text}
"""

    def _processar_resposta(self, prompt_text):
        """Processa a resposta da API do Gemini."""
        try:
            response = self.model.generate_content(prompt_text)
            response_text = response.text.strip().replace("```json\n", "").replace("\n```", "").strip()
            return json.loads(response_text)
        except Exception as e:
            print(f"Erro na ferramenta: {e}")
            return None
