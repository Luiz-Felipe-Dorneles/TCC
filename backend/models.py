from datetime import datetime
from database import db


# ==========================
# 🧍 Tabela de Usuários
# ==========================
from database import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    perfil = db.Column(db.String(50))
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)



# ==========================
# 📦 Tabela de Produtos
# ==========================
class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('insumo', 'produto_final'))
    preco_unit = db.Column(db.Numeric(14, 2), nullable=False)
    unidade_medida = db.Column(db.String(50))

    itens_pedido = db.relationship("ItemPedido", backref="produto", lazy=True)
    estoque = db.relationship("Estoque", uselist=False, backref="produto", lazy=True)

    def __repr__(self):
        return f"<Produto {self.nome}>"


# ==========================
# 🧾 Tabela de Pedidos
# ==========================
class Pedido(db.Model):
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(255), nullable=False)
    cliente_contato = db.Column(db.String(255))
    status = db.Column(
        db.Enum('criado', 'aprovado', 'em_producao', 'em_logistica', 'entregue', 'finalizado'),
        default='criado'
    )
    total = db.Column(db.Numeric(14, 2), nullable=False, default=0.00)
    criado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)

    def __repr__(self):
        return f"<Pedido {self.id} - {self.cliente_nome}>"


# ==========================
# 🧱 Tabela de Itens do Pedido
# ==========================
class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Numeric(14, 2), nullable=False)
    preco_unit = db.Column(db.Numeric(14, 2), nullable=False)
    total_item = db.Column(db.Numeric(14, 2), nullable=False)

    def __repr__(self):
        return f"<ItemPedido Pedido:{self.pedido_id} Produto:{self.produto_id}>"


# ==========================
# 📦 Tabela de Estoque
# ==========================
class Estoque(db.Model):
    __tablename__ = "estoque"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade_atual = db.Column(db.Numeric(14, 2), nullable=False, default=0.00)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    entradas = db.relationship("EntradaEstoque", backref="estoque", lazy=True)

    def __repr__(self):
        return f"<Estoque Produto:{self.produto_id} Quantidade:{self.quantidade_atual}>"


# ==========================
# 🧾 Tabela de Entradas de Estoque
# ==========================
class EntradaEstoque(db.Model):
    __tablename__ = "entrada_estoque"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Numeric(14, 2), nullable=False)
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    criado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    estoque_id = db.Column(db.Integer, db.ForeignKey("estoque.id"))

    def __repr__(self):
        return f"<EntradaEstoque Produto:{self.produto_id} Quantidade:{self.quantidade}>"
