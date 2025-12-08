from flask import Flask
from database import db, init_app
from sqlalchemy import text

# Inicializa Flask
app = Flask(__name__)
init_app(app)  # Conecta ao MySQL via SQLAlchemy

# Rota de teste de conexão
@app.route("/teste_db")
def teste_db():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ Conectado ao banco!"
    except Exception as e:
        return f"❌ Erro: {e}"

# Roda o servidor
if __name__ == "__main__":
    app.run(debug=True)
