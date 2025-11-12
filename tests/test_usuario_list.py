import uuid

import pytest

from tests.helpers import request_auth


@pytest.mark.integration
class TestUsuarioListIntegration:
    def test_list_users_returns_items_and_total(self, client, auth_token):
        # Get initial total
        resp_initial = request_auth(client, "GET", "/admin/usuarios/", token=auth_token)
        assert resp_initial.status_code == 200
        initial = resp_initial.json()
        initial_total = initial.get("total", 0)

        # Create 3 new users
        created = []
        for i in range(3):
            user_data = {
                "nome": f"ListUser{i}",
                "sobrenome": "Teste",
                "email": f"listuser_{uuid.uuid4().hex[:8]}@example.com",
                "password": "senha123",
            }
            resp = request_auth(
                client, "POST", "/admin/usuarios/", token=auth_token, json=user_data
            )
            assert resp.status_code == 201
            created.append(resp.json())

        # List again and assert total increased
        resp_after = request_auth(client, "GET", "/admin/usuarios/", token=auth_token)
        assert resp_after.status_code == 200
        data = resp_after.json()
        assert "items" in data and "total" in data
        assert data["total"] == initial_total + len(created)

    def test_pagination_returns_correct_page(self, client, auth_token):
        # Create 12 users so we have at least 13 including fixture user
        for i in range(12):
            user_data = {
                "nome": f"PageUser{i}",
                "sobrenome": "Teste",
                "email": f"pageuser_{uuid.uuid4().hex[:8]}@example.com",
                "password": "senha123",
            }
            resp = request_auth(
                client, "POST", "/admin/usuarios/", token=auth_token, json=user_data
            )
            assert resp.status_code == 201

        # page=2 size=10 -> expect remaining items
        resp_page2 = request_auth(
            client, "GET", "/admin/usuarios/?page=2&size=10", token=auth_token
        )
        assert resp_page2.status_code == 200
        data = resp_page2.json()
        assert "items" in data and "total" in data
        # total should be >= 13
        assert data["total"] >= 13
        # items length for page 2 should be total - 10 (at most 10)
        expected_len = max(0, data["total"] - 10)
        assert len(data["items"]) == expected_len

    def test_search_query_filters_results(self, client, auth_token):
        # Create a user with a distinctive name/email
        unique_name = f"UniqueName{uuid.uuid4().hex[:6]}"
        unique_email = f"{unique_name.lower()}@example.com"
        user_data = {
            "nome": unique_name,
            "sobrenome": "Filtro",
            "email": unique_email,
            "password": "senha123",
        }
        resp = request_auth(
            client, "POST", "/admin/usuarios/", token=auth_token, json=user_data
        )
        assert resp.status_code == 201

        # Search by part of the name
        q = unique_name[:6]
        resp_search = request_auth(
            client, "GET", f"/admin/usuarios/?q={q}", token=auth_token
        )
        assert resp_search.status_code == 200
        data = resp_search.json()
        # expect at least one result and that returned items contain our user
        assert data["total"] >= 1
        emails = [u["email"] for u in data["items"]]
        assert unique_email in emails

    def test_search_no_results_returns_empty(self, client, auth_token):
        resp = request_auth(
            client,
            "GET",
            "/admin/usuarios/?q=this_query_should_not_match_anyone",
            token=auth_token,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["items"] == []
