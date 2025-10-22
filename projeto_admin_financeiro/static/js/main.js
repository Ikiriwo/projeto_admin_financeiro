// JavaScript principal para o sistema de administração financeira

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização de tooltips do Bootstrap (se necessário)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Exemplo de função para formatar valores monetários
    window.formatarMoeda = function(valor) {
        return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    };

    // Exemplo de função para confirmar exclusão
    window.confirmarExclusao = function(id, tipo) {
        return confirm(`Tem certeza que deseja excluir esta ${tipo} (ID: ${id})?`);
    };
});

// ==========================
// Validação e Integração API
// ==========================
(function() {
    const qs = (sel) => document.querySelector(sel);

    function limparMascaraDocumento(doc) {
        return (doc || '').toString().replace(/\D/g, '');
    }

    function setBadge(id, status) {
        const el = qs(`#${id}`);
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

    function setIdField(id, value) {
        const el = qs(`#${id}`);
        if (el) el.textContent = value ?? '—';
    }

    function toggleButton(id, show) {
        const el = qs(`#${id}`);
        if (el) el.style.display = show ? 'inline-block' : 'none';
    }

    async function getJSON(url) {
        const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
        if (!res.ok) throw new Error(`Falha na requisição: ${res.status}`);
        return await res.json();
    }

    async function postJSON(url, body) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(`Falha no POST: ${res.status}`);
        return await res.json();
    }

    // Controla habilitação do botão Confirmar
    function updateConfirmButtonState() {
        const fornecedorId = (qs('#resumo-id-fornecedor')?.textContent || '—').trim();
        const faturadoId = (qs('#resumo-id-faturado')?.textContent || '—').trim();
        const classId = (qs('#resumo-id-classificacao')?.textContent || '—').trim();
        const btn = qs('#btn-confirmar');
        if (!btn) return;
        const podeConfirmar = fornecedorId !== '—' && faturadoId !== '—' && classId !== '—';
        btn.disabled = !podeConfirmar;
    }

    // Validação principal
    window.validarDados = async function(dados) {
        const feedbackEl = qs('#feedback-validacao');
        if (feedbackEl) {
            feedbackEl.textContent = '🕓 Validando informações…';
        }
        try {
            // Fornecedor
            const cnpj = limparMascaraDocumento(dados['Fornecedor']['CNPJ']);
            const fornecedorQuery = `/pessoas?tipo=FORNECEDOR&documento=${encodeURIComponent(cnpj)}`;
            const fornecedorResp = await getJSON(fornecedorQuery);
            if (fornecedorResp.existe) {
                setBadge('status-fornecedor', 'success');
                setIdField('id-fornecedor', fornecedorResp.id);
                setIdField('resumo-id-fornecedor', fornecedorResp.id);
                toggleButton('btn-cadastrar-fornecedor', false);
            } else {
                setBadge('status-fornecedor', 'error');
                setIdField('id-fornecedor', '—');
                toggleButton('btn-cadastrar-fornecedor', true);
            }

            // Faturado
            const cpf = limparMascaraDocumento(dados['Faturado']['CPF']);
            const faturadoQuery = `/pessoas?tipo=FATURADO&documento=${encodeURIComponent(cpf)}`;
            const faturadoResp = await getJSON(faturadoQuery);
            if (faturadoResp.existe) {
                setBadge('status-faturado', 'success');
                setIdField('id-faturado', faturadoResp.id);
                setIdField('resumo-id-faturado', faturadoResp.id);
                toggleButton('btn-cadastrar-faturado', false);
            } else {
                setBadge('status-faturado', 'error');
                setIdField('id-faturado', '—');
                toggleButton('btn-cadastrar-faturado', true);
            }

            // Classificação
            const classDesc = dados['Classificacao Despesa'];
            const classQuery = `/classificacao?descricao=${encodeURIComponent(classDesc)}`;
            const classResp = await getJSON(classQuery);
            if (classResp.existe) {
                setBadge('status-classificacao', 'success');
                setIdField('id-classificacao', classResp.id);
                setIdField('resumo-id-classificacao', classResp.id);
                toggleButton('btn-cadastrar-classificacao', false);
            } else {
                setBadge('status-classificacao', 'error');
                setIdField('id-classificacao', '—');
                toggleButton('btn-cadastrar-classificacao', true);
            }

            if (feedbackEl) {
                feedbackEl.textContent = '✔️ Validação concluída.';
            }
            updateConfirmButtonState();
        } catch (err) {
            console.error(err);
            if (feedbackEl) feedbackEl.textContent = '❌ Erro ao validar. Verifique a API.';
            updateConfirmButtonState();
        }
    }

    // Cadastro de registros inexistentes
    window.cadastrarFornecedor = async function(dados) {
        const cnpj = limparMascaraDocumento(dados['Fornecedor']['CNPJ']);
        const feedbackEl = qs('#feedback-validacao');
        try {
            const resp = await postJSON('/pessoas', {
                tipo: 'FORNECEDOR',
                nome: dados['Fornecedor']['Razao Social'],
                documento: cnpj
            });
            setBadge('status-fornecedor', 'success');
            setIdField('id-fornecedor', resp.id);
            setIdField('resumo-id-fornecedor', resp.id);
            toggleButton('btn-cadastrar-fornecedor', false);
            if (feedbackEl) feedbackEl.textContent = '✅ Fornecedor cadastrado com sucesso!';
            updateConfirmButtonState();
        } catch (err) {
            if (feedbackEl) feedbackEl.textContent = '❌ Erro ao cadastrar fornecedor.';
            updateConfirmButtonState();
        }
    }

    window.cadastrarFaturado = async function(dados) {
        const cpf = limparMascaraDocumento(dados['Faturado']['CPF']);
        const feedbackEl = qs('#feedback-validacao');
        try {
            const resp = await postJSON('/pessoas', {
                tipo: 'FATURADO',
                nome: dados['Faturado']['Nome'],
                documento: cpf
            });
            setBadge('status-faturado', 'success');
            setIdField('id-faturado', resp.id);
            setIdField('resumo-id-faturado', resp.id);
            toggleButton('btn-cadastrar-faturado', false);
            if (feedbackEl) feedbackEl.textContent = '✅ Faturado cadastrado com sucesso!';
            updateConfirmButtonState();
        } catch (err) {
            if (feedbackEl) feedbackEl.textContent = '❌ Erro ao cadastrar faturado.';
            updateConfirmButtonState();
        }
    }

    window.cadastrarClassificacao = async function(dados) {
        const classDesc = dados['Classificacao Despesa'];
        const feedbackEl = qs('#feedback-validacao');
        try {
            const resp = await postJSON('/classificacao', {
                descricao: classDesc
            });
            setBadge('status-classificacao', 'success');
            setIdField('id-classificacao', resp.id);
            setIdField('resumo-id-classificacao', resp.id);
            toggleButton('btn-cadastrar-classificacao', false);
            if (feedbackEl) feedbackEl.textContent = '✅ Classificação cadastrada com sucesso!';
            updateConfirmButtonState();
        } catch (err) {
            if (feedbackEl) feedbackEl.textContent = '❌ Erro ao cadastrar classificação.';
            updateConfirmButtonState();
        }
    }

    window.confirmarLancamento = async function(dados) {
        const feedbackEl = qs('#feedback-lancamento');
        const fornecedorId = qs('#resumo-id-fornecedor').textContent.trim();
        const faturadoId = qs('#resumo-id-faturado').textContent.trim();
        const classId = qs('#resumo-id-classificacao').textContent.trim();
        if (!fornecedorId || !faturadoId || !classId || fornecedorId === '—' || faturadoId === '—' || classId === '—') {
            feedbackEl.textContent = '❌ Valide/cadastre Fornecedor, Faturado e Classificação antes de confirmar.';
            return;
        }
        try {
            feedbackEl.textContent = '🕓 Registrando movimento…';
            const movimento = await postJSON('/movimentos', {
                fornecedor_id: Number(fornecedorId),
                faturado_id: Number(faturadoId),
                classificacao_id: Number(classId),
                valor_total: dados['Valor Total'],
                data_emissao: dados['Data Emissao'],
                tipo: 'A_PAGAR'
            });

            const qtdParcelas = Number(dados['Quantidade de Parcelas'] || 0);
            if (qtdParcelas > 0) {
                const valorParcela = (Number(dados['Valor Total']) / qtdParcelas);
                for (let i = 1; i <= qtdParcelas; i++) {
                    try {
                        await postJSON('/parcelas', {
                            movimento_id: movimento.id,
                            parcela: i,
                            valor: valorParcela
                        });
                    } catch (errParcela) {
                        console.warn('Falha ao criar parcela', i, errParcela);
                    }
                }
            }

            feedbackEl.textContent = '✅ Registro lançado com sucesso!';
        } catch (err) {
            console.error(err);
            feedbackEl.textContent = '❌ Erro ao lançar registro.';
        }
    }
})();