import os, threading, serial, re, datetime, subprocess, time, psutil, signal

serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
connected 	= False
video_dir 	= "video_export"
fuck 		= []
threshold 	= 100

def get_time_now():
	a = str(datetime.datetime.now())
	a = a.split(".")[0]
	a = a.replace(" ", "_")
	return a

# def record():
# 	#a = vid_count()
# 	b = get_time_now()
# 	os.system("ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 1280x720 -r 25 -i /dev/video0 -t 00:00:01 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(b)+".avi")

def read_from_port(ser):
	global connected
	# global fuck
	# while not connected:
	# 	connected = True

	while True:
		msg = ser.readline()
		msg = str("".join(map(chr, msg))).replace("\r\n", "")
		# print(msg)
		# print(msg.isdigit())
		# if msg.isdigit() == True and int(msg) > 50:
			# fuck.append(int(msg))
			# print(msg)
			# print(msg)
			# print(msg)
			# print(msg)
		# try:
		# if len(fuck) > 3:
			# if fuck[-1:][0] > threhold and fuck[-2:][0] > threhold and fuck[-3:][0] > threhold:
		if ser.in_waiting > 0 and msg.isdigit() == True and int(msg) > threshold:
			print([v.terminate() for v in psutil.process_iter() if "ffmpeg" in str(v)])
			# print(fuck)
			# print("FUCK")
			# fuck = []
			# print("shit")
			record()
			print(ser.in_waiting)
			ser.reset_input_buffer()
			print(ser.in_waiting)
			# print(fuck)
			print("*"*50)
			# time.sleep(1)
		# except:
			# pass

def record():
	a = get_time_now()
	# b = "ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 1280x720 -r 25 -i /dev/video0 -t 00:00:01 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(a)+".avi"
	b = "ffmpeg -f alsa -i default -s 1280x720 -r 25 -i /dev/video0 -t 00:00:03 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(a)+".avi"
	# c = subprocess.Popen(b, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# c = subprocess.Popen(b)
	# c = subprocess.call(b, shell=True)
	c = subprocess.call(b, shell=True, stdin=subprocess.PIPE)
	# fout = c.stdin

	# fout.close()
	# c.wait()
	# if c.returncode !=0: raise subprocess.CalledProcessError(c.returncode,b)
	# print(c)
	# d = c.communicate()[0]
	# print(d)
	# os.system("ffmpeg -f alsa -i default -itsoffset 00:00:00 -f video4linux2 -s 1280x720 -r 25 -i /dev/video0 -t 00:00:01 <local-user-path>/Desktop/0_vib/"+video_dir+"/"+str(a)+".avi")


# def shit():
# 	global test
# 	while True:
# 		if len(test) > 2:
# 			print(test)
# 			print("*"*50)
# 			test = []

read_from_port(serial_port)
# thread = threading.Thread(target=read_from_port, args=(serial_port,))
# thread.start()

# shit()

# thread_shit = threading.Thread(target=shit)
# thread_shit.start()