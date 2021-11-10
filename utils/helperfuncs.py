"""
  utils.helperfuncs.py
  ~~~~~~~~~~~~~~~~~~~~

  Contains the utility functions which are used by 
  the application.
"""

from werkzeug.security import check_password_hash
from schema.models import *

def login_valid(username, password):
  """ Validates the credentials of the user.

    :param username: username of the user
    :param password: password of the user
    :return: a boolean indicating whether login is valid or not
    :rtype: boolean
  """

  user = User.query.filter(User.username == username).first()
  # Return false if the username is invalid or if the passwords
  # dont match.
  if user is None or not check_password_hash(user.password, password):
    return False
  else:
    return True


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