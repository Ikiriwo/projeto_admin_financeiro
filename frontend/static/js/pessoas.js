// Variáveis globais
let pessoasData = [];
let ordemAscendente = true;

// Carregar todos os registros ATIVOS
function carregarTodos() {
    const incluirInativos = document.getElementById('incluirInativos').checked;
    const url = `/api/pessoas?incluir_inativos=${incluirInativos}`;

    fetch(url)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                pessoasData = result.data;
                renderizarTabela(pessoasData);
                atualizarContador(pessoasData.length);
            } else {
                alert('Erro ao carregar pessoas: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar pessoas');
        });
}

// Buscar com filtros
function carregarPessoas() {
    const tipo = document.getElementById('filtroTipo').value;
    const busca = document.getElementById('filtroBusca').value.toLowerCase();
    const incluirInativos = document.getElementById('incluirInativos').checked;

    const url = `/api/pessoas?tipo=${tipo}&incluir_inativos=${incluirInativos}`;

    fetch(url)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                let dados = result.data;

                // Filtrar por busca local (razão social ou CPF/CNPJ)
                if (busca) {
                    dados = dados.filter(p =>
                        p.razao_social.toLowerCase().includes(busca) ||
                        p.cpf_cnpj.includes(busca)
                    );
                }

                pessoasData = dados;
                renderizarTabela(pessoasData);
                atualizarContador(pessoasData.length);
            } else {
                alert('Erro ao buscar pessoas: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao buscar pessoas');
        });
}

// Renderizar tabela
function renderizarTabela(dados) {
    const tbody = document.getElementById('tbodyPessoas');

    if (dados.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted">
                    <i class="fas fa-inbox"></i> Nenhum registro encontrado
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = dados.map(pessoa => `
        <tr>
            <td>${pessoa.id}</td>
            <td><span class="badge badge-info">${pessoa.tipo}</span></td>
            <td>${pessoa.razao_social}</td>
            <td>${pessoa.cpf_cnpj}</td>
            <td>
                <span class="badge badge-${pessoa.status === 'ATIVO' ? 'success' : 'danger'}">
                    ${pessoa.status}
                </span>
            </td>
            <td>${formatarData(pessoa.data_cadastro)}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-warning" onclick="abrirModalEditar(${pessoa.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger" onclick="excluirPessoa(${pessoa.id})" title="Excluir"
                            ${pessoa.status === 'INATIVO' ? 'disabled' : ''}>
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Ordenar tabela por coluna
function ordenarTabela(coluna) {
    const campos = ['id', 'tipo', 'razao_social', 'cpf_cnpj', 'status', 'data_cadastro'];
    const campo = campos[coluna];

    pessoasData.sort((a, b) => {
        let valorA = a[campo];
        let valorB = b[campo];

        if (campo === 'id') {
            return ordemAscendente ? valorA - valorB : valorB - valorA;
        }

        if (valorA < valorB) return ordemAscendente ? -1 : 1;
        if (valorA > valorB) return ordemAscendente ? 1 : -1;
        return 0;
    });

    ordemAscendente = !ordemAscendente;
    renderizarTabela(pessoasData);
}

// Abrir modal para criar
function abrirModalCriar() {
    document.getElementById('modalTitulo').textContent = 'Nova Pessoa';
    document.getElementById('formPessoa').reset();
    document.getElementById('pessoaId').value = '';
    document.getElementById('pessoaStatus').value = 'ATIVO';
    $('#modalPessoa').modal('show');
}

// Abrir modal para editar
function abrirModalEditar(id) {
    fetch(`/api/pessoas/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                const pessoa = result.data;
                document.getElementById('modalTitulo').textContent = 'Editar Pessoa';
                document.getElementById('pessoaId').value = pessoa.id;
                document.getElementById('pessoaTipo').value = pessoa.tipo;
                document.getElementById('pessoaRazaoSocial').value = pessoa.razao_social;
                document.getElementById('pessoaCpfCnpj').value = pessoa.cpf_cnpj;
                document.getElementById('pessoaStatus').value = pessoa.status;
                $('#modalPessoa').modal('show');
            } else {
                alert('Erro ao carregar pessoa: ' + result.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao carregar pessoa');
        });
}

// Salvar pessoa (criar ou atualizar)
function salvarPessoa() {
    const id = document.getElementById('pessoaId').value;
    const tipo = document.getElementById('pessoaTipo').value;
    const razaoSocial = document.getElementById('pessoaRazaoSocial').value;
    const cpfCnpj = document.getElementById('pessoaCpfCnpj').value;

    if (!tipo || !razaoSocial || !cpfCnpj) {
        alert('Preencha todos os campos obrigatórios');
        return;
    }

    const dados = {
        tipo: tipo,
        razao_social: razaoSocial,
        cpf_cnpj: cpfCnpj
    };

    const url = id ? `/api/pessoas/${id}` : '/api/pessoas';
    const metodo = id ? 'PUT' : 'POST';

    fetch(url, {
        method: metodo,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(result.message);
            $('#modalPessoa').modal('hide');
            carregarTodos();
        } else {
            alert('Erro: ' + result.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar pessoa');
    });
}

// Excluir pessoa (exclusão lógica)
function excluirPessoa(id) {
    if (!confirm('Deseja realmente excluir esta pessoa? (Exclusão lógica)')) {
        return;
    }

    fetch(`/api/pessoas/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(result.message);
            carregarTodos();
        } else {
            alert('Erro: ' + result.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao excluir pessoa');
    });
}

// Formatar data
function formatarData(dataISO) {
    if (!dataISO) return '';
    const data = new Date(dataISO);
    return data.toLocaleDateString('pt-BR') + ' ' + data.toLocaleTimeString('pt-BR');
}

// Atualizar contador de registros
function atualizarContador(total) {
    document.getElementById('contadorRegistros').textContent = `${total} registro(s) encontrado(s)`;
}
