import random
import itertools
import time
import signal
from multiprocessing import Pool
import multiprocessing
import sys
import ctypes
import math
import threading

POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html
AVERAGE_SYNAPSES_PER_NEURON = 8200 # The average number of synapses per neuron: 8,200 --- http://www.ncbi.nlm.nih.gov/pubmed/2778101

# https://en.wikipedia.org/wiki/Neuron

class Neuron():

	def __init__(self,network):
		self.subscriptions = {}
		self.value = round(random.uniform(0.1, 1.0), 2)
		self.instability = 0.0
		self.type = 0
		network.neurons.append(self)

	def fully_subscribe(self,network):
		for neuron in network.neurons[len(self.subscriptions):]:
			if id(neuron) != id(self):
				self.subscriptions[id(neuron)] = round(random.uniform(0.1, 1.0), 2)

	def partially_subscribe(self,network):
		if len(self.subscriptions) == 0:
			#neuron_count = len(network.neurons)
			elected = random.sample(network.neurons,100)
			for neuron in elected:
				if id(neuron) != id(self):
					self.subscriptions[id(neuron)] = round(random.uniform(0.1, 1.0), 2)
			network.initiated_neurons += 1

	def get_neuron(self,id):
		return ctypes.cast(id, ctypes.py_object).value

	def primitive_calculate(self):
		grand_total = 0
		for neuron_id in self.subscriptions:
			grand_total += self.get_neuron(neuron_id).value * (1 / self.subscriptions[neuron_id])
		print grand_total
		print self.activation_function(grand_total)

	def activation_function(self,value):
		return abs(math.sin(value**2))

	def fire(self):
		self.instability = round(random.uniform(0.1, 1.0), 2)

class Network():

	def __init__(self,size,input_dim=0,output_dim=0):
		self.neurons = []
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons created."
		self.initiated_neurons = 0
		self.initiate_subscriptions()

		self.sensory_neurons = []
		self.input_dim = input_dim
		self.pick_sensory_neurons(self.input_dim)

		self.ultimate_neurons = []
		self.output_dim = output_dim
		self.pick_ultimate_neurons(self.output_dim)

		self.freezer = False
		self.thread = None
		self.ignite()

	def initiate_subscriptions(self,only_new_ones=0):
		for neuron in self.neurons:
			if only_new_ones and len(neuron.subscriptions) != 0:
				continue
			neuron.partially_subscribe(self)
			print "Initiated: " + str(self.initiated_neurons) + "\r",
			sys.stdout.flush()
		print "\n"

	def add_neurons(self,size):
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons added."
		self.initiate_subscriptions(1)

	def _ignite(self):
		while not self.freezer:
			random.sample(self.neurons,1)[0].fire()

	def ignite(self):
		self.freezer = False
		if not self.thread:
			self.thread = threading.Thread(target=self._ignite)
			self.thread.start()

	def freeze(self):
		self.freezer = True
		self.thread = None

	def pick_sensory_neurons(self,input_dim):
		available_neurons = []
		for neuron in self.neurons:
			if neuron.type is not 1:
				available_neurons.append(neuron)
		for neuron in random.sample(available_neurons,input_dim):
			neuron.type = 1
			neuron.subscriptions = {}
			self.sensory_neurons.append(neuron)

	def pick_ultimate_neurons(self,output_dim):
		available_neurons = []
		for neuron in self.neurons:
			if neuron.type is not 2:
				available_neurons.append(neuron)
		for neuron in random.sample(available_neurons,output_dim):
			neuron.type = 2
			self.ultimate_neurons.append(neuron)
