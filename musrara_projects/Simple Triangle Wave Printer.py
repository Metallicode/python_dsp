import time

wave_length = 14

x = 0
directionIsUp = True

while True:
	time.sleep(0.02)
	print("*"*(x+wave_length))

	if directionIsUp is True:
		x+=1
	else:
		x-=1

	if x > wave_length:
		directionIsUp = False
	elif x < -wave_length: 
		directionIsUp = True

