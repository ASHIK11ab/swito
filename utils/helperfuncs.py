"""
  utils.helperfuncs.py
  ~~~~~~~~~~~~~~~~~~~~

  Contains the utility functions which are used by 
  the application.
"""

from models import *
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


def get_category_of_user(username):
  """ Finds a category of the user.

  :param username: username of the user
  :return: a string representing the category of the user
  :rtype: str
  """
  p = Purchase.query.filter(
    and_(
      Purchase.cust_id == Customer.id,
      Customer.cust_name == username
    )
  ).first()

  if p is None:
    return 'Bronze'
  else:
    return p.category


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
  # Adding a user to customer entity.
  user.add_customer()