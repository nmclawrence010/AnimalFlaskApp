from datetime import datetime
from flask import url_for, current_app
from SAMapp import db, login_manager
from flask_login import UserMixin 


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


#Database model for User accounts
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#Database model for forum posts
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"


#Model for classifications (Mammals, reptiles etc)
class Classification(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	classification_type = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Classification('{self.classificationType}')"


#Model for the animals
class Animal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	species = db.Column(db.String(75), nullable=False)
	feeding_information = db.Column(db.String(200), nullable=False)
	residency_status = db.Column(db.String(200), nullable=False)
	extra_information = db.Column(db.String(200))
	animal_image = db.Column(db.String(20), default='defaultanimal.jpg')
	animal_qr = db.Column(db.String(20))
	
	def __repr__(self):
		return f"Animal('{self.species}', '{self.feeding_information}', '{self.residency_status}', '{self.animal_image}', '{self.extra_information}')"


#Storing feedings
class Feedings(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	extra_info = db.Column(db.String(60))

	def __repr__(self):
		return f"Feedings('{self.user_id}', '{self.date_completed}', '{self.extra_info}')"


#Storing Cleanings
class Cleanings(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	extra_info = db.Column(db.String(60))

	def __repr__(self):
		return f"Cleanings('{self.user_id}', '{self.date_completed}', '{self.extra_info}')"


#Monitoring Information
class Monitoring(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	extra_info = db.Column(db.String(60))

	def __repr__(self):
		return f"Monitoring('{self.user_id}', '{self.date_completed}', '{self.extra_info}')"