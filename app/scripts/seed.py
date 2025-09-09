#!/usr/bin/env python3
import os
import sys

from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


from app.config.database import SessionLocal
from app.models.demo_model import Demo
from app.models.organizador_model import Organizador
from app.models.usuario_model import Usuario
from app.utils.password_hasher import PasswordHasher


def seed_demos():
    db = SessionLocal()

    try:
        result = db.execute(
            text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'demos')"
            )
        )
        table_exists = result.scalar()

        if not table_exists:
            print("Tabela 'demos' não existe. Execute as migrations primeiro.")
            return

        existing_count = db.query(Demo).count()
        if existing_count > 0:
            print(f"Seed já executado. Encontrados {existing_count} demos.")
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

        for demo_data in admins_data:
            demo = Demo(**demo_data)
            db.add(demo)

        db.commit()
        print(f"Seed executado com sucesso. Criados {len(admins_data)} demos.")

    except Exception as e:
        db.rollback()
        print(f"Erro ao executar seed: {e}")
        sys.exit(1)
    finally:
        db.close()


def seed_users():
    db = SessionLocal()
    hasher = PasswordHasher()

    try:
        existing_count = db.query(Usuario).count()
        if existing_count > 0:
            print(f"Usuários já existem. Encontrados {existing_count} usuários.")
            return

        users_data = [
            {
                "email": "admin@bah.com.br",
                "password": "admin123",
                "nome": "Administrador",
                "sobrenome": "Sistema",
            },
            {
                "email": "joao.silva@bah.com.br",
                "password": "senha123",
                "nome": "João",
                "sobrenome": "Silva",
            },
            {
                "email": "maria.santos@bah.com.br",
                "password": "senha123",
                "nome": "Maria",
                "sobrenome": "Santos",
            },
        ]

        for user_data in users_data:
            password_hash = hasher.hash(user_data["password"])
            usuario = Usuario(
                email=user_data["email"],
                senha_hash=password_hash,
                nome=user_data["nome"],
                sobrenome=user_data["sobrenome"],
            )
            db.add(usuario)

        db.commit()
        print(
            f"Seed de usuários executado com sucesso. Criados {len(users_data)} usuários."
        )
        print("\nCredenciais de login:")
        for user_data in users_data:
            print(f"Email: {user_data['email']} | Senha: {user_data['password']}")

    except Exception as e:
        db.rollback()
        print(f"Erro ao executar seed de usuários: {e}")
        sys.exit(1)
    finally:
        db.close()


def seed_organizadores():
    db = SessionLocal()

    try:
        existing_count = db.query(Organizador).count()
        if existing_count > 0:
            print(
                f"Organizadores já existem. Encontrados {existing_count} organizadores."
            )
            return

        organizadores_data = [
            {"nome": "Prefeitura de Caxias do Sul"},
            {"nome": "SENAC"},
            {"nome": "UCS - Universidade de Caxias do Sul"},
            {"nome": "SEBRAE"},
            {"nome": "Associação Comercial"},
        ]

        for org_data in organizadores_data:
            organizador = Organizador(**org_data)
            db.add(organizador)

        db.commit()
        print(
            f"Seed de organizadores executado com sucesso. Criados {len(organizadores_data)} organizadores."
        )

    except Exception as e:
        db.rollback()
        print(f"Erro ao executar seed de organizadores: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("Executando seed do banco de dados...")
    seed_users()
    seed_organizadores()
    seed_demos()
    print("Seed finalizado")
