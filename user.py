from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from database import select
from flask import current_app

secret_key = '\x14\xf6T;\xbd7\xf5"\xf8\x82\x1d\xdd\x84\x02\x95.Qx\xdb\x9b'
login_serializer = URLSafeTimedSerializer(secret_key)

class User(UserMixin):

  def __init__(self, dictionary):
    self.id = dictionary["id"]
    self.pw_hash = dictionary["hash"]

  def get_auth_token(self):
    data = [str(self.id), self.pw_hash]
    return login_serializer.dumps(data)

def get_user(userid):
  """Given a user ID, this function fetches that user object from the database.
  The caller will handle the authentication by looking at the hash."""
  users = select("SELECT * FROM users WHERE id = %s", (int(userid),))
  if not users:
    return None
  return User(users[0])

def load_token(token):
  """Give a token securely stored in a cookie using our app secret, we will
  deserialize the token into its constituent parts and then validate it."""
  # We serialize the time the cookie was generated into the cookie itself
  max_age = current_app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
  data = login_serializer.loads(token, max_age=max_age)
  user = get_user(data[0])
  if user and user.pw_hash == data[1]:
    return user
  return None
