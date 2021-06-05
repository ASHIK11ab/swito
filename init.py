from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Dynamically loading configuration based on environment.
if app.config['ENV'] == 'production':
  app.config.from_object('configuration.Config')
elif app.config['ENV'] == 'development':
  app.config.from_object('configuration.DevelopmentConfig')

db = SQLAlchemy(app)