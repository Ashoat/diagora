import os
import psycopg2
import psycopg2.extras
import urlparse
from flask import g

def get_db():
  """Flask request has to be initiated before this can be used. This also
  assumes that we're using Heroku and the DB URL is an environmental variable"""
  db = getattr(g, 'db', None)
  if db is not None:
    return db
  urlparse.uses_netloc.append("postgres")
  url = urlparse.urlparse(os.environ["DATABASE_URL"])
  g.db = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port,
  )
  return g.db

def close_connection(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

def select(query, args=()):
  cursor = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
  cursor.execute(query, args)
  results = cursor.fetchall()
  cursor.close()
  return results
