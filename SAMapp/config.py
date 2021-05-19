import os	

class Config:
	SECRET_KEY = '13599689ffaf3677d1795666ba382357'
	SQLALCHEMY_DATABASE_URI ='sqlite:///site.db'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	#MAIL_USERNAME = os.environ.get('EMAIL_USER')
	#MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
	MAIL_USERNAME = 'sercanimalmanagement@gmail.com'
	MAIL_PASSWORD = 'Sercam123'