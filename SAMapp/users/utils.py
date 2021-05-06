import os
import secrets
from PIL import Image
from flask import url_for, current_app

#Saving the profile pic
def save_picture(form_picture):
	#Creates a random 8 bit hex code to assign the image name so we dont have repeat names in the db
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn =random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	
	#Resizing the image before saving
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)		
	i.save(picture_path)

	return picture_fn

#Saving the animal pic
def save_picture_animal(animal_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(animal_picture.filename)
	picture_fn =random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/animal_pics', picture_fn)
	
	output_size = (125, 125)
	i = Image.open(animal_picture)
	i.thumbnail(output_size)		
	i.save(picture_path)
	return picture_fn