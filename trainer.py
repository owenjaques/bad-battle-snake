#calls the game engine with the snake every 10 seconds

import subprocess as sp
import json
import time
import winsound

for i in range(500):
	print("Trial #", i)
	try:
		cmdCommand = "../engine/engine.exe create -c snake-config.json"
		process = sp.Popen(cmdCommand.split(), stdout=sp.PIPE)
		output, error = process.communicate()

		l = json.loads(output)

		s = l['ID']

		sp.run(['../engine/engine', 'run', '-g', s])

		time.sleep(8)
	except Exception as e:
		print(e)
		duration = 1000  # milliseconds
		freq = 440  # Hz
		winsound.Beep(freq, duration)

