
from flask import render_template, Flask
from wsgi import app

@app.route('/')
def homepage():
    return render_template('index.html', name='', file = None)