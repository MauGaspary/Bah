#!/usr/bin/env python3
"""Script para setup do banco de teste"""

import sys

from alembic import command
from alembic.config import Config


def setup_test_database(database_url: str):
    """Executa migrations no banco de teste"""
    import os

    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    original_cwd = os.getcwd()
    os.chdir(project_root)

    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        raise
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_test_db.py <database_url>")
        sys.exit(1)

    setup_test_database(sys.argv[1])
