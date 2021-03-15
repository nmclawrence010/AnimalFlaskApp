from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from SAMapp.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max =20)])
	email = StringField('Email', validators=[DataRequired(), Email()])

	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	#Makes sure we cant have repeat usernames
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	#Makes sure we cant have repeat emails
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember =  BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max =20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	#Makes sure we cant have repeat usernames
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	#Makes sure we cant have repeat emails
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.')

class AddAnimal(FlaskForm):
	#Dropdown for selecting classification
	classification = ['Mammal', 'Reptile', 'Amphibian', 'Bird', 'Fish', 'Invertebrate']
	seqSimilarity = SelectField('Delivery Types', choices=classification, default=1)
	species = StringField('Species', validators=[DataRequired()])
	feeding_information = StringField('Feed Information', validators=[DataRequired(), Length(max =150)])
	residency_status = StringField('Residency Status', validators=[DataRequired(), Length(max =150)])
	#qrCode_image = 
