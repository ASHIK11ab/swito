from flask import Flask
from schema.models import db

def create_app(config_dict={}):
  app = Flask(__name__)

  # Dynamically loading configuration based on environment.
  if app.config['ENV'] == 'production':
    app.config.from_object('configuration.Config')
  elif app.config['ENV'] == 'development':
    app.config.from_object('configuration.DevelopmentConfig')
  elif app.config['ENV'] == 'testing':
    app.config.from_object('configuration.TestingConfig')

  # Setting configurations passed during testing.
  for key, value in config_dict.items():
    app.config[key] = value

  db.init_app(app)
  return app