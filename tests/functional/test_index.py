from app import app
import pytest

@pytest.fixture
def client():
  with app.test_client() as test_client:
    yield test_client


def test_home_page(client):
  """
    GIVEN the response of the home page of a application
    WHEN a user visits the index route
    THEN check whether the home page is rendered properly
  """
  response = client.get("/")
  assert response.status_code == 200
  assert b"You will miss your favourite foods again" in response.data