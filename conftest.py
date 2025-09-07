import os

os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"
os.environ["TESTCONTAINERS_HOST_OVERRIDE"] = "host.docker.internal"

import pytest
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        url = postgres.get_connection_url().replace("localhost", "host.docker.internal")
        postgres.get_connection_url = lambda: url
        yield postgres
