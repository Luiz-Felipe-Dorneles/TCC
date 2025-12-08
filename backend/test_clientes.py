from flask import Flask
from database import init_app, db
from models import Cliente, Endereco
from app import app

with app.app_context():
    try:
        print("Consultando clientes...")
        clientes = Cliente.query.all()
        print(f"Total de clientes encontrados: {len(clientes)}")
        
        for c in clientes:
            print(f"ID: {c.id_clientes}, Nome: {c.nome}")
            if c.endereco:
                print(f"  Endereco: {c.endereco.rua}, {c.endereco.numero} - {c.endereco.cidade}/{c.endereco.estado}")
            else:
                print("  Endereco: NONE (Isso pode causar erro na API)")
                
    except Exception as e:
        print(f"Erro ao consultar: {e}")
