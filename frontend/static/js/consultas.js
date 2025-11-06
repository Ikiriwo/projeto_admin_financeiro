/**
 * Script para a página de consultas ao banco de dados
 */

// Função para limpar máscara de documento
function limparMascaraDocumento(doc) {
    return (doc || '').toString().replace(/\D/g, '');
}

// Função para definir badge de status
function setBadge(id, status) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove('status-success', 'status-error');
    if (status === 'success') {
        el.classList.add('status-success');
        el.textContent = '✅ EXISTE';
    } else if (status === 'error') {
        el.classList.add('status-error');
        el.textContent = '❌ NÃO EXISTE';
    } else {
        el.textContent = 'Aguardando...';
    }
}

// Função auxiliar para fazer requisições GET
async function getJSON(url) {
    const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) throw new Error('Falha: ' + res.status);
    return await res.json();
}

// Inicialização quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Event listener para consulta de pessoas
    document.getElementById('btn-consultar-pessoas').addEventListener('click', async () => {
        const tipo = document.getElementById('tipoPessoa').value;
        const doc = limparMascaraDocumento(document.getElementById('docPessoa').value);
        try {
            const resp = await getJSON(`/pessoas?tipo=${encodeURIComponent(tipo)}&documento=${encodeURIComponent(doc)}`);
            setBadge('status-consulta-pessoas', resp.existe ? 'success' : 'error');
            document.getElementById('resp-consulta-pessoas').textContent = JSON.stringify(resp, null, 2);
        } catch (e) {
            setBadge('status-consulta-pessoas', 'error');
            document.getElementById('resp-consulta-pessoas').textContent = e.toString();
        }
    });

    // Event listener para consulta de classificação
    document.getElementById('btn-consultar-class').addEventListener('click', async () => {
        const desc = document.getElementById('descClass').value;
        try {
            const resp = await getJSON(`/classificacao?descricao=${encodeURIComponent(desc)}`);
            setBadge('status-consulta-class', resp.existe ? 'success' : 'error');
            document.getElementById('resp-consulta-class').textContent = JSON.stringify(resp, null, 2);
        } catch (e) {
            setBadge('status-consulta-class', 'error');
            document.getElementById('resp-consulta-class').textContent = e.toString();
        }
    });
});
