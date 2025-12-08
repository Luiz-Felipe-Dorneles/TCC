import pymysql
from database import init_app, db
from models import Usuario, Cliente, Endereco, Produto, Variante, Estoque, Pedido, ItemPedido, Insumo
from flask import Flask

# Conectar ao MySQL sem especificar banco
try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='admin'
    )
    
    cursor = connection.cursor()
    
    # Criar novo banco de dados
    print("Criando banco de dados 'sistema_tcc2'...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS sistema_tcc2")
    print("✅ Banco 'sistema_tcc2' criado/verificado com sucesso!")
    
    # Verificar se o banco antigo existe
    cursor.execute("SHOW DATABASES LIKE 'sistema_tcc(2)'")
    old_db_exists = cursor.fetchone()
    
    if old_db_exists:
        print("\n⚠️  Banco antigo 'sistema_tcc(2)' encontrado!")
        print("Você pode copiar os dados manualmente ou usar o MySQL Workbench.")
        print("\nComando SQL para copiar dados (execute no MySQL):")
        print("USE sistema_tcc2;")
        print("-- Copie as tabelas do banco antigo conforme necessário")
    
    cursor.close()
    connection.close()
    
    # Criar tabelas no novo banco
    print("\nCriando tabelas no banco 'sistema_tcc2'...")
    app = Flask(__name__)
    init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Todas as tabelas foram criadas com sucesso!")
        
        # Verificar tabelas criadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\nTabelas criadas: {', '.join(tables)}")
    
    print("\n✅ Migração concluída! Reinicie o servidor Flask.")
    
except pymysql.Error as e:
    print(f"❌ Erro ao conectar ao MySQL: {e}")
    print("\nVerifique se:")
    print("1. O MySQL está rodando")
    print("2. As credenciais (root/admin) estão corretas")
    print("3. O usuário 'root' tem permissões para criar bancos de dados")
except Exception as e:
    print(f"❌ Erro: {e}")
