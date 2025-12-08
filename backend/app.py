from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_app, db
from models import (
    Usuario, Produto, Variante, Estoque, MovimentoEstoque,
    Pedido, ItemPedido, Insumo, Cliente, Endereco,
    registrar_entrada_variante, registrar_saida_variante,
    calcular_custo_producao, calcular_preco_venda
)
import os
import re
from datetime import datetime

# Diretórios
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, "../frontend")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=TEMPLATE_DIR)
init_app(app)

# 🔴 NOVO: CHAVE SECRETA OBRIGATÓRIA PARA SESSÕES
app.secret_key = "a_chave_secreta_segura_para_mev_glass"

# -------------------
# Páginas (com verificação de login no /inicio)
# -------------------
@app.route("/inicio")
def inicio_page():
    # 🟢 NOVO: Se não estiver logado, redireciona para o login
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Envia o nome do usuário logado para o template
    return render_template("inicio.html", nome_usuario=session.get('user_nome'))

@app.route("/")
def index():
    # Se já estiver logado, redireciona para o início
    if 'user_id' in session:
        return redirect(url_for('inicio_page'))
    return render_template("login.html")

@app.route("/register_page")
def register_page():
    return render_template("criar_conta.html")

# Rotas que não mudam (mantidas por segurança)
@app.route("/produtos")
def produtos_page():
    return render_template("produtos.html")

@app.route("/clientes")
def clientes_page():
    return render_template("clientes.html")

@app.route("/lista_cliente")
def lista_cliente_page():
    return render_template("lista_clientes.html")

@app.route("/estoque")
def estoque_page():
    return render_template("estoque.html")

