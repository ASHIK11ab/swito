"""
  utils.decorators.py
  ~~~~~~~~~~~~~~~~~~~~

  Contains user defined decorators which are 
  used by the application.
"""

from functools import wraps
from flask import flash, redirect, url_for, session

def login_required(f):
  """ Prevents access to routes if user is not logged in. """
  @wraps(f)
  def wrapper(*args, **kwargs):
    if "user" not in session:
      flash("Access Denied. Sign in required.", "danger")
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return wrapper


def admin_login_required(f):
  """ Prevents unauthorised access to admin routes. """
  @wraps(f)
  def wrapper(*args, **kwargs):
    if session["user"] != "Admin":
      flash("Access denied. Admin login required.", "danger")
      return redirect(url_for('login'))
    return f(*args, **kwargs)
  return wrapper
