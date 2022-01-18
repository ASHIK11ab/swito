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
  """ Adds a food tag to database """
  tag = Tags(name=tag_name)
  db.session.add(tag)
  db.session.commit()


def get_tags():
  """ Returns all food tags """
  return Tags.query.all()


def file_valid(file):
  """ Checks whether the uploaded file format is supported. """
  filename = file.filename
  return filename.rsplit('.')[1] in app.config["ALLOWED_IMAGE_EXTENSIONS"]


def add_food_to_db(name, price, quantity, img_url, tags):
  """ Adds a new food to the database. """
  food = Food(name=name, price=price, quantity=quantity, img_url=img_url)
  db.session.add(food)
  db.session.flush()
  food.add_tags(tags)
  # Commit when food its associated tags are added to database.
  db.session.commit()


def get_dashboard_foods():
  """ 
    Returns the list of foods which are to be displayed in user's dashboard.
    :return: A tuple containing foods and tags.
    :rtype: tuple  
  """

  foods = {}
  tags_to_search_for = ["Trending", "Budget", "Best Sellers"]

  # Select the foods which belongs to the above chosen tags.
  for tag in tags_to_search_for:
    res = db.session.query(Food, FoodTag)\
      .with_entities(Food.id, Food.name, Food.price, 
                      Food.quantity, Food.img_url, FoodTag.tag_name)\
      .filter(Food.id == FoodTag.food_id, FoodTag.tag_name == tag).all()
    foods[tag] = res
  return (foods, tags_to_search_for)


def get_food_tags(food_id):
  """ 
    Returns the list of tags associated with a food. 

    :param food_id: Id of the food whose tags is to be retrieved.
    :return: A list of tags associated with the food.
    :rtype: list
  """

  food_tags = FoodTag.query.with_entities(FoodTag.tag_name)\
    .filter(FoodTag.food_id == food_id).all()
  
  tags = [tag.tag_name for tag in food_tags]
  return tags


def get_food_info(food_id):
  """ 
    Returns a food's info along with its associated tags.

    :param food_id: Id of the food whose info is to be retrieved
    :return: A tuple containing the food's info and its associated tags
    :rtype: tuple
  """

  food = Food.query.get(food_id)
  tags = get_food_tags(food_id)
  return (food, tags)