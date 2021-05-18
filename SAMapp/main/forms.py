from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from SAMapp.models import User, Animal


class AddAnimalForm(FlaskForm): 
	species = StringField('Species', validators=[DataRequired()])
	feeding_information = StringField('Feeding Information', validators=[DataRequired(), Length(max =200)])
	residency_status = StringField('Residency Status', validators=[DataRequired(), Length(max =200)])
	extra_information = TextAreaField('Extra Information')
	submit = SubmitField('Add Animal')

	#Makes sure we cant have repeat species names
	def validate_animal(self, species):
		animal = Animal.query.filter_by(species=species.data).first()
		if animal:
			raise ValidationError('That animal already exists. Please choose a different one.')

#For changing each animals current info
class UpdateAnimalInfoForm(FlaskForm):
	species = StringField('Species', validators=[DataRequired()])
	feeding_information = StringField('Feeding Information', validators=[DataRequired(), Length(max =200)])
	residency_status = StringField('Residency Status', validators=[DataRequired(), Length(max =200)])
	extra_information = TextAreaField('Extra Information')
	picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update Animal')

#Form for adding feedings
class AddFeedingForm(FlaskForm):
	#date_time = DateTimeField('Date & Time')
	extra_information = StringField('Extra Information', validators=[Length(max =150)])
	submit = SubmitField('Submit')

#Form for adding cleanings
class AddCleaningForm(FlaskForm):
	extra_information = StringField('Extra Information', validators=[DataRequired(), Length(max =150)])
	submit = SubmitField('Submit')

#Form for adding monitoring
class AddMonitoringForm(FlaskForm):
	extra_information = StringField('Extra Information', validators=[DataRequired(), Length(max =150)])
	submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	#Makes sure we cant have repeat emails
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email, You must register first')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')