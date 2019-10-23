#calls the game engine with the snake every 10 seconds
#one long beep indicates it is done one short beep indicates an exception

import subprocess as sp
import json
import time
import winsound

for i in range(1000):
	print("Trial #", i)
	try:
		cmdCommand = "../engine/engine.exe create -c snake-config.json"
		process = sp.Popen(cmdCommand.split(), stdout=sp.PIPE)
		output, error = process.communicate()

		l = json.loads(output)

		s = l['ID']

		sp.run(['../engine/engine', 'run', '-g', s])

		time.sleep(6)
	except Exception as e:
		print(e)
		duration = 1000  # milliseconds
		freq = 440  # Hz
		winsound.Beep(freq, duration)

#indicates it is done
duration = 10000  # milliseconds
freq = 200  # Hz
winsound.Beep(freq, duration)

