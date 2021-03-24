from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from SAMapp.models import User, Animal


class AddAnimalForm(FlaskForm):
	#classification = ['Mammal', 'Reptile', 'Amphibian', 'Bird', 'Fish', 'Invertebrate']
	#seqSimilarity = SelectField('Delivery Types', choices=classification) #SPAGHETTI 
	species = StringField('Species', validators=[DataRequired()])
	feeding_information = StringField('Feeding Information', validators=[DataRequired(), Length(max =200)])
	residency_status = StringField('Residency Status', validators=[DataRequired(), Length(max =200)])
	extra_information = TextAreaField('Extra Information')
	submit = SubmitField('Add Animal')
	  

#For changing each animals current info
class UpdateAnimalInfoForm(FlaskForm):
	species = StringField('Species', validators=[DataRequired()])
	feeding_information = StringField('Feeding Information', validators=[DataRequired(), Length(max =200)])
	residency_status = StringField('Residency Status', validators=[DataRequired(), Length(max =200)])
	extra_information = TextAreaField('Extra Information')
	animal_image = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update Animal')

#Selecting current animal??????????????????????
#class SelectCurrentAnimalForm(FlaskForm):
	#select_animal = dropdown of animals

#Form for adding feedings
class AddFeedingForm(FlaskForm):
	completed = BooleanField('Completed')
	date_time = DateTimeField('Date & Time')
	extra_information = StringField('Extra Information', validators=[DataRequired(), Length(max =150)]) 

#Form for adding cleanings
class AddCleaningForm(FlaskForm):
	completed = BooleanField('Completed')
	date_time = DateTimeField('Date & Time')
	extra_information = StringField('Extra Information', validators=[DataRequired(), Length(max =150)])

#Form for adding monitoring
class AddMonitoringForm(FlaskForm):
	completed = BooleanField('Completed')
	date_time = DateTimeField('Date & Time')
	extra_information = StringField('Extra Information', validators=[DataRequired(), Length(max =150)])