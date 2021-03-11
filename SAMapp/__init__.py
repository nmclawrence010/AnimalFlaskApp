from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '13599689ffaf3677d1795666ba382357'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
db= SQLAlchemy(app)

from SAMapp import routes