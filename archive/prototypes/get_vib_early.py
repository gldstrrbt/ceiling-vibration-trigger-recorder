#!<local-user-path>/miniconda3/envs/vib/bin/python
import os, serial, time, datetime

video_dir = "video_export"

def open_serial():
	a = serial.Serial("/dev/ttyACM0", 9600, timeout=5)
	return a

def vid_count():
	return len(os.listdir(video_dir))

def get_time_now():
	a = str(datetime.datetime.now())
	a = a.split(".")[0]
	a = a.replace(" ", "_")
	return a

def record():
	#a = vid_count()
	b = get_time_now()
	os.system("ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 1280x720 -r 25 -i /dev/video0 -t 00:00:01 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(b)+".avi")

def init():
	#try:
	a = open_serial()
	while True:
		#try:
		if "movement detected" in str(a.readline()).lower():
			a.flushInput()
			a.flushOutput()
			time.sleep(0.2)
			print(a.readline())
			record()
			time.sleep(0.2)
			a.flushInput()
			a.flushOutput()
			#except:
			#	pass
	#except:
	#	time.sleep(2)
	#	init()

init()