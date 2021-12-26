from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), nullable=False, unique=True)
  password = db.Column(db.String(256), nullable=False)

  def __init__(self, username, password):
    self.username = username
    self.password = generate_password_hash(password)


class Food(db.Model):
  __tablename__ = "foods"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  price = db.Column(db.Float, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  img_url = db.Column(db.String(70), nullable=False)

  def add_tags(self, tags):
    """ Adds a list of tags associated with the food to the database. """
    tag_objects = []
    for tag in tags:
      food_tag = FoodTag(food_id=self.id, tag_name=tag)
      tag_objects.append(food_tag)
    db.session.add_all(tag_objects)


class Order(db.Model):
  __tablename__ = "orders"
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.String(10), nullable=False)
  time = db.Column(db.String(8), nullable=False)
  total_amount = db.Column(db.Float, nullable=False)


class Tags(db.Model):
  __tablename__ = "tags"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(15), nullable=False, unique=True)


class UserInfo(db.Model):
  __tablename__ = "user_info"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  phone = db.Column(db.String(15), nullable=True, unique=True)
  street_name = db.Column(db.String(40), nullable=False)
  city = db.Column(db.String(30), nullable=False)
  state = db.Column(db.String(30), nullable=False)
  country = db.Column(db.String(30), nullable=False)
  pincode = db.Column(db.String(10), nullable=False)


class UserOrder(db.Model):
  __tablename__ = "user_orders"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), 
    nullable=False, unique=True)


class OrderItem(db.Model):
  __tablename__ = "order_items"
  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
  food_name = db.Column(db.String(30), nullable=False)
  price = db.Column(db.Float, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)


class Cart(db.Model):
  __tablename__ = "cart"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  food_id = db.Column(db.Integer, db.ForeignKey("foods.id"), nullable=False)
  quantity = db.Column(db.Integer, nullable=False)


class FoodTag(db.Model):
  __tablename__ = "food_tags"
  id = db.Column(db.Integer, primary_key=True)
  food_id = db.Column(db.Integer, db.ForeignKey("foods.id"), nullable=False)
  tag_name = db.Column(db.String(15), nullable=False)