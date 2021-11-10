from init import create_app

def test_new_app():
  """
    GIVEN a application instance
    WHEN a new application is created
    THEN check whether the application and its configurations
      are loaded correctly
  """
  app = create_app({"TESTING": True, "DEBUG": True})
  assert app.config["TESTING"] == True
  assert app.config["DEBUG"] == True