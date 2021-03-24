import pyqrcode
global text
import shutil
import os

def qrgen(s):
	qr = pyqrcode.create(s)
	qr.png(s+'.png',scale = 8)
	original = r'' + s + '.png'
	target = r'SAMapp/static/qr_codes//' + s + '.png'

	shutil.move(original,target)