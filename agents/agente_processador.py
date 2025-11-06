"""
Agente que decide qual ferramenta usar para a tarefa.
"""


class AgenteProcessador:
    """Agente que decide qual ferramenta usar para a tarefa."""

    def __init__(self, ferramentas):
        self.ferramentas = ferramentas

    def executar_tarefa(self, tarefa, dados):
        """Executa a tarefa usando a ferramenta apropriada."""
        if "processar nota fiscal" in tarefa.lower():
            ferramenta = self.ferramentas.get("processador_nf")
            if ferramenta:
                return ferramenta.executar()
        return None
