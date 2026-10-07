#!<local-user-path>/miniconda3/envs/vib/bin/python
import os, serial, time, datetime, asyncio, serial_asyncio

detect_arr = []
# z = asyncio

class Reader(asyncio.Protocol):
	# global detect_arr
	# global z
	#self.buf = b''
	def connection_made(self, transport):
		"""Store the serial transport and prepare to receive data.
		"""
		self.transport = transport
		self.buf = bytes()
		# self.z = asyncio
		self.msgs_recvd = 0
		print('Reader connection created')

	def data_received(self, data):
		global detect_arr
		# global z
		"""Store characters until a newline is received.
		"""
		# self.buf = b''
		self.buf += data
		#print(self.buf)
		if b'\n' in self.buf:
			lines = self.buf.split(b'\n')
			self.buf = lines[-1]  # whatever was left over
			for line in lines[:-1]:
				#print(f'Reader received: {line.decode()}')
				#print(self.buf)
				detect_arr.append(line.decode())
				if "movement detected" in str(line.decode()).lower():
					# print(asyncio.Queue.get_nowait())
					
					#record()
					#print(f'Reader received: {line.decode()}')
					print(self.buf)
					print(self.buf)
					print(self.buf)
					self.buf = bytes()
					print(self.buf)
					print(self.buf)
					print(self.buf)
					print("*"*50)
					try:
						asyncio.Queue(0).get_nowait()
						asyncio.Queue(0).task_done()
					except:
						pass
					# detect_arr = []
					
					# self.buf = b''
					#del self.buf
					#print(a.readline())
				self.msgs_recvd += 1
			#if self.msgs_recvd == 4:
			#	self.transport.close()

	def connection_lost(self, exc):
		print('Reader closed')
 
video_dir = "video_export"
loop 	= asyncio.get_event_loop()
reader 	= serial_asyncio.create_serial_connection(loop, Reader, '/dev/ttyACM0', baudrate=9600)




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
	#a = open_serial()
	asyncio.ensure_future(reader)
	print('Ready')
	loop.run_forever()
	#while True:
		#try:
		
			#except:
			#	pass
	#except:
	#	time.sleep(2)
	#	init()

init()