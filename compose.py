from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from wtforms import Form, TextField, TextAreaField, validators
from database import select
import re

compose_bp = Blueprint('compose', __name__)

class ComposeForm(Form):
  title = TextField('Title', [validators.Length(min=4, max=50)])
  topics = TextField(
    'Topics',
    [validators.Regexp(r'^\s*(#[a-zA-Z0-9_-]+\s*)*$')]
  )
  body = TextAreaField('Body', [validators.Length(min=4, max=5000)])

def topic_strings_to_ids(topics):
  # First, see if they exist
  in_clause = ','.join(('%s',) * len(topics))
  print in_clause
  results = select(
    'SELECT * FROM topics WHERE name IN (%s)' % in_clause,
    topics,
  ) 
  # Figure out which topics already exist
  ids = []
  need_creation = []
  for topic in topics:
    found = False
    for result in results:
      if topic == result["name"]:
        ids.append(result["id"])
        found = True
        break
    if not found:
      need_creation.append(topic)
  if not need_creation:
    return ids
  values_clause = ','.join(('(%s)',) * len(need_creation))
  creation = select(
    'INSERT INTO topics(name) VALUES %s RETURNING *' % values_clause,
    need_creation,
  )
  for row in creation:
    ids.append(row["id"])
  return ids

@compose_bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
  form = ComposeForm(request.form)
  if request.method == 'GET' or not form.validate():
    return render_template('compose.html', form=form, user=current_user)
  # First, get the topics
  topics = re.compile(r'#([a-zA-Z0-9_-]+)\s*').findall(form.topics.data)
  topic_ids = []
  if topics:
    topic_ids = topic_strings_to_ids(topics)
  if len(topic_ids) != len(topics):
    return render_template(
      'error.html',
      message="Database error :(",
    )
  # Next, create the post
  rows = select(
    'INSERT INTO posts (title, body, "user") VALUES(%s, %s, %s) RETURNING *',
    (form.title.data, form.body.data, current_user.get_id()),
  )
  if not rows:
    return render_template(
      'error.html',
      message="Database error :(",
    )
  post_id = rows[0]["id"]
  # Finally, create the topic associations
  if topic_ids:
    values_clause = ','.join(('(%s, %s)',) * len(topic_ids))
    values = sum([(post_id, topic_id) for topic_id in topic_ids], ())
    select(
      'INSERT INTO tags("from", "to") VALUES %s RETURNING *' % values_clause,
      values,
    )
  return redirect(url_for('post.post', post=post_id))
