"""
  tests.functional
  ~~~~~~~~~~~~~~~~~~~~

  Contains all of the integration tests for the application.
"""
from app import app

ADMIN_USERNAME = app.config['TEST_ADMIN_USERNAME']
ADMIN_PASSWORD = app.config['TEST_ADMIN_PASSWORD']