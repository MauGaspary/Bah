#!/usr/bin/env python3
import os
import sys

from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import uuid

from app.config.database import SessionLocal
from app.models.admin_model_example import Admin
from app.models.usuario_model import Usuario


def seed_admins():
    db = SessionLocal()

    try:
        result = db.execute(
            text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'admins')"
            )
        )
        table_exists = result.scalar()

        if not table_exists:
            print("Tabela 'admins' não existe. Execute as migrations primeiro.")
            return

        existing_count = db.query(Admin).count()
        if existing_count > 0:
            print(f"Seed já executado. Encontrados {existing_count} admins.")
            return

        admins_data = [
            {
                "username": "pedro",
                "email": "pedro@bah.com.br",
            },
            {
                "username": "joao.silva",
                "email": "joao.silva@bah.com.br",
            },
            {
                "username": "maria.santos",
                "email": "maria.santos@bah.com.br",
            },
        ]

        for admin_data in admins_data:
            admin = Admin(**admin_data)
            db.add(admin)

        db.commit()
        print(f"Seed executado com sucesso. Criados {len(admins_data)} admins.")

    except Exception as e:
        db.rollback()
        print(f"Erro ao executar seed: {e}")
        sys.exit(1)
    finally:
        db.close()


def seed_usuarios():
    db = SessionLocal()

    try:
        existing_count = db.query(Usuario).count()
        if existing_count > 0:
            print(f"Usuários já existem. Encontrados {existing_count} usuários.")
            return

        usuario_sistema = Usuario(
            id="sistema",
            nome="Sistema",
            sobrenome="Admin",
            email="sistema@bah.com.br",
            senha_hash="hash_sistema",
        )

        usuarios_data = [
            {
                "id": str(uuid.uuid4()),
                "nome": "João",
                "sobrenome": "Silva",
                "email": "joao.silva@example.com",
                "senha_hash": "hash_joao",
            },
            {
                "id": str(uuid.uuid4()),
                "nome": "Maria",
                "sobrenome": "Santos",
                "email": "maria.santos@example.com",
                "senha_hash": "hash_maria",
            },
        ]

        db.add(usuario_sistema)

        for usuario_data in usuarios_data:
            usuario = Usuario(**usuario_data)
            db.add(usuario)

        db.commit()
        print(
            f"Seed de usuários executado com sucesso. Criados {len(usuarios_data) + 1} usuários."
        )

    except Exception as e:
        db.rollback()
        print(f"Erro ao executar seed de usuários: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("Executando seed do banco de dados...")
    seed_usuarios()
    seed_admins()
    print("Seed finalizado")
