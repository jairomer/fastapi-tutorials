from fastapi.testclient import TestClient

from .main import app 

client = TestClient(app)

def test_get_hello_world():
    response = client.get("/helloworld")
    assert response.status_code == 200
    assert response.json() == "Hello World"


