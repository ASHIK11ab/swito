"""
  utils.helperfuncs.py
  ~~~~~~~~~~~~~~~~~~~~

  Contains the utility functions which are used by 
  the application.
"""

from werkzeug.security import check_password_hash
from schema.models import *
from flask import current_app as app
import requests

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


def valid_extension(filename):
  return filename.lower().rsplit('.')[1] in app.config['FOOD_IMAGE_EXTENSIONS']


def food_tag_available(tag_name):
  """
    Checks whether a food tag is available or aldready exists 
    :param tag_name: name of the tag to be checked
    :return: boolean indicating whether tag is available or not
    :rtype: boolean
  """
  tags = Tags.query.all()
  for tag in tags:
    # Return False if tag name aldready exists.
    if tag.name == tag_name:
      return False
  return True


def create_food_tag(tag_name):
  """ Adds a created food tag to database """
  tag = Tags(name=tag_name)
  db.session.add(tag)
  db.session.commit()


def get_food_tags():
  """ Returns all food tags """
  return Tags.query.all()