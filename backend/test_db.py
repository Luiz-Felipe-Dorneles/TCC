# Script de teste de conexão com banco de dados
from flask import Flask
from database import init_app, db
from models import Cliente, Endereco, Insumo, Produto, Variante
from sqlalchemy import text

app = Flask(__name__)
init_app(app)

with app.app_context():
    try:
        # Testar conexão
        db.session.execute(text("SELECT 1"))
        print("✅ Conexão com banco de dados OK")
        
        # Verificar tabelas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Tabelas encontradas ({len(tables)}):")
        for table in sorted(tables):
            print(f"  - {table}")
        
        # Verificar se tabelas necessárias existem
        required_tables = ['clientes', 'endereco', 'insumos', 'produto', 'variante']
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            print(f"\n⚠️  Tabelas faltando: {', '.join(missing)}")
            print("Execute: mysql -u root -p sistema_tcc < tcc.sql")
        else:
            print("\n✅ Todas as tabelas necessárias existem")
        
        # Testar modelos
        print("\n🔍 Testando modelos:")
        print(f"  - Cliente: {Cliente.__tablename__}")
        print(f"  - Endereco: {Endereco.__tablename__}")
        print(f"  - Insumo: {Insumo.__tablename__}")
        print(f"  - Produto: {Produto.__tablename__}")
        print(f"  - Variante: {Variante.__tablename__}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        print("\nVerifique:")
        print("1. MySQL está rodando?")
        print("2. Banco 'sistema_tcc' existe?")
        print("3. Usuário 'root' com senha 'admin'?")
