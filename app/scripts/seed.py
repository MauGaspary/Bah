#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.config.database import SessionLocal
from app.models.admin_model_example import Admin


def seed_admins():
    db = SessionLocal()

    try:
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


if __name__ == "__main__":
    print("Executando seed do banco de dados...")
    seed_admins()
    print("Seed finalizado")
