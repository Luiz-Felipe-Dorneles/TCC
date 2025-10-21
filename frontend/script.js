// Função para mostrar seção
function showSection(id) {
  document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
  document.getElementById(id).style.display = 'block';
}

// ===== Produtos =====
let produtos = JSON.parse(localStorage.getItem('produtos') || '[]');

function updateProdutosTable() {
  const tbody = document.querySelector('#produtos-table tbody');
  tbody.innerHTML = '';
  produtos.forEach(p => {
    tbody.innerHTML += `<tr><td>${p.nome}</td><td>${p.preco.toFixed(2)}</td><td>${p.estoque}</td></tr>`;
  });
}
document.getElementById('produto-form').addEventListener('submit', e => {
  e.preventDefault();
  const nome = document.getElementById('produto-nome').value;
  const preco = parseFloat(document.getElementById('produto-preco').value);
  const estoque = parseInt(document.getElementById('produto-estoque').value);
  produtos.push({nome, preco, estoque});
  localStorage.setItem('produtos', JSON.stringify(produtos));
  updateProdutosTable();
  document.getElementById('produto-form').reset();
  updateEstoqueTable();
  updateFaturamentoSelects();
});
updateProdutosTable();

// ===== Clientes =====
let clientes = JSON.parse(localStorage.getItem('clientes') || '[]');
function updateClientesTable() {
  const tbody = document.querySelector('#clientes-table tbody');
  tbody.innerHTML = '';
  clientes.forEach(c => {
    tbody.innerHTML += `<tr><td>${c.nome}</td><td>${c.email}</td></tr>`;
  });
}
document.getElementById('cliente-form').addEventListener('submit', e => {
  e.preventDefault();
  const nome = document.getElementById('cliente-nome').value;
  const email = document.getElementById('cliente-email').value;
  clientes.push({nome, email});
  localStorage.setItem('clientes', JSON.stringify(clientes));
  updateClientesTable();
  document.getElementById('cliente-form').reset();
  updateFaturamentoSelects();
});
updateClientesTable();

// ===== Estoque =====
function updateEstoqueTable() {
  const tbody = document.querySelector('#estoque-table tbody');
  tbody.innerHTML = '';
  produtos.forEach(p => {
    tbody.innerHTML += `<tr><td>${p.nome}</td><td>${p.estoque}</td></tr>`;
  });
}
updateEstoqueTable();

// ===== Faturamento =====
let faturamentos = JSON.parse(localStorage.getItem('faturamentos') || '[]');

function updateFaturamentoSelects() {
  const clienteSelect = document.getElementById('fatura-cliente');
  const produtoSelect = document.getElementById('fatura-produto');
  clienteSelect.innerHTML = '<option value="">Selecione Cliente</option>';
  produtoSelect.innerHTML = '<option value="">Selecione Produto</option>';
  clientes.forEach((c,i)=> clienteSelect.innerHTML += `<option value="${i}">${c.nome}</option>`);
  produtos.forEach((p,i)=> produtoSelect.innerHTML += `<option value="${i}">${p.nome}</option>`);
}

function updateFaturamentoTable() {
  const tbody = document.querySelector('#faturamento-table tbody');
  tbody.innerHTML = '';
  faturamentos.forEach(f => {
    tbody.innerHTML += `<tr><td>${clientes[f.cliente].nome}</td>
                        <td>${produtos[f.produto].nome}</td>
                        <td>${f.quantidade}</td>
                        <td>${f.total.toFixed(2)}</td></tr>`;
  });
}

document.getElementById('faturamento-form').addEventListener('submit', e => {
  e.preventDefault();
  const cliente = parseInt(document.getElementById('fatura-cliente').value);
  const produto = parseInt(document.getElementById('fatura-produto').value);
  const quantidade = parseInt(document.getElementById('fatura-quantidade').value);
  const total = produtos[produto].preco * quantidade;
  faturamentos.push({cliente, produto, quantidade, total});
  localStorage.setItem('faturamentos', JSON.stringify(faturamentos));

  // Atualiza estoque
  produtos[produto].estoque -= quantidade;
  localStorage.setItem('produtos', JSON.stringify(produtos));

  updateFaturamentoTable();
  updateEstoqueTable();
  document.getElementById('faturamento-form').reset();
});
updateFaturamentoSelects();
updateFaturamentoTable();
