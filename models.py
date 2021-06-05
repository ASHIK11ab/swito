from flask import flash, session
from init import db

access = {
  "normal-user": 1,
  "admin": 2
}

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  password = db.Column(db.String(20), nullable=False)

  def add_customer(self, phone):
    access_lvl = 1
    if(self.username == 'Admin' or self.username == 'admin'):
      access_lvl = 2
    customer = Customer(cust_name=self.username, phone=phone, access_lvl=access_lvl)
    db.session.add(customer)
    db.session.commit()

class Customer(db.Model):
  __tablename__ = "customers"
  id = db.Column(db.Integer, primary_key=True)
  cust_name = db.Column(db.String, nullable=False)
  phone = db.Column(db.Integer)
  access_lvl = db.Column(db.Integer, nullable = False)

class Food(db.Model):
  __tablename__ = "foods"
  id = db.Column(db.Integer, primary_key=True)
  food_name = db.Column(db.String, nullable=False)
  cost = db.Column(db.Integer, nullable=False)

  def addOrder(self, username):
    customer = Customer.query.filter(Customer.cust_name == username).first()
    order = Order(cust_id = customer.id, food_id = self.id)
    p = Purchase.query.filter(Purchase.cust_id == customer.id).first()
    if p is None:
      p = Purchase(cust_id = customer.id, p_cnt = 1)
      db.session.add(p)
    else:
      p.p_cnt += 1
      if p.p_cnt == 2:
        p.category = 'Silver'
        session["category"] = 'Silver'
        flash("Congragulation on becoming a Silver user 🥈")
      elif p.p_cnt == 5:
        p.category = 'Gold'
        flash("Congragulation on becoming a Gold user 🥇")
        session["category"] = 'Gold'
    db.session.add(order)
    db.session.commit()


class Order(db.Model):
  __tablename__ = "orders"
  id = db.Column(db.Integer, primary_key=True)
  cust_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
  food_id = db.Column(db.Integer, db.ForeignKey("foods.id"), nullable=False)

class Purchase(db.Model):
  __tablename__ = "purchase"
  id = db.Column(db.Integer, primary_key=True)
  cust_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
  p_cnt = db.Column(db.Integer, nullable=False)
  category = db.Column(db.String, default="bronze", nullable=True)

