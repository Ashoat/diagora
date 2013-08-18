from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required
from user import User
from database import select
from wtforms import Form, TextField, PasswordField, validators
from hashlib import sha256
import binascii
from os import urandom

login_bp = Blueprint('login', __name__)

class LoginForm(Form):
  email = TextField('Email', [validators.Email()])
  password = PasswordField('Password', [validators.Required()])

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
  """Controller for the log in page."""
  # TODO: redirect back to where we came from
  form = LoginForm(request.form)
  if request.method == 'GET' or not form.validate():
    return render_template('login.html', form=form)
  users = select("SELECT * FROM users WHERE email = %s", (form.email.data,))
  if not users:
    return render_template(
      'error.html',
      message="Could not find user!"
    )
  password = form.password.data.encode('ascii')
  salt = binascii.unhexlify(users[0]['salt'])
  pw_hash = sha256(password + salt).hexdigest()
  if pw_hash != users[0]['hash']:
    return render_template(
      'error.html',
      message="Could not find user!"
    )
  login_user(User(users[0]), remember=True)
  return redirect(url_for('home.home'))

@login_bp.route('/logout')
@login_required
def logout():
  """Controller for the log out page."""
  # TODO: redirect back to where we came from
  logout_user()
  return redirect(url_for('home.home'))

class RegistrationForm(Form):
  name = TextField('Name', [validators.Length(min=4, max=25)])
  email = TextField('Email Address', [validators.Email()])
  password = PasswordField('Password', [
    validators.Required(),
    validators.EqualTo('confirm'),
  ])
  confirm = PasswordField('Repeat Password')

@login_bp.route('/register', methods=['GET', 'POST'])
def register():
  """Controller for the register page."""
  # TODO: redirect back to where we came from
  form = RegistrationForm(request.form)
  if request.method == 'GET' or not form.validate():
    return render_template('register.html', form=form)
  users = select("SELECT * FROM users WHERE email = %s", (form.email.data,))
  if users:
    return render_template(
      'error.html',
      message="An account with that email already exists!",
    )
  password = form.password.data.encode('ascii')
  salt = urandom(6)
  pw_hash = sha256(password + salt).hexdigest()
  hexlified = binascii.hexlify(salt)
  rows = select(
    "INSERT INTO users (email, name, hash, salt) VALUES(%s, %s, %s, %s) "
    "RETURNING id",
    (form.email.data, form.name.data, pw_hash, hexlified),
  )
  if not rows:
    return render_template(
      'error.html',
      message="Database error :(",
    )
  login_user(User(rows[0]), remember=True)
  return redirect(url_for('home.home'))
