#!/usr/bin/python

from os import listdir
from os.path import isfile, join
import datetime
import os
import shutil

hourOFF = datetime.timedelta(hours=-8)

mypath = os.getcwd()
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
print onlyfiles

shutil.rmtree("old",ignore_errors=True)
os.mkdir('old')


for fi in onlyfiles:
	filesplit = fi.split('.')
	if filesplit[-1].lower() == 'jpg':
		shutil.copy(fi,'old/'+fi)
		imagesplit = filesplit[0].split('_')
		if len(imagesplit)==3:
			ymd = imagesplit[0]
			hms = imagesplit[1]
			year = int(ymd[0:4])
			month = int(ymd[4:6])
			day = int(ymd[6:8])
			hour = int(hms[0:2])
			minute = int(hms[2:4])
			sec = int(hms[4:6])
			dateimg = datetime.datetime(year,month,day,hour,minute,sec)
	#		print dateimg
	#		print dateimg + hourOFF
			dateimg = dateimg + hourOFF
			newname = dateimg.strftime('%Y%m%d_%H%M%S')
			print newname
			os.rename(fi,newname+'.jpg')
		#Change Date

