from init import db

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), nullable=False, unique=True)
  password = db.Column(db.String(256), nullable=False)


class Food(db.Model):
  __tablename__ = "foods"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)
  price = db.Column(db.Float, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)


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
  tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)