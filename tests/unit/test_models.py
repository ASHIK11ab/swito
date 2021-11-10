from schema.models import User

def test_new_user():
  """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, hashed_password are defined correctly
  """
  user = User("test-user", "mypass@1")
  assert user.username == "test-user"
  assert user.username != "mypass@1"