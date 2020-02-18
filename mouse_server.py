#######################################################################################
# Project: 
# 	Gyro Mouse
# Description: 
# 	a bluetooth server to receive data over bluetooth transmisson
# 	from arduino board, the arduino transmiting gyro values for two axis x and y.
# 	when data is received the server changes thu cursor position accordingly to the incoming values.
# Author: 
# 	Bar Polyak
#######################################################################################

import serial
import time
import win32api 
import win32con

class mouse_server:
	def __init__(self):
		self.port = self.port_check()
		self.bt = serial.Serial(self.port, 9600, timeout=0)
		self.gx = 0
		self.gy = 0
		self.sensitivity = 2
		print("[*] Server running")
		self.run()

	# Port Check Function
	def port_check(self):
		ports_list = ['COM%s' % (i + 1) for i in range(256)]
		result = {}
		print("[*] Starting COM Ports Check...")
		for port in ports_list:
			try:
				s = serial.Serial(port, 9600, timeout=0)
				s.close()
				result[len(result)+1] = port
			except (OSError, serial.SerialException):
				pass
		print("List of available COM Ports:")
		for p in result.keys():
			print("["+ str(p) +"] " + result[p])
		bt_port = int(input("Choose Gyro Mouse COM Port:"))
		return result[bt_port]
		
	# Right Click Function
	def right_click(self):
		x,y = win32api.GetCursorPos()
		win32api.SetCursorPos((x,y))
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
		time.sleep(0.05)
		win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

	# Left Click Function
	def left_click(self):
		x,y = win32api.GetCursorPos()
		win32api.SetCursorPos((x,y))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		time.sleep(0.05)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

	# Read Bluetooth Data Function
	def read_data(self):
		try:
			input_data = self.bt.readline().decode()
			return input_data
		except UnicodeDecodeError:
			pass

	# Move Mouse Function
	def moveMouse(self):
		print("gx: " + str(self.gx) + " gy: " + str(self.gy))
		# Get current cursor position
		current_pos = win32api.GetCursorPos()
		cx = current_pos[0] 
		cy = current_pos[1]
		# Calculate new cursor position
		mx = cx - ((self.gx -1) * self.sensitivity)
		my = cy + ((self.gy) * self.sensitivity)
		# Set new cursor position
		win32api.SetCursorPos((int(mx), int(my)))

	# Main Run Function
	def run(self):
		try:
			print("[*] Incoming Data...")
			self.bt.flushInput()
			while True:
				# Read bluetooth transmission
				line = self.read_data().rstrip()
				if "right" in line:
					# Right click check
					self.right_click()
				elif "left" in line:
					# Left click check
					self.left_click()
				else:
					# Values check
					line = line.split('|')
					if len(line) == 2:
						try:
							# Get gyro values
							self.gx = float(line[0])
							self.gy = float(line[1])
							# Move mouse
							self.moveMouse()
						except ValueError:
							continue
				
				time.sleep(0.01)
		except KeyboardInterrupt:
			self.bt.close()
			print("[*] End")

if __name__ == "__main__":
	# Initialize new mouse server at HC-05 bluetooth port COM4.
	gm = mouse_server()
    
