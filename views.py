
from flask import render_template, request, redirect
from main import app



@app.route('/')
def homepage():
    return render_template('index.html', name='', file = None)