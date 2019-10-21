#calls the game engine with the snake every 10 seconds

import subprocess as sp
import json
import time

for i in range(500):
	print("Trial #", i)
	cmdCommand = "../engine/engine.exe create -c snake-config.json"
	process = sp.Popen(cmdCommand.split(), stdout=sp.PIPE)
	output, error = process.communicate()

	l = json.loads(output)

	s = l['ID']

	sp.run(['../engine/engine', 'run', '-g', s])

	time.sleep(5)

