"""
  utils.helperfuncs.py
  ~~~~~~~~~~~~~~~~~~~~

  Contains the utility functions which are used by 
  the application.
"""

from schema.models import *
from sqlalchemy import and_

def login_valid(username, password):
  """ Validates the credentials of the user.

    :param username: username of the user
    :param password: password of the user
    :return: a boolean indicating whether login is valid or not
    :rtype: boolean
  """
  return not User.query.filter(
    and_(
      User.username == username,
      User.password == password
      )
    ).first() is None


def username_exists(username):
  """ Checks if a username aldready exists

    :param username: username to be checked
    :return: Boolean indicating whether the username exists or not
    :rtype: boolean
  """
  return not User.query.filter_by(
    username=username).first() is None


def add_user(username, password):
  """ Adds a new user to the database.

  :param username: username of the user
  :param password: password of the user
  """
  user = User(username=username, password=password)
  db.session.add(user)
  db.session.commit()