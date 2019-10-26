"""
creating this module in response to what I believe was logical error
by having my snakes each save to 'weights.h5' after each game and or 
generation it was only saving the weights of the last snake causing
the model to overfit to just that snake. the goal is now to have each
snake work on the same model. well see how it goes...
"""

from keras import Sequential
from keras.layers import InputLayer, Dense, Flatten

class Model:
	def __init__(self):
		self.model = Sequential()
		self.model.add(InputLayer(input_shape=(13,13,4), batch_size=1))
		self.model.add(Dense(32, activation='relu'))
		self.model.add(Dense(32, activation='relu'))
		self.model.add(Dense(32, activation='relu'))
		self.model.add(Flatten())
		self.model.add(Dense(4, activation='softmax'))
		self.model.compile(loss='mse', optimizer='adam')
		#loads weights comment out if you want new **WILL DELETE OLD WEIGHTS**
		try:
			self.model.load_weights('weights.h5')
			print("Loaded weights from weights.h5")
		except Exception as e:
			print(e)

	def saveModel(self):
		try:
			self.model.save_weights('weights.h5')
			print("Model Saved to weights.h5")
		except Exception as e:
			print(e)