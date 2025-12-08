from flask import Flask
from database import init_app, db
from sqlalchemy import text

app = Flask(__name__)
init_app(app)

with app.app_context():
    try:
        print("Atualizando tabela clientes...")
        # Adicionar colunas faltantes em clientes
        try:
            db.session.execute(text("ALTER TABLE clientes ADD COLUMN telefone VARCHAR(15) NOT NULL DEFAULT ''"))
            print("  - Adicionado telefone")
        except Exception as e: print(f"  - Erro telefone: {e}")

        try:
            db.session.execute(text("ALTER TABLE clientes ADD COLUMN cpf_cnpj VARCHAR(18)"))
            print("  - Adicionado cpf_cnpj")
        except Exception as e: print(f"  - Erro cpf_cnpj: {e}")

        try:
            db.session.execute(text("ALTER TABLE clientes ADD COLUMN created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP"))
            print("  - Adicionado created_at")
        except Exception as e: print(f"  - Erro created_at: {e}")

        try:
            db.session.execute(text("ALTER TABLE clientes ADD COLUMN updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
            print("  - Adicionado updated_at")
        except Exception as e: print(f"  - Erro updated_at: {e}")

        # Remover coluna antiga se existir (opcional, mas bom para limpeza)
        try:
            db.session.execute(text("ALTER TABLE clientes DROP COLUMN numero"))
            print("  - Removido numero (antigo)")
        except Exception as e: print(f"  - Erro drop numero: {e}")
        
        # Ajustar AUTO_INCREMENT se não estiver
        try:
            db.session.execute(text("ALTER TABLE clientes MODIFY id_clientes INT NOT NULL AUTO_INCREMENT"))
            print("  - Ajustado AUTO_INCREMENT clientes")
        except Exception as e: print(f"  - Erro auto_increment clientes: {e}")


        print("\nAtualizando tabela endereco...")
        # Adicionar colunas faltantes em endereco
        try:
            db.session.execute(text("ALTER TABLE endereco ADD COLUMN cidade VARCHAR(100) NOT NULL DEFAULT ''"))
            print("  - Adicionado cidade")
        except Exception as e: print(f"  - Erro cidade: {e}")

        try:
            db.session.execute(text("ALTER TABLE endereco ADD COLUMN estado VARCHAR(2) NOT NULL DEFAULT ''"))
            print("  - Adicionado estado")
        except Exception as e: print(f"  - Erro estado: {e}")
        
        try:
            db.session.execute(text("ALTER TABLE endereco ADD COLUMN complemento VARCHAR(100)"))
            print("  - Adicionado complemento")
        except Exception as e: print(f"  - Erro complemento: {e}")

        try:
            db.session.execute(text("ALTER TABLE endereco MODIFY cep VARCHAR(9) NOT NULL"))
            print("  - Ajustado tipo CEP")
        except Exception as e: print(f"  - Erro modify cep: {e}")
        
        try:
            db.session.execute(text("ALTER TABLE endereco MODIFY numero VARCHAR(10) NOT NULL"))
            print("  - Ajustado tipo Numero")
        except Exception as e: print(f"  - Erro modify numero: {e}")

        try:
            db.session.execute(text("ALTER TABLE endereco MODIFY id_endereco INT NOT NULL AUTO_INCREMENT"))
            print("  - Ajustado AUTO_INCREMENT endereco")
        except Exception as e: print(f"  - Erro auto_increment endereco: {e}")

        db.session.commit()
        print("\n✅ Atualização de esquema concluída!")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Erro geral: {e}")
