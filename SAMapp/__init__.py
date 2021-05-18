import os
from flask import Flask, g, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from SAMapp.config import Config
from SAMapp import QRCode
from flask_mail import Mail


db= SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view ='users.login'
login_manager.login_message_category = 'info'
mail = Mail()
 
from SAMapp.models import User, Post, Animal

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	
	db.init_app(app)

	with app.app_context():
		db.create_all()

	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from SAMapp.users.routes import users
	from SAMapp.posts.routes import posts
	from SAMapp.main.routes import main

	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app

#db.create_all(app=create_app())