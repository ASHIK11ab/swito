from functools import wraps
from flask import flash, redirect, url_for, session
from models import access, Customer

def login_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    if "user" not in session:
      flash("Unauthorised access", "danger")
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return wrapper

def admin_login_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    if Customer.query.with_entities(Customer.access_lvl).filter(Customer.cust_name == session["user"]).first()[0] != access["admin"]:
      flash("Unauthorised access", "danger")
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return wrapper
