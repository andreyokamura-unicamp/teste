#from distutils.log import debug 
#from fileinput import filename 
from flask import Flask

app = Flask(__name__)
#from app.main import *

    
@app.route('/')
def homepage():
    return "teste"

if __name__ == '__main__':
    app.run()

