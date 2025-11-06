/**
 * Script para a página de upload de nota fiscal
 */

// Script para mostrar o nome do arquivo selecionado
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('file').addEventListener('change', function() {
        var fileName = this.files[0] ? this.files[0].name : 'Nenhum arquivo selecionado';
        document.getElementById('file-name').textContent = fileName;
    });
});
