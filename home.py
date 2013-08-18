from flask import Blueprint, render_template, request
from flask_login import current_user
from wtforms import Form, TextField, validators
from database import select
from bs4 import BeautifulSoup
import re

home_bp = Blueprint('home', __name__)

class FilterForm(Form):
  topics = TextField(
    'Topics',
    [validators.Regexp(r'^\s*(#[a-zA-Z0-9_-]+\s*)*$')],
  )

def parse_post(post):
  # Only keep the first line; no newlines please
  soup = BeautifulSoup(post["body"])
  for tag in soup.findAll(True):
    tag.hidden = True
  post["body"] = soup.renderContents()
  return post

def topic_strings_to_ids(topics):
  # First, see if they exist
  in_clause = ','.join(('%s',) * len(topics))
  results = select(
    'SELECT * FROM topics WHERE name IN (%s)' % in_clause,
    topics,
  ) 
  # Figure out which topics already exist
  ids = []
  for topic in topics:
    for result in results:
      if topic == result["name"]:
        ids.append(result["id"])
        break
  return ids

@home_bp.route('/', methods=['GET', 'POST'])
def home():
  form = FilterForm(request.form)
  topic_ids = []
  if request.method == 'POST' and form.validate():
    topics = re.compile(r'#([a-zA-Z0-9_-]+)\s*').findall(form.topics.data)
    if topics:
      topic_ids = topic_strings_to_ids(topics)
  if not topic_ids:
    posts = select(
      "SELECT p.*, u.name FROM posts p LEFT JOIN users u ON u.id = p.user"
    )
  else:
    in_clause = ','.join(('%s',) * len(topic_ids))
    posts = select(
      'SELECT p.*, u.name FROM posts p '
      'LEFT JOIN users u ON u.id = p.user '
      'INNER JOIN tags t ON t."from" = p.id AND t."to" IN (%s)' % in_clause,
      topic_ids,
    )
  parsed = [parse_post(post) for post in posts]
  return render_template(
    'home.html',
    posts=parsed,
    user=current_user,
    form=form,
  )
