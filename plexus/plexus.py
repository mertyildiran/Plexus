import random
import sys
import math
import threading
import time

class Neuron():

	def __init__(self,network):
		self.network = network
		self.subscriptions = {}
		self.publications = {}
		self.potential = random.uniform(0.0, 1.0)
		self.desired_potential = None
		self.loss = None
		self.type = 0
		self.network.neurons.append(self)
		self.fire_counter = 0
		self.ban_counter = 0
		self.position = (None, None)
		self.index = None

	def partially_subscribe(self):
		if len(self.subscriptions) == 0:
			sample_length = int(random.normalvariate(self.network.connectivity, self.network.connectivity_sqrt))
			if sample_length > len(self.network.nonmotor_neurons):
				sample_length = len(self.network.nonmotor_neurons)
			if sample_length <= 0: sample_length = 0
			elected = random.sample(self.network.nonmotor_neurons, sample_length)
			for neuron in elected:
				if id(neuron) != id(self):
					self.subscriptions[neuron] = random.uniform(-1.0, 1.0)
					neuron.publications[self] = 0
			self.network.initiated_neurons += 1

	def calculate_potential(self):
		total = 0
		for neuron, weight in self.subscriptions.iteritems():
			total += neuron.potential * weight
		return self.activation_function(total)

	def activation_function(self,x):
		return 1 / (1 + math.exp(-x))

	def derivative(self,x):
		return x*(1-x)

	def calculate_loss(self):
		try:
			return self.potential - self.desired_potential
		except:
			return None

	def fire(self):
		if self.type != 1:

			self.potential = self.calculate_potential()
			self.network.fire_counter += 1
			self.fire_counter += 1

			if self.desired_potential != None:

				self.loss = self.calculate_loss()
				if self.loss > 0:
					alteration_sign = -1
				elif self.loss < 0:
					alteration_sign = 1
				else:
					self.desired_potential = None
					return True

				blame_value = (abs(self.loss) ** (1/2))
				alteration_value = (abs(self.loss) ** 2)
				alteration_value = alteration_value * (self.network.decay_factor ** (self.network.fire_counter/1000))


				for neuron, weight in self.subscriptions.iteritems():
					neuron.desired_potential = neuron.potential + (blame_value * alteration_sign) * self.derivative(neuron.potential)
					self.subscriptions[neuron] = weight + (alteration_value * alteration_sign) * self.derivative(neuron.potential)


