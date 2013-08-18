from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from wtforms import Form, TextField, TextAreaField, validators
from database import select

compose_bp = Blueprint('compose', __name__)

class ComposeForm(Form):
  title = TextField('Title', [validators.Length(min=4, max=50)])
  body = TextAreaField('Body', [validators.Length(min=4, max=5000)])

@compose_bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
  form = ComposeForm(request.form)
  if request.method == 'GET' or not form.validate():
    return render_template('compose.html', form=form, user=current_user)
  rows = select(
    'INSERT INTO posts (title, body, "user") VALUES(%s, %s, %s) RETURNING *',
    (form.title.data, form.body.data, current_user.get_id()),
  )
  if not rows:
    return render_template(
      'error.html',
      message="Database error :(",
    )
  return redirect(url_for('post.post', post=rows[0]["id"]))
