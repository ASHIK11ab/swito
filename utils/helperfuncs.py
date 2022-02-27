"""
  utils.helperfuncs.py
  ~~~~~~~~~~~~~~~~~~~~

  Contains the utility functions which are used by 
  the application.
"""

from datetime import datetime
from werkzeug.security import check_password_hash
from schema.models import *
from flask import current_app as app
import requests

def get_current_date():
  """ Returns the current date in `dd/mm/yyyy` format. """
  date = datetime.now()
  current_date = f"{date.day}/{date.month}/{date.year}"
  return current_date


def get_current_time():
  """ Returns the current time in 12 hrs `hh:mm` format. """
  date = datetime.now()
  # Set `AM` and `PM` accordingly.
  if date.hour > 12:
    hour = date.hour - 12
    time = f"{hour}:{date.minute} PM"
  else:
    hour = date.hour
    time = f"{hour}:{date.minute} AM"
  return time


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
  """
    Adds a new user to the database.

    :param username: username of the user
    :param password: password of the user
  """
  user = User(username=username, password=password)
  db.session.add(user)
  db.session.commit()


def get_user(username):
  """
    Returns a users details

    :param username: username of the user
    :return: information of the user
    :rtype: User object
  """
  return User.query.filter(User.username == username).first()


def valid_extension(filename):
  return filename.lower().rsplit('.')[1] in app.config['ALLOWED_IMAGE_EXTENSIONS']


def food_tag_exists(tag_name):
  """
    Checks whether a food tag aldready exists .
    :param tag_name: name of the tag to be checked
    :return: boolean indicating whether tag exists or not
    :rtype: boolean
  """
  tags = Tags.query.all()
  for tag in tags:
    # Return False if tag name aldready exists.
    if tag.name == tag_name:
      return True
  return False


def create_food_tag(tag_name):
  """ Adds a food tag to database """
  tag = Tags(name=tag_name)
  db.session.add(tag)
  db.session.commit()


def get_tags():
  """ Returns all food tags """
  return Tags.query.all()


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


def get_similar_foods(food_id):
  """ 
    Returns the foods which are similar to a given food.

    :param food_id: Id of the food for which similar foods are to be found
    :return: list of foods which are similar to the given food
    :rtype: list
  """

  # List of tags which the selected food contains which is used
  # for finding similar foods of a given food.
  tags = get_food_tags(food_id)

  # Get details of tags associated with each food.
  result = FoodTag.query.with_entities(FoodTag.food_id, FoodTag.tag_name).all()

  # A food is qualified if it contains atleast one tag which is 
  # part of the list of tags of the selected food. Avoid the food
  # selected by the user and choosing same foods again.
  qualified_food_ids = []
  for foodId, tagname in result:
    if tagname in tags and foodId != food_id and foodId not in qualified_food_ids:
      qualified_food_ids.append(foodId)
  
  # Get details of the foods whose id is part of the `qualified_food_ids`.
  similar_foods = []
  for foodId in qualified_food_ids:
    res = db.session.query(Food, FoodTag)\
            .with_entities(Food.id, Food.name, Food.price,
                            Food.img_url, FoodTag.tag_name)\
            .filter(Food.id == FoodTag.food_id, Food.id == foodId).first()

    food = {
      'id': res.id,
      'name': res.name,
      'price': res.price,
      'img_url': res.img_url,
      'tag': res.tag_name
    }
    similar_foods.append(food)
  
  return similar_foods


def can_add_item_to_cart(food_id, quantity, username):
  """ 
    Performs the necessary checks before adding an item to cart.

    :param food_id: Id of the food to be added to cart
    :param quantity: Quantity of the food to be added
    :param username: Username of the user
    :return: A tuple of status and the response message
    :rtype: tuple  
  """
  food, tags = get_food_info(food_id)
  
  if food is None:
    return (False, 'Invalid food id')
  
  if quantity > food.quantity:
    return (False, 'Enter lesser quantity')

  # Check if the selected food is aldreadly in cart or not.
  cart_food = db.session.query(User, Cart).filter(
                User.id == Cart.user_id, User.username == username, 
                Cart.food_id == food.id).first()

  if not cart_food is None:
    return (False, 'Item aldready in cart')
  
  return (True, 'Added to cart successfully')