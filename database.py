import os
import psycopg2
import urlparse
from flask import Flask, g

app = Flask(__name__)

def get_db():
  """Flask request has to be initiated before this can be used. This also
  assumes that we're using Heroku and the DB URL is an environmental variable"""
  db = getattr(g, 'db', None)
  if db is None:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    db = g.db = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port,
    )
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()
