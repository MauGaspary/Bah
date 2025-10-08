#!/usr/bin/env python3
import os
import sys
from datetime import date, datetime, time, timezone

from sqlalchemy import text

from app.models.tag_model import Tag

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


from app.config.database import SessionLocal
from app.models.demo_model import Demo
from app.models.iniciativa_horario_model import HorarioTipo, IniciativaHorario
from app.models.iniciativa_model import Iniciativa
from app.models.iniciativa_tag_model import IniciativaTag
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


def seed_tags():
    db = SessionLocal()

    try:
        existing_count = db.query(Tag).count()
        if existing_count > 0:
            print(f"Tags já existem. Encontrados {existing_count} tags.")
            return

        tags_data = [
            {"nome": "Meio Ambiente"},
            {"nome": "Educação"},
            {"nome": "Saúde"},
            {"nome": "Tecnologia"},
            {"nome": "Cultura"},
            {"nome": "Esporte"},
            {"nome": "Inclusão Social"},
            {"nome": "Desenvolvimento Sustentável"},
        ]

        for tag_data in tags_data:
            tag = Tag(**tag_data)
            db.add(tag)

        db.commit()
        print(f"Seed de tags executado com sucesso. Criados {len(tags_data)} tags.")

    except Exception as e:
        db.rollback()
        print(f"Erro ao executar seed de tags: {e}")
        sys.exit(1)
    finally:
        db.close()


