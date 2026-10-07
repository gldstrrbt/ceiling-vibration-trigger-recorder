import os, serial, datetime, subprocess, time, psutil, signal

serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
video_dir 	= "video_export"
threshold 	= 50
avg_reading = []

def get_time_now():
	a = str(datetime.datetime.now())
	a = a.split(".")[0]
	a = a.replace(" ", "_")
	return a


def record():
	os.system("sudo pkill ffmpeg")
	a = get_time_now()
	############## VVVVV WORKS VVVVV ##############
	############## VVVVV WORKS VVVVV ##############
	############## VVVVV WORKS VVVVV ##############
	# b = "ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 1280x720 -r 25 -i /dev/video0 -t 00:00:03 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(a)+".avi"
	b = "ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 640x480 -r 25 -i /dev/video0 -t 00:00:03 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(a)+".avi"
	############## ^^^^^ WORKS ^^^^^ ##############
	############## ^^^^^ WORKS ^^^^^ ##############
	############## ^^^^^ WORKS ^^^^^ ##############
	# b = "ffmpeg -f alsa -thread_queue_size 1024 -i default -itsoffset 00:00:00 -f video4linux2 -s 640x480 -r 25 -i /dev/video0 -t 00:00:03 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(a)+".avi"
	###############################################
	###############################################
	###############################################
	c = subprocess.call(b, shell=True, stdin=subprocess.PIPE)


def get_max():
	global avg_reading
	return max(avg_reading)

def read_from_port(ser):
	global avg_reading
	global threshold

	while True:
		msg = ser.readline()
		msg = str("".join(map(chr, msg))).replace("\r\n", "")
		print(msg)
		if ser.in_waiting > 0 and msg.isdigit() == True:
	
			if len(avg_reading) < 100:
				avg_reading.append(int(msg))
				threshold = get_max()
				print(threshold)
			elif len(avg_reading) >= 100 and int(msg) > threshold:
				print([v.terminate() for v in psutil.process_iter() if "ffmpeg" in str(v)])
				record()
				ser.reset_input_buffer()
				print([v.terminate() for v in psutil.process_iter() if "ffmpeg" in str(v)])
				print(ser.in_waiting)
				print(msg)
				print(msg)
				print(msg)
				ser.reset_input_buffer()
				time.sleep(1)
				ser.reset_input_buffer()
				print("*"*50)
				print("READY ON STANDBY")
				print("*"*50)


def init():
	read_from_port(serial_port)


init()