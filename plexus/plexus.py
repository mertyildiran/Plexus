import random
import itertools
import time
import signal
from threading import Thread
from multiprocessing import Pool
import multiprocessing
import sys
import ctypes

POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html
AVERAGE_SYNAPSES_PER_NEURON = 8200 # The average number of synapses per neuron: 8,200 --- http://www.ncbi.nlm.nih.gov/pubmed/2778101

# https://en.wikipedia.org/wiki/Neuron

class Neuron():

	def __init__(self,network):
		self.subscriptions = {}
		self.value = 0.0
		self.error = 0.0
		#self.create_subscriptions()
		#self.create_axon_terminals()
		network.neurons.append(self)
		self.thread = Thread(target = self.activate)
		#self.thread.start()
		#self.process = multiprocessing.Process(target=self.activate)

	def fully_subscribe(self,network):
		for neuron in network.neurons[len(self.subscriptions):]:
			if id(neuron) != id(self):
				self.subscriptions[id(neuron)] = round(random.uniform(0.1, 1.0), 2)

	def partially_subscribe(self,network):
		if len(self.subscriptions) == 0:
			neuron_count = len(network.neurons)
			#for neuron in network.neurons:
			elected = random.sample(network.neurons,100)
			for neuron in elected:
				if id(neuron) != id(self):
					#if random.randint(1,neuron_count/100) == 1:
					self.subscriptions[id(neuron)] = round(random.uniform(0.1, 1.0), 2)
			network.n += 1
			#print "Neuron ID: " + str(id(self))
			#print "    Potential: " + str(self.potential)
			#print "    Error: " + str(self.error)
			#print "    Connections: " + str(len(self.subscriptions))

	def get_neuron(self,id):
		return ctypes.cast(id, ctypes.py_object).value

	def activate(self,network):
		while True:
			'''
			for dendritic_spine in self.subscriptions:
				if dendritic_spine.axon_terminal is not None:
					dendritic_spine.potential = dendritic_spine.axon_terminal.potential
					print dendritic_spine.potential
				self.neuron_potential += dendritic_spine.potential * dendritic_spine.excitement
			terminal_potential = self.neuron_potential / len(self.axon_terminals)
			for axon_terminal in self.axon_terminals:
				axon_terminal.potential = terminal_potential
			'''
			#if len(self.subscriptions) == 0:
			#	self.partially_subscribe()
			#else:
			self.partially_subscribe()
			pass

			'''
			if abs(len(network.neurons) - len(self.subscriptions) + 1) > 0:
				self.create_subscriptions()

			if abs(len(network.neurons) - len(self.axon_terminals) + 1) > 0:
				self.create_axon_terminals()
			'''

class Network():

	def __init__(self,size):
		self.neurons = []
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons created."
		self.n = 0
		self.initiate_subscriptions()
		#pool = Pool(4, self.init_worker)
		#pool.apply_async(self.initiate_subscriptions(), arguments)
		#map(lambda x: x.partially_subscribe(),network.neurons)
		#map(lambda x: x.create_subscriptions(),network.neurons)
		#map(lambda x: x.create_axon_terminals(),network.neurons)

	def initiate_subscriptions(self):
		for neuron in self.neurons:
			#neuron.thread.start()
			neuron.partially_subscribe(self)
			print "Counter: " + str(self.n) + "\r",
			sys.stdout.flush()
		print "\n"

	def add_neurons(self,size):
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons added."
		self.initiate_subscriptions()