def seed_iniciativas():
    db = SessionLocal()

    try:
        existing_count = db.query(Iniciativa).count()
        if existing_count > 0:
            print(f"Iniciativas já existem. Encontrados {existing_count} iniciativas.")
            return

        # Buscar os primeiros usuários e organizadores para usar como referência
        primeiro_usuario = db.query(Usuario).first()
        if not primeiro_usuario:
            print("Erro: Nenhum usuário encontrado. Execute seed_users() primeiro.")
            return

        organizadores = db.query(Organizador).all()
        if not organizadores:
            print(
                "Erro: Nenhum organizador encontrado. Execute seed_organizadores() primeiro."
            )
            return

        tags = db.query(Tag).all()
        if not tags:
            print("Erro: Nenhuma tag encontrada. Execute seed_tags() primeiro.")
            return

        iniciativas_data = [
            {
                "titulo": "Workshop de Desenvolvimento Sustentável",
                "descricao": "Workshop prático sobre técnicas de desenvolvimento sustentável e impacto ambiental. Aprenda como implementar práticas eco-friendly em seus projetos.",
                "link": "https://exemplo.com/workshop-sustentavel",
                "destaque": True,
                "local": "Centro de Convenções - Caxias do Sul",
                "imagem_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800",
                "organizador_id": organizadores[0].id,
                "horarios": [
                    {
                        "data_evento": date(2025, 11, 15),
                        "hora_inicio": time(9, 0),
                        "hora_fim": time(17, 0),
                        "tipo": HorarioTipo.PRESENCIAL,
                    }
                ],
                "tag_ids": [
                    tag.id
                    for tag in tags
                    if tag.nome in ["Meio Ambiente", "Desenvolvimento Sustentável"]
                ],
            },
            {
                "titulo": "Curso de Programação para Iniciantes",
                "descricao": "Curso completo de introdução à programação, cobrindo conceitos fundamentais e linguagens modernas. Ideal para quem está começando na área tech.",
                "link": "https://exemplo.com/curso-programacao",
                "destaque": False,
                "local": "SENAC - Sala 201",
                "imagem_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800",
                "organizador_id": (
                    organizadores[1].id
                    if len(organizadores) > 1
                    else organizadores[0].id
                ),
                "horarios": [
                    {
                        "data_evento": date(2025, 11, 20),
                        "hora_inicio": time(19, 0),
                        "hora_fim": time(22, 0),
                        "tipo": HorarioTipo.PRESENCIAL,
                    },
                    {
                        "data_evento": date(2025, 11, 22),
                        "hora_inicio": time(19, 0),
                        "hora_fim": time(22, 0),
                        "tipo": HorarioTipo.PRESENCIAL,
                    },
                ],
                "tag_ids": [
                    tag.id for tag in tags if tag.nome in ["Tecnologia", "Educação"]
                ],
            },
            {
                "titulo": "Feira de Saúde Comunitária",
                "descricao": "Evento gratuito com consultas médicas, exames preventivos e palestras educativas sobre saúde e bem-estar para toda a comunidade.",
                "link": "https://exemplo.com/feira-saude",
                "destaque": True,
                "local": "Praça Dante Alighieri",
                "imagem_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800",
                "organizador_id": organizadores[0].id,
                "horarios": [
                    {
                        "data_evento": date(2025, 12, 5),
                        "hora_inicio": time(8, 0),
                        "hora_fim": time(16, 0),
                        "tipo": HorarioTipo.PRESENCIAL,
                    }
                ],
                "tag_ids": [
                    tag.id for tag in tags if tag.nome in ["Saúde", "Inclusão Social"]
                ],
            },
            {
                "titulo": "Festival Cultural de Inverno",
                "descricao": "Apresentações artísticas, exposições e shows musicais celebrando a diversidade cultural da região. Evento híbrido com transmissão online.",
                "link": "https://exemplo.com/festival-cultural",
                "destaque": False,
                "local": "Teatro Municipal",
                "imagem_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800",
                "organizador_id": (
                    organizadores[2].id
                    if len(organizadores) > 2
                    else organizadores[0].id
                ),
                "horarios": [
                    {
                        "data_evento": date(2025, 12, 15),
                        "hora_inicio": time(18, 0),
                        "hora_fim": time(22, 0),
                        "tipo": HorarioTipo.HIBRIDO,
                    },
                    {
                        "data_evento": date(2025, 12, 16),
                        "hora_inicio": time(14, 0),
                        "hora_fim": time(18, 0),
                        "tipo": HorarioTipo.HIBRIDO,
                    },
                ],
                "tag_ids": [
                    tag.id for tag in tags if tag.nome in ["Cultura", "Inclusão Social"]
                ],
            },
            {
                "titulo": "Webinar: Empreendedorismo Digital",
                "descricao": "Palestra online sobre as principais estratégias para empreender no mundo digital, com cases de sucesso e dicas práticas.",
                "link": "https://exemplo.com/webinar-empreendedorismo",
                "destaque": False,
                "local": None,
                "imagem_url": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800",
                "organizador_id": (
                    organizadores[3].id
                    if len(organizadores) > 3
                    else organizadores[0].id
                ),
                "horarios": [
                    {
                        "data_evento": date(2025, 11, 30),
                        "hora_inicio": time(14, 0),
                        "hora_fim": time(16, 0),
                        "tipo": HorarioTipo.ONLINE,
                    }
                ],
                "tag_ids": [tag.id for tag in tags if tag.nome in ["Tecnologia"]],
            },
            {
                "titulo": "Torneio de Futebol Solidário",
                "descricao": "Campeonato de futebol beneficente com arrecadação de alimentos não perecíveis. Toda a comunidade está convidada a participar.",
                "link": "https://exemplo.com/torneio-futebol",
                "destaque": True,
                "local": "Campo do Juventude",
                "imagem_url": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800",
                "organizador_id": (
                    organizadores[4].id
                    if len(organizadores) > 4
                    else organizadores[0].id
                ),
                "horarios": [
                    {
                        "data_evento": date(2025, 12, 10),
                        "hora_inicio": time(8, 0),
                        "hora_fim": time(18, 0),
                        "tipo": HorarioTipo.PRESENCIAL,
                    }
                ],
                "tag_ids": [
                    tag.id for tag in tags if tag.nome in ["Esporte", "Inclusão Social"]
                ],
            },
        ]

        for iniciativa_data in iniciativas_data:
            # Criar vetor de descrição (simulado com zeros por agora)
            descricao_vetor = [0.0] * 768  # Assumindo 768 dimensões

            # Criar a iniciativa
            iniciativa = Iniciativa(
                titulo=iniciativa_data["titulo"],
                descricao=iniciativa_data["descricao"],
                descricao_vetor=descricao_vetor,
                organizador_id=iniciativa_data["organizador_id"],
                link=iniciativa_data["link"],
                destaque=iniciativa_data["destaque"],
                local=iniciativa_data["local"],
                imagem_url=iniciativa_data["imagem_url"],
                criado_por=primeiro_usuario.id,
                criado_em=datetime.now(timezone.utc),
            )

            db.add(iniciativa)
            db.flush()  # Para obter o ID da iniciativa

            # Criar os horários
            for horario_data in iniciativa_data["horarios"]:
                horario = IniciativaHorario(
                    iniciativa_id=iniciativa.id,
                    data_evento=horario_data["data_evento"],
                    hora_inicio=horario_data["hora_inicio"],
                    hora_fim=horario_data["hora_fim"],
                    tipo=horario_data["tipo"],
                    criado_em=datetime.now(timezone.utc),
                )
                db.add(horario)

            # Associar tags
            if iniciativa_data.get("tag_ids"):
                for tag_id in iniciativa_data["tag_ids"]:
                    iniciativa_tag = IniciativaTag(
                        iniciativa_id=iniciativa.id, tag_id=tag_id
                    )
                    db.add(iniciativa_tag)

        db.commit()
        print(
            f"Seed de iniciativas executado com sucesso. Criadas {len(iniciativas_data)} iniciativas."
        )

    except Exception as e:
        db.rollback()
        print(f"Erro ao executar seed de iniciativas: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("Executando seed do banco de dados...")
    seed_users()
    seed_organizadores()
    seed_tags()
    seed_iniciativas()
    seed_demos()
    print("Seed finalizado")
