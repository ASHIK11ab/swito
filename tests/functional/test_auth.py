from tests.functional.test_index import client
from app import app
import string 
import random

def login(client, username, password):
  """ Fires a post request to the login route """
  return client.post("/login", data=dict(
    username = username,
    password = password
  ), follow_redirects=True)


def generate_random_string():
  """ Generates a random string """
  return ''.join(random.choices(string.ascii_letters, k = 15))


def register(client, username, password, confirm_password):
  """ Fires a post request to the register route """
  return client.post("/register", data=dict(
    username = username,
    password = password,
    confirm_password = confirm_password
  ), follow_redirects=True)


def logout(client):
  return client.get("/logout", follow_redirects=True)


def test_login_logout(client):
  """
    GIVEN username and password
    WHEN a user logs in
    CHECK whether the login and logout functionalities work properly
  """
  username = app.config["TEST_USERNAME"]
  password = app.config["TEST_PASSWORD"]

  # On successfull login user is redirected to dashboard
  resp = login(client, username, password)
  assert resp.status_code == 200
  assert b"Shop by category" in resp.data
  
  # Unsuccessfull login
  resp = login(client, username + "X", password + "Y")
  assert resp.status_code == 200
  assert b"Invalid username or password" in resp.data

  # User is redirected to login page on successfull logout
  resp = logout(client)
  assert resp.status_code == 200
  assert b"Login to Swito" in resp.data


def test_new_registration(client):
  """
    GIVEN user credentials
    WHEN a user registers for an account
    THEN check whether registration functionality works properly
  """
  # Registering new user with randomly generated credentials
  username = "RANDOM_" + generate_random_string()
  password = generate_random_string()
  resp = register(client, username, password, password)
  assert resp.status_code == 200
  assert b"Shop by category" in resp.data

  # Registering with a existing username
  resp = register(client, app.config["TEST_USERNAME"], 
                    app.config["TEST_PASSWORD"], 
                    app.config["TEST_PASSWORD"])
  assert resp.status_code == 200
  assert b"Username aldready exists" in resp.data

  # When passwords dont match
  resp = register(client, app.config["TEST_USERNAME"], "pass", "pass1")
  assert resp.status_code == 200
  assert b"Passwords dont match" in resp.data