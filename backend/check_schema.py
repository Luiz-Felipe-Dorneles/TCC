from flask import Flask
from database import init_app, db
from sqlalchemy import text, inspect

app = Flask(__name__)
init_app(app)

with app.app_context():
    try:
        inspector = inspect(db.engine)
        
        print("--- Table: clientes ---")
        columns = [c['name'] for c in inspector.get_columns('clientes')]
        print(columns)
        
        print("\n--- Table: endereco ---")
        columns = [c['name'] for c in inspector.get_columns('endereco')]
        print(columns)
        
    except Exception as e:
        print(e)
