import os

import pytest
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://bah_user:bah_password@db:5432/bah_db"
)


@pytest.fixture() 
def conn():
    engine = sa.create_engine(DATABASE_URL, future=True)
    with engine.begin() as c:
        yield c


def test_seed_admin_existe(conn):
    row = conn.execute(
        sa.text("SELECT email, name FROM users WHERE email='admin@bah.local'")
    ).first()
    assert row is not None
    assert row.email == "admin@bah.local"


def test_email_unique_case_insensitive(conn):
    conn.execute(
        sa.text("DELETE FROM users WHERE lower(email) IN ('xxx.com','exxx.com')")
    )
    conn.execute(
        sa.text("INSERT INTO users (email, password_hash) VALUES ('xxx.com','h')")
    )
    with pytest.raises(IntegrityError):
        conn.execute(
            sa.text("INSERT INTO users (email, password_hash) VALUES ('XXX.com','h')")
        )


def test_not_null_password_hash(conn):
    with pytest.raises(IntegrityError):
        conn.execute(
            sa.text("INSERT INTO users (email) VALUES ('no-pass@example.com')")
        )
