from flask import Flask
from database import init_app, db
from models import Cliente, Endereco

app = Flask(__name__)
init_app(app)

with app.app_context():
    try:
        # Testar conexão
        print("🔍 Testando conexão com o banco de dados...")
        db.session.execute(db.text("SELECT 1"))
        print("✅ Conexão estabelecida com sucesso!\n")
        
        # Testar query na tabela clientes
        print("🔍 Testando query na tabela 'clientes'...")
        clientes = Cliente.query.all()
        print(f"✅ Query executada! Total de clientes: {len(clientes)}\n")
        
        # Testar query com filtro (o que estava causando erro)
        print("🔍 Testando query com filtro por email...")
        cliente_teste = Cliente.query.filter_by(email='matheus@gmail').first()
        
        if cliente_teste:
            print(f"✅ Cliente encontrado: {cliente_teste.nome}")
        else:
            print("ℹ️  Nenhum cliente encontrado com esse email (isso é normal se não houver dados)")
        
        print("\n✅ TODOS OS TESTES PASSARAM! O erro foi resolvido.")
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        print(f"\nTipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
