from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_app, db
from models import Usuario
import os

# Caminhos HTML/CSS
template_path = os.path.join(os.path.dirname(__file__), "../frontend")
static_path = template_path

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
init_app(app)

# Cria tabelas se não existirem
with app.app_context():
    db.create_all()

# Rotas de páginas
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register_page")
def register_page():
    return render_template("criar_conta.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# API: criar conta
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify(status="erro", mensagem="Preencha todos os campos"), 400

    if Usuario.query.filter_by(email=email.lower()).first():
        return jsonify(status="erro", mensagem="E-mail já cadastrado"), 400

    user = Usuario(
        email=email.lower(),
        senha_hash=generate_password_hash(senha)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(status="ok", mensagem="Conta criada com sucesso!")

# API: login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify(status="erro", mensagem="Preencha todos os campos"), 400

    user = Usuario.query.filter_by(email=email.lower()).first()
    if not user:
        return jsonify(status="erro", mensagem="Conta não encontrada"), 401

    if not check_password_hash(user.senha_hash, senha):
        return jsonify(status="erro", mensagem="Senha incorreta"), 401

    return jsonify(status="ok", mensagem="Login realizado com sucesso")


@app.route("/teste_db")
def teste_db():
    try:
        db.session.execute("SELECT 1")
        return "✅ Conectado ao banco!"
    except Exception as e:
        return f"❌ Erro: {e}"
    


if __name__ == "__main__":
    app.run(debug=True)