class Network():

	def __init__(self,size,input_dim=0,output_dim=0,connectivity=0.01,precision=2,randomly_fire=False,dynamic_output=False,visualization=False):
		self.precision = precision
		print "\nPrecision of the network will be " + str( 1.0 / (10**precision) )
		self.connectivity = int(size * connectivity)
		self.connectivity_sqrt = int(math.sqrt(self.connectivity))
		print "Each individual non-sensory neuron will subscribe to " + str(int(size * connectivity)) + " different neurons"

		self.neurons = []
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons created"

		self.sensory_neurons = []
		self.input_dim = input_dim
		self.pick_sensory_neurons(self.input_dim)

		self.motor_neurons = []
		self.output_dim = output_dim
		self.pick_motor_neurons(self.output_dim)

		self.nonsensory_neurons = [x for x in self.neurons if x.type is not 1]
		self.nonmotor_neurons = [x for x in self.neurons if x.type is not 2]
		self.interneurons = [x for x in self.neurons if x.type is 0]
		self.randomly_fire = randomly_fire
		self.motor_randomly_fire_rate = int(math.sqrt( len(self.nonsensory_neurons)/len(self.motor_neurons) ))

		self.dynamic_output = dynamic_output

		self.decay_factor = 0.99

		self.initiated_neurons = 0
		self.initiate_subscriptions()

		self.fire_counter = 0
		self.first_queue = {}
		self.next_queue = {}
		self.output = []
		self.wave_counter = 0

		print "\n"

		self.freezer = False
		self.thread1 = None
		self.thread2 = None
		self.thread_kill_signal = False
		if visualization:
			self.visualize()
		self.ignite()

		print ""

	def initiate_subscriptions(self):
		print ""
		for neuron in self.neurons:
			if neuron.type == 1:
				continue
			neuron.partially_subscribe()
			print "Initiated: " + str(self.initiated_neurons) + " neurons\r",
			sys.stdout.flush()
		print "\n"

	def add_neurons(self,units):
		for i in range(units):
			Neuron(self)
		print "\n"
		print str(units) + " neurons added"
		self.initiate_subscriptions()

	def _ignite(self):
		#t0 = time.time()
		motor_fire_counter = 0
		ban_list = []
		while not self.freezer:
			if self.randomly_fire:
				neuron = random.sample(self.nonsensory_neurons,1)[0]
				if neuron.type == 2:
					if 1 != random.randint(1,self.motor_randomly_fire_rate):
						continue
					else:
						motor_fire_counter += 1
				neuron.fire()
				if motor_fire_counter >= len(self.motor_neurons):
					if self.dynamic_output:
						print "Output: " + str(self.get_output()) + "\r",
						sys.stdout.flush()
					self.output = self.get_output()
					self.wave_counter += 1
					motor_fire_counter = 0

			else:
				if not self.next_queue:
					#print "Delta time: " + str(time.time() - t0)
					#t0 = time.time()
					for neuron in self.motor_neurons:
						neuron.fire()
					for neuron in ban_list:
						neuron.ban_counter = 0
					ban_list = []
					if self.dynamic_output:
						print "Output: " + str(self.get_output()) + "\r",
						sys.stdout.flush()
					self.output = self.get_output()
					self.wave_counter += 1

					if not self.first_queue:
						for neuron in self.sensory_neurons:
							self.first_queue.update(neuron.publications)
					self.next_queue = self.first_queue.copy()

				current_queue = self.next_queue.copy()
				self.next_queue = {}
				for neuron in ban_list:
					if neuron.ban_counter > self.connectivity_sqrt:
						current_queue.pop(neuron, None)
				while current_queue:
					neuron = random.choice(current_queue.keys())
					current_queue.pop(neuron, None)
					if neuron.ban_counter <= self.connectivity_sqrt:
						if neuron.type == 2:
							continue
						neuron.fire()
						ban_list.append(neuron)
						neuron.ban_counter += 1
						self.next_queue.update(neuron.publications)

	def ignite(self):
		self.freezer = False
		if not self.thread1:
			self.thread1 = threading.Thread(target=self._ignite)
			self.thread1.start()
		print "Network has been ignited"

	def freeze(self):
		self.freezer = True
		self.thread1 = None
		self.thread2 = None
		self.thread_kill_signal = True
		print "Network is now frozen"

	def breakit(self):
		for neuron in self.neurons:
			neuron.subscriptions = {}
		print "All the subscriptions are now broken"

	def pick_sensory_neurons(self,input_dim):
		available_neurons = []
		for neuron in self.neurons:
			if neuron.type is 0:
				available_neurons.append(neuron)
		for neuron in random.sample(available_neurons,input_dim):
			neuron.type = 1
			self.sensory_neurons.append(neuron)
		print str(input_dim) + " neuron picked as sensory neuron"

	def pick_motor_neurons(self,output_dim):
		available_neurons = []
		for neuron in self.neurons:
			if neuron.type is 0:
				available_neurons.append(neuron)
		for neuron in random.sample(available_neurons,output_dim):
			neuron.type = 2
			self.motor_neurons.append(neuron)
		print str(output_dim) + " neuron picked as motor neuron"

	def load(self,input_arr,output_arr=None):
		if len(self.sensory_neurons) != len(input_arr):
			print "Size of the input array: " + str(len(input_arr))
			print "Number of the sensory neurons: " + str(len(self.sensory_neurons))
			print "Size of the input array and number of the sensory neurons are not matching! Please try again"
		else:
			step = 0
			for neuron in self.sensory_neurons:
				neuron.potential = input_arr[step]
				step += 1
		if output_arr is None:
			step = 0
			for neuron in self.motor_neurons:
				neuron.desired_potential = None
				step += 1
		else:
			if len(self.motor_neurons) != len(output_arr):
				print "Size of the output/target array: " + str(len(output_arr))
				print "Number of the motor_neurons: " + str(len(self.motor_neurons))
				print "Size of the output/target array and number of the motor neurons are not matching! Please try again"
			else:
				step = 0
				for neuron in self.motor_neurons:
					neuron.desired_potential = output_arr[step]
					step += 1

	def get_output(self):
		output = []
		for neuron in self.motor_neurons:
			output.append( round(neuron.potential, self.precision) )
		return output

	def visualize(self):
		self.thread2 = threading.Thread(target=self._visualize)
		self.thread2.start()
		print "Visualization initiated"

	def _visualize(self):
		import pyqtgraph as pg
		from pyqtgraph.Qt import QtCore, QtGui
		import numpy as np

		# Enable antialiasing for prettier plots
		pg.setConfigOptions(antialias=True)

		w = pg.GraphicsWindow()
		w.setWindowTitle('Visualization of the Network')
		v = w.addViewBox()
		v.setAspectLocked()

		g = pg.GraphItem()
		v.addItem(g)

		positions = []
		symbols = []
		symbol_brushes = []
		x = 0
		y = 0

		x += 1
		for neuron in self.sensory_neurons:
			y += 1
			neuron.position = (x, y)
			#plot.plot(x=[neuron.position[0]], y=[neuron.position[1]], pen=None, symbolBrush=(250,194,5), symbolPen='w', symbol='t1', symbolSize=14, name="sensory neuron")
			positions.append(neuron.position)
			symbols.append('t')
			symbol_brushes.append((250,194,5))
			neuron.index = len(positions) - 1

		x += 1
		y = 0
		for neuron in self.interneurons:
			neuron.position = (random.uniform(x, round(math.sqrt(len(self.interneurons)))+1), random.uniform(y+1, round(math.sqrt(len(self.interneurons)))+1))
			#plot.plot(x=[neuron.position[0]], y=[neuron.position[1]], pen=None, symbolBrush=(195,46,212), symbolPen='w', symbol='h', symbolSize=14, name="interneuron")
			positions.append(neuron.position)
			symbols.append('h')
			symbol_brushes.append((195,46,212))
			neuron.index = len(positions) - 1

		x = round(math.sqrt(len(self.interneurons)))+2
		y = 0
		for neuron in self.motor_neurons:
			y += 1
			neuron.position = (x, y)
			#plot.plot(x=[neuron.position[0]], y=[neuron.position[1]], pen=None, symbolBrush=(19,234,201), symbolPen='w', symbol='s', symbolSize=14, name="motor neuron")
			positions.append(neuron.position)
			symbols.append('s')
			symbol_brushes.append((19,234,201))
			neuron.index = len(positions) - 1


		while True:
			connections = []
			lines = []
			for neuron2 in self.neurons:
				for neuron1, weight in neuron2.subscriptions.iteritems():
					connections.append((neuron1.index, neuron2.index))
					lines.append((55,55,55,((weight+1)/2)*255,(weight+1)))


			positions = np.asarray(positions)
			connections = np.asarray(connections)
			lines = np.asarray(lines, dtype=[('red',np.ubyte),('green',np.ubyte),('blue',np.ubyte),('alpha',np.ubyte),('width',float)])
			g.setData(pos=positions, adj=connections, pen=lines, size=0.1, symbolBrush=symbol_brushes, symbol=symbols, pxMode=False) # Update the graph

			pg.QtGui.QApplication.processEvents()
			if self.thread_kill_signal:
				break
			time.sleep(0.01666)
