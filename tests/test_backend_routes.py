import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from main import app


client = TestClient(app)


def test_required_health_and_admin_routes_exist():
    for path in ["/health", "/api/health", "/api/admin/system", "/api/v1/admin/system"]:
        response = client.get(path)
        assert response.status_code == 200


def test_chat_route_exists():
    assert any(
        route.path == "/api/v1/chat" and "POST" in route.methods
        for route in app.routes
        if hasattr(route, "methods")
    )
