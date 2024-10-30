#from distutils.log import debug 
#from fileinput import filename 
from flask import Flask

app = Flask(__name__)
#from app.main import *

if __name__ == '__main__':
    app.run()
    
@app.route('/')
def homepage():
    return "teste"