@app.route("/faturamento")
def faturamento_page():
    return render_template("faturamento.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@app.route("/relatorios")
def relatorios_page():
    return render_template("relatorios.html")


# -------------------
# Util: gerar SKU simples
# -------------------
def gerar_sku_from_fields(produto_linha: str, altura=None, largura=None, cor=None, moldura=None):
    base = re.sub(r'[^A-Za-z0-9]', '', produto_linha[:3]).upper()
    parts = [base]
    if altura:
        parts.append(str(altura).replace('.', '').replace(',', ''))
    if largura:
        parts.append(str(largura).replace('.', '').replace(',', ''))
    if cor:
        parts.append(re.sub(r'[^A-Za-z0-9]', '', cor)[:6].upper())
    if moldura:
        parts.append(re.sub(r'[^A-Za-z0-9]', '', moldura)[:4].upper())
    sku = "-".join(parts)
    return sku[:60]


# -------------------
# Rotas de autenticação / registro
# -------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify(status="erro", mensagem="Preencha todos os campos"), 400

    if Usuario.query.filter_by(email=email.lower()).first():
        return jsonify(status="erro", mensagem="E-mail já cadastrado"), 400

    try:
        user = Usuario(
            nome=nome.lower() if nome else None,
            perfil="cliente",
            email=email.lower(),
            senha_hash=generate_password_hash(senha)
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(status="ok", mensagem="Conta criada com sucesso!")
    except Exception as e:
        db.session.rollback()
        return jsonify(status="erro", mensagem=str(e))


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify(status="erro", mensagem="Preencha todos os campos"), 400

    user = Usuario.query.filter_by(email=email.lower()).first()
    if not user:
        return jsonify(status="erro", mensagem="Conta não encontrada"), 401

    if not check_password_hash(user.senha_hash, senha):
        return jsonify(status="erro", mensagem="Senha incorreta"), 401

    # 🟢 NOVO: Salva dados na Sessão do Flask (Server-Side)
    session['user_id'] = user.id
    session['user_nome'] = user.nome
    session['user_email'] = user.email

    # Não precisa retornar o nome no JSON, o Flask Session cuida do estado
    return jsonify(status="ok", mensagem="Login realizado com sucesso")


@app.route("/logout")
def logout():
    # 🟢 NOVO: Limpa a sessão e redireciona para o login
    session.clear()
    return redirect(url_for('index'))


# -------------------
# Teste DB
# -------------------
@app.route("/teste_db")
def teste_db():
    try:
        db.session.execute("SELECT 1")
        return "✅ Conectado ao banco!"
    except Exception as e:
        return f"❌ Erro ao conectar: {e}"


# -------------------
# Endpoints CRUD, Estoque, Pedidos e Atividades (Mantidos)
# -------------------
@app.route("/produto/variantes", methods=["POST"])
def criar_produto_com_variantes():
    """
    Cria um novo produto e suas variantes.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "payload JSON required"}), 400

    linha = data.get("linha")
    formato = data.get("formato")
    descricao = data.get("descricao")
    imagem_url = data.get("imagem_url")
    variantes = data.get("variantes", [])

    if not linha or not formato:
        return jsonify({"error": "linha and formato required"}), 400

    produto = Produto(
        linha=linha,
        formato=formato,
        descricao=descricao,
        imagem_url=imagem_url
    )
    try:
        db.session.add(produto)
        db.session.flush()

        resposta_variantes = []
        for v in variantes:
            altura = v.get("altura_cm")
            largura = v.get("largura_cm")
            cor = v.get("cor")
            moldura = v.get("moldura")
            insumos_data = v.get("insumos", [])

            sku_base = gerar_sku_from_fields(linha, altura, largura, cor, moldura)
            sku = sku_base
            i = 1
            while Variante.query.filter_by(sku=sku).first():
                i += 1
                sku = f"{sku_base}-{i}"

            variante = Variante(
                produto_id=produto.id,
                altura_cm=altura,
                largura_cm=largura,
                cor=cor,
                led_direto=bool(v.get("led_direto", False)),
                led_indireto=bool(v.get("led_indireto", False)),
                moldura=moldura,
                sku=sku,
                preco_base=0,  # Será calculado depois dos insumos
                ativo=True
            )
            db.session.add(variante)
            db.session.flush()

            # Adicionar insumos
            for insumo_data in insumos_data:
                insumo = Insumo(
                    variante_id=variante.id,
                    material=insumo_data.get("material"),
                    quantidade=insumo_data.get("quantidade"),
                    custo_unitario=insumo_data.get("custo_unitario", 0),
                    unidade_medida=insumo_data.get("unidade_medida", "un")
                )
                db.session.add(insumo)
            
            db.session.flush()

            # Calcular preço base automaticamente ou usar o fornecido
            preco_fornecido = v.get("preco_base")
            if preco_fornecido:
                variante.preco_base = preco_fornecido
            else:
                # Calcular automaticamente baseado nos insumos
                variante.preco_base = variante.preco_venda_sugerido

            estoque = Estoque(
                variante_id=variante.id,
                quantidade=int(v.get("estoque_inicial", 0)),
                minimo=int(v.get("minimo", 0))
            )
            db.session.add(estoque)

            resposta_variantes.append({
                "variante_id": variante.id,
                "sku": sku,
                "custo_producao": float(variante.custo_producao),
                "preco_venda_sugerido": float(variante.preco_venda_sugerido),
                "preco_base": str(variante.preco_base),
                "estoque_inicial": int(v.get("estoque_inicial", 0))
            })

        db.session.commit()
        return jsonify({"produto_id": produto.id, "variantes": resposta_variantes}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/produto/catalogo", methods=["GET"])
def listar_catalogo():
    """ Retorna todas as variantes ativas com dados do produto e estoque. """
    q = db.session.query(Produto, Variante, Estoque) \
        .join(Variante, Variante.produto_id == Produto.id) \
        .outerjoin(Estoque, Estoque.variante_id == Variante.id) \
        .filter(Produto.ativo == True, Variante.ativo == True) \
        .all()

    resultado = []
    for prod, var, est in q:
        resultado.append({
    "produto_id": prod.id,
    "nome_produto": f"{prod.linha} {prod.formato}",
    "linha": prod.linha,
    "formato": prod.formato,
    "variante_id": var.id,
    "sku": var.sku,
    "altura_cm": float(var.altura_cm) if var.altura_cm is not None else None,
    "largura_cm": float(var.largura_cm) if var.largura_cm is not None else None,
    "cor": var.cor,
    "moldura": var.moldura,
    "preco_base": str(var.preco_base),
    "estoque": int(est.quantidade) if est is not None else 0
})
    return jsonify(resultado)


@app.route("/estoque/variantes", methods=["GET"])
def listar_variantes_estoque():
    variantes = Variante.query.filter_by(ativo=True).all()
    resp = []
    for v in variantes:
        est = v.estoque
        resp.append({
            "variante_id": v.id,
            "produto_id": v.produto_id,
            "nome_produto": v.produto.linha,
            "formato": v.produto.formato,
            "sku": v.sku,
            "altura_cm": float(v.altura_cm) if v.altura_cm is not None else None,
            "largura_cm": float(v.largura_cm) if v.largura_cm is not None else None,
            "cor": v.cor,
            "moldura": v.moldura,
            "preco_base": str(v.preco_base),
            "estoque": int(est.quantidade) if est else 0,
            "minimo": int(est.minimo) if est else 0
        })
    return jsonify(resp)

@app.route("/estoque/entrada_sku", methods=["POST"])
def entrada_sku():
    """ Payload: { "variante_id": 1, "quantidade": 5, "usuario_id": 1, "motivo": "compra" } """
    data = request.get_json()
    variante_id = data.get("variante_id")
    quantidade = int(data.get("quantidade", 0))
    usuario_id = data.get("usuario_id")
    motivo = data.get("motivo", "Entrada manual")

    if not variante_id or quantidade <= 0:
        return jsonify({"error": "variante_id and quantidade>0 required"}), 400

    try:
        novo = registrar_entrada_variante(variante_id=variante_id, quantidade=quantidade, usuario_id=usuario_id, motivo=motivo)
        return jsonify({"status": "ok", "estoque_atual": novo})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@app.route("/estoque/saida_sku", methods=["POST"])
def saida_sku():
    """ Payload: { "variante_id": 1, "quantidade": 2, "usuario_id": 1, "motivo": "venda" } """
    data = request.get_json()
    variante_id = data.get("variante_id")
    quantidade = int(data.get("quantidade", 0))
    usuario_id = data.get("usuario_id")
    motivo = data.get("motivo", "Saída por pedido")

    if not variante_id or quantidade <= 0:
        return jsonify({"error": "variante_id and quantidade>0 required"}), 400

    try:
        novo = registrar_saida_variante(variante_id=variante_id, quantidade=quantidade, usuario_id=usuario_id, motivo=motivo)
        return jsonify({"status": "ok", "estoque_atual": novo})
    except ValueError as ve:
        return jsonify({"status": "erro", "mensagem": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/estoque/entrada", methods=["POST"])
def entrada_estoque_compat():
    """ Endpoint legado: tenta localizar variante pelo produto e incrementar estoque da primeira variante. """
    data = request.get_json()
    produto_id = data.get("produto_id")
    quantidade = int(data.get("quantidade", 0))
    usuario_id = data.get("usuario_id")

    if not produto_id or quantidade <= 0:
        return jsonify({"status": "erro", "mensagem": "produto_id and quantidade>0 required"}), 400

    variante = Variante.query.filter_by(produto_id=produto_id, ativo=True).first()
    if not variante:
        return jsonify({"status": "erro", "mensagem": "Nenhuma variante encontrada para o produto"}), 404

    try:
        novo = registrar_entrada_variante(variante_id=variante.id, quantidade=quantidade, usuario_id=usuario_id, motivo="Entrada compatibilidade produto")
        return jsonify({"status": "ok", "estoque_atual": novo})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@app.route("/pedido/confirmar", methods=["POST"])
def confirmar_pedido():
    data = request.get_json()
    item_id = data.get("item_pedido_id")
    usuario_id = data.get("usuario_id")

    if not item_id:
        return jsonify({"status": "erro", "mensagem": "item_pedido_id required"}), 400

    item = ItemPedido.query.get(item_id)
    if not item:
        return jsonify({"status": "erro", "mensagem": "Item não encontrado"}), 404

    try:
        novo = registrar_saida_variante(variante_id=item.variante_id, quantidade=int(item.quantidade), usuario_id=usuario_id, motivo="Saída por confirmação de pedido")
        return jsonify({"status": "ok", "estoque_atual": novo})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


@app.route('/api/clientes', methods=['GET'])
def api_clientes():
    clientes = Usuario.query.all()
    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "email": c.email
        }
        for c in clientes
    ])


@app.route('/pedido/criar', methods=['POST'])
def criar_pedido():
    data = request.get_json()

    cliente_nome = data.get("cliente_nome")
    
    if not cliente_nome and data.get("cliente_id"):
        cliente_nome = f"Cliente ID {data.get('cliente_id')}"

    itens = data.get("itens", [])

    if not cliente_nome:
        return jsonify({"error": "Nome do cliente é obrigatório"}), 400
    if not itens:
        return jsonify({"error": "Nenhum item no pedido"}), 400

    usuario_responsavel = 1 

    try:
        pedido = Pedido(
            cliente_nome=cliente_nome, 
            cliente_contato=None,
            status="criado",
            total=0,
            criado_por=usuario_responsavel
        )

        db.session.add(pedido)
        db.session.flush()

        total_geral = 0

        for item in itens:
            variante_id = item.get("variante_id")
            quantidade = item.get("quantidade")
            preco_unit = item.get("preco_unit")

            if not variante_id or not quantidade:
                db.session.rollback()
                return jsonify({"error": "Dados do item incompletos"}), 400

            quantidade = int(quantidade)
            preco_unit = float(preco_unit)

            estoque_registro = Estoque.query.filter_by(variante_id=variante_id).first()
            
            if not estoque_registro:
                db.session.rollback()
                return jsonify({"error": f"Estoque não encontrado para o item {variante_id}"}), 400

            if estoque_registro.quantidade < quantidade:
                db.session.rollback()
                return jsonify({"error": f"Estoque insuficiente. Disponível: {estoque_registro.quantidade}"}), 400

            estoque_registro.quantidade -= quantidade
            db.session.add(estoque_registro)

            item_pedido = ItemPedido(
                pedido_id=pedido.id,
                variante_id=variante_id,
                quantidade=quantidade,
                preco_unit=preco_unit,
                valor_total=preco_unit * quantidade
            )
            db.session.add(item_pedido)

            total_geral += preco_unit * quantidade

        pedido.total = total_geral
        db.session.commit()

        return jsonify({
            "status": "ok",
            "pedido_id": pedido.id,
            "total": total_geral
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/pedido/listar', methods=['GET'])
def listar_pedidos():
    """ Lista pedidos com itens e informações das variantes. """
    pedidos = Pedido.query.order_by(Pedido.created_at.desc()).limit(100).all()
    resultado = []

    for p in pedidos:
        itens_processados = []
        for item in p.itens:
            var = Variante.query.get(item.variante_id)
            itens_processados.append({
                "variante_id": item.variante_id,
                "sku": var.sku if var else None,
                "quantidade": int(item.quantidade),
                "preco_unit": float(item.preco_unit),
                "valor_total": float(item.valor_total)
            })

        resultado.append({
            "id": p.id,
            "cliente_nome": p.cliente_nome,
            "total": float(p.total or 0),
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
            "itens": itens_processados
        })

    return jsonify(resultado)

@app.route("/variante/excluir/<int:id>", methods=["DELETE"])
def excluir_variante(id):
    try:
        variante = Variante.query.get(id)
        if not variante:
            return jsonify({"status": "erro", "mensagem": "Variante não encontrada"}), 404
        
        if variante.estoque:
            variante.estoque.quantidade = 0
            
        variante.ativo = False
        
        db.session.commit()
        
        return jsonify({"status": "ok", "mensagem": "Produto removido com sucesso!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
        

@app.route("/api/atividades_recentes")
def api_atividades_recentes():
    atividades = []

    # Vendas
    ultimos_pedidos = Pedido.query.order_by(Pedido.created_at.desc()).limit(50).all()
    for p in ultimos_pedidos:
        qtd_total = sum([i.quantidade for i in p.itens])
        nome_exemplo = "Produtos diversos"
        if p.itens:
            primeiro_item = p.itens[0]
            var = db.session.get(Variante, primeiro_item.variante_id)
            if var and var.produto:
                nome_exemplo = f"{var.produto.linha}"
            else:
                nome_exemplo = "(Produto Excluído)"

        atividades.append({
            "id": p.id,
            "tipo": "venda",
            "icone": "💰",
            "titulo": "Venda Realizada",
            "descricao": f"{nome_exemplo} (e mais itens...)",
            "detalhe": f"{qtd_total} un. vendidas",
            "data": p.created_at.isoformat()
        })

    # Produtos (Apenas ativos)
    ultimos_produtos = Variante.query.filter_by(ativo=True).order_by(Variante.created_at.desc()).limit(50).all()
    for v in ultimos_produtos:
        nome_prod = "Produto"
        prod = db.session.get(Produto, v.produto_id)
        if prod:
            nome_prod = f"{prod.linha} {prod.formato}"
        
        qtd_inicial = 0
        if v.estoque:
            qtd_inicial = v.estoque.quantidade

        atividades.append({
            "id": v.id,
            "tipo": "cadastro",
            "icone": "✨",
            "titulo": "Novo Produto",
            "descricao": f"{nome_prod} - {v.cor}",
            "detalhe": f"Estoque inicial: {qtd_inicial}",
            "data": v.created_at.isoformat()
        })

    atividades.sort(key=lambda x: x['data'], reverse=True)
    return jsonify(atividades[:50])


@app.route("/pedido/excluir/<int:id>", methods=["DELETE"])
def excluir_pedido(id):
    try:
        pedido = Pedido.query.get(id)
        if not pedido:
            return jsonify({"status": "erro", "mensagem": "Pedido não encontrado"}), 404
        
        ItemPedido.query.filter_by(pedido_id=id).delete()
        
        db.session.delete(pedido)
        db.session.commit()
        
        return jsonify({"status": "ok", "mensagem": "Venda excluída do histórico!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/admin/limpar_todas_vendas")
def limpar_todas_vendas():
    try:
        num_itens = db.session.query(ItemPedido).delete()
        num_pedidos = db.session.query(Pedido).delete()
        db.session.commit()
        
        return jsonify({
            "status": "ok", 
            "mensagem": f"Limpeza concluída! {num_pedidos} pedidos e {num_itens} itens foram apagados."
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# -------------------
# Endpoints de Insumos
# -------------------
@app.route("/insumo/criar", methods=["POST"])
def criar_insumo():
    """
    Cria um ou mais insumos para uma variante.
    Payload: { "variante_id": 1, "insumos": [{"material": "...", "quantidade": 2.5, "custo_unitario": 50.00}] }
    """
    data = request.get_json()
    variante_id = data.get("variante_id")
    insumos_data = data.get("insumos", [])

    if not variante_id:
        return jsonify({"error": "variante_id required"}), 400
    
    variante = Variante.query.get(variante_id)
    if not variante:
        return jsonify({"error": "Variante não encontrada"}), 404
    
    # Validações
    if not insumos_data or len(insumos_data) == 0:
        return jsonify({"error": "Pelo menos um insumo deve ser fornecido"}), 400

    try:
        insumos_criados = []
        for insumo_data in insumos_data:
            material = insumo_data.get("material", "").strip()
            quantidade = insumo_data.get("quantidade")
            custo_unitario = insumo_data.get("custo_unitario", 0)
            
            # Validações de dados
            if not material:
                return jsonify({"error": "Material é obrigatório"}), 400
            
            if quantidade is None or float(quantidade) <= 0:
                return jsonify({"error": f"Quantidade deve ser maior que zero para '{material}'"}), 400
            
            if float(custo_unitario) < 0:
                return jsonify({"error": f"Custo unitário não pode ser negativo para '{material}'"}), 400
            
            # Verificar duplicação de material na mesma variante
            insumo_existente = Insumo.query.filter_by(
                variante_id=variante_id,
                material=material
            ).first()
            
            if insumo_existente:
                return jsonify({
                    "error": f"Insumo '{material}' já existe para esta variante. Atualize o existente ou use outro nome."
                }), 400
            
            insumo = Insumo(
                variante_id=variante_id,
                material=material,
                quantidade=quantidade,
                custo_unitario=custo_unitario,
                unidade_medida=insumo_data.get("unidade_medida", "un")
            )
            db.session.add(insumo)
            db.session.flush()
            
            insumos_criados.append({
                "id": insumo.id,
                "material": insumo.material,
                "quantidade": float(insumo.quantidade),
                "custo_unitario": float(insumo.custo_unitario),
                "custo_total": insumo.custo_total
            })
        
        db.session.commit()
        
        # Retornar também os custos atualizados da variante
        return jsonify({
            "status": "ok",
            "mensagem": f"{len(insumos_criados)} insumo(s) cadastrado(s) com sucesso",
            "insumos": insumos_criados,
            "custo_producao": float(variante.custo_producao),
            "preco_venda_sugerido": float(variante.preco_venda_sugerido)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/insumo/variante/<int:variante_id>", methods=["GET"])
def listar_insumos_variante(variante_id):
    """Lista todos os insumos de uma variante específica com custos calculados."""
    variante = Variante.query.get(variante_id)
    if not variante:
        return jsonify({"error": "Variante não encontrada"}), 404
    
    insumos = Insumo.query.filter_by(variante_id=variante_id).all()
    
    return jsonify({
        "variante_id": variante_id,
        "sku": variante.sku,
        "insumos": [{
            "id": i.id,
            "material": i.material,
            "quantidade": float(i.quantidade),
            "custo_unitario": float(i.custo_unitario),
            "unidade_medida": i.unidade_medida,
            "custo_total": i.custo_total
        } for i in insumos],
        "custo_producao": float(variante.custo_producao),
        "preco_venda_sugerido": float(variante.preco_venda_sugerido),
        "preco_base_atual": float(variante.preco_base)
    })


@app.route("/insumo/<int:id>", methods=["DELETE"])
def deletar_insumo(id):
    """Remove um insumo específico."""
    try:
        insumo = Insumo.query.get(id)
        if not insumo:
            return jsonify({"status": "erro", "mensagem": "Insumo não encontrado"}), 404
        
        variante_id = insumo.variante_id
        db.session.delete(insumo)
        db.session.commit()
        
        # Retornar custos atualizados
        variante = Variante.query.get(variante_id)
        return jsonify({
            "status": "ok",
            "mensagem": "Insumo removido com sucesso",
            "custo_producao": float(variante.custo_producao),
            "preco_venda_sugerido": float(variante.preco_venda_sugerido)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


# -------------------
# Endpoints de Clientes e Endereços
# -------------------
@app.route("/cliente/criar", methods=["POST"])
def criar_cliente():
    """Cria um novo cliente com endereço."""
    data = request.get_json()
    
    # Validações
    nome = data.get("nome", "").strip()
    email = data.get("email", "").strip()
    telefone = data.get("telefone", "").strip()
    endereco_data = data.get("endereco", {})
    
    if not nome or not email or not telefone:
        return jsonify({"error": "Nome, email e telefone são obrigatórios"}), 400
    
    # Verificar se email já existe
    if Cliente.query.filter_by(email=email.lower()).first():
        return jsonify({"error": "Email já cadastrado"}), 400
    
    # Validar endereço
    cep = endereco_data.get("cep", "").strip()
    rua = endereco_data.get("rua", "").strip()
    bairro = endereco_data.get("bairro", "").strip()
    cidade = endereco_data.get("cidade", "").strip()
    estado = endereco_data.get("estado", "").strip()
    numero = endereco_data.get("numero", "").strip()
    
    if not all([cep, rua, bairro, cidade, estado, numero]):
        return jsonify({"error": "Todos os campos de endereço são obrigatórios"}), 400
    
    try:
        # Criar endereço
        endereco = Endereco(
            cep=cep, rua=rua, bairro=bairro, cidade=cidade,
            estado=estado.upper(), numero=numero,
            complemento=endereco_data.get("complemento", "").strip() or None
        )
        db.session.add(endereco)
        db.session.flush()
        
        # Criar cliente
        cliente = Cliente(
            id_endereco=endereco.id_endereco, nome=nome,
            email=email.lower(), telefone=telefone,
            cpf_cnpj=data.get("cpf_cnpj", "").strip() or None
        )
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify({
            "status": "ok",
            "mensagem": "Cliente cadastrado com sucesso",
            "cliente_id": cliente.id_clientes
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/clientes/listar", methods=["GET"])
def listar_todos_clientes():
    """Lista todos os clientes com endereços."""
    try:
        clientes = Cliente.query.all()
        return jsonify([{
            "id": c.id_clientes,
            "nome": c.nome,
            "email": c.email,
            "telefone": c.telefone,
            "cpf_cnpj": c.cpf_cnpj,
            "endereco": {
                "cep": c.endereco.cep,
                "rua": c.endereco.rua,
                "numero": c.endereco.numero,
                "bairro": c.endereco.bairro,
                "cidade": c.endereco.cidade,
                "estado": c.endereco.estado
            }
        } for c in clientes])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cliente/<int:id>", methods=["DELETE"])
def deletar_cliente_endpoint(id):
    """Deleta um cliente."""
    try:
        cliente = Cliente.query.get(id)
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({"status": "ok", "mensagem": "Cliente deletado"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# -------------------
# Endpoints de Relatórios
# -------------------
@app.route("/relatorio/custos", methods=["GET"])
def relatorio_custos():
    """
    Gera relatório completo de custos de todos os produtos ativos.
    Retorna análise detalhada de insumos, custos e margens.
    """
    try:
        produtos = Produto.query.filter_by(ativo=True).all()
        relatorio = []
        
        for produto in produtos:
            variantes_info = []
            
            for variante in produto.variantes:
                if not variante.ativo:
                    continue
                
                # Informações dos insumos
                insumos_detalhes = []
                custo_total_insumos = 0
                
                for insumo in variante.insumos:
                    custo_insumo = insumo.custo_total
                    custo_total_insumos += custo_insumo
                    
                    insumos_detalhes.append({
                        "material": insumo.material,
                        "quantidade": float(insumo.quantidade),
                        "unidade": insumo.unidade_medida,
                        "custo_unitario": float(insumo.custo_unitario),
                        "custo_total": float(custo_insumo)
                    })
                
                # Cálculos
                custo_producao = variante.custo_producao
                preco_sugerido = variante.preco_venda_sugerido
                preco_atual = float(variante.preco_base)
                
                # Margens
                margem_interna = custo_producao - custo_total_insumos
                margem_venda = preco_atual - custo_producao if preco_atual > 0 else 0
                percentual_margem = (margem_venda / preco_atual * 100) if preco_atual > 0 else 0
                
                # Estoque
                estoque_info = variante.estoque
                qtd_estoque = estoque_info.quantidade if estoque_info else 0
                valor_estoque = qtd_estoque * preco_atual
                
                variantes_info.append({
                    "variante_id": variante.id,
                    "sku": variante.sku,
                    "dimensoes": f"{variante.altura_cm}x{variante.largura_cm} cm" if variante.altura_cm and variante.largura_cm else "N/A",
                    "cor": variante.cor,
                    "moldura": variante.moldura,
                    "insumos": insumos_detalhes,
                    "analise_custos": {
                        "custo_insumos": float(custo_total_insumos),
                        "margem_interna_10pct": float(margem_interna),
                        "custo_producao_total": float(custo_producao),
                        "preco_sugerido_125pct": float(preco_sugerido),
                        "preco_venda_atual": float(preco_atual),
                        "margem_lucro": float(margem_venda),
                        "percentual_margem": round(percentual_margem, 2)
                    },
                    "estoque": {
                        "quantidade": int(qtd_estoque),
                        "valor_total": float(valor_estoque)
                    }
                })
            
            if variantes_info:
                relatorio.append({
                    "produto_id": produto.id,
                    "linha": produto.linha,
                    "formato": produto.formato,
                    "descricao": produto.descricao,
                    "total_variantes": len(variantes_info),
                    "variantes": variantes_info
                })
        
        return jsonify({
            "status": "ok",
            "total_produtos": len(relatorio),
            "data_geracao": datetime.utcnow().isoformat(),
            "relatorio": relatorio
        })
    
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/relatorio/custos/produto/<int:produto_id>", methods=["GET"])
def relatorio_custos_produto(produto_id):
    """Relatório de custos de um produto específico."""
    try:
        produto = Produto.query.get(produto_id)
        if not produto:
            return jsonify({"error": "Produto não encontrado"}), 404
        
        variantes_info = []
        for variante in produto.variantes:
            if not variante.ativo:
                continue
            
            insumos_detalhes = [{
                "material": i.material,
                "quantidade": float(i.quantidade),
                "unidade": i.unidade_medida,
                "custo_unitario": float(i.custo_unitario),
                "custo_total": float(i.custo_total)
            } for i in variante.insumos]
            
            variantes_info.append({
                "variante_id": variante.id,
                "sku": variante.sku,
                "insumos": insumos_detalhes,
                "custo_producao": float(variante.custo_producao),
                "preco_sugerido": float(variante.preco_venda_sugerido),
                "preco_atual": float(variante.preco_base)
            })
        
        return jsonify({
            "produto_id": produto.id,
            "linha": produto.linha,
            "formato": produto.formato,
            "variantes": variantes_info
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------
# Run
# -------------------
if __name__ == "__main__":
    app.run(debug=True)