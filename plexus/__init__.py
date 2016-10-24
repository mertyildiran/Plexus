import random
import itertools
import time
import signal
from threading import Thread
from multiprocessing import Pool
import multiprocessing
import sys

POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html
AVERAGE_SYNAPSES_PER_NEURON = 8200 # The average number of synapses per neuron: 8,200 --- http://www.ncbi.nlm.nih.gov/pubmed/2778101

# https://en.wikipedia.org/wiki/Neuron

class Neuron():

	def __init__(self,network):
		self.connections = {}
		self.potential = 0.0
		self.error = 0.0
		#self.create_connections()
		#self.create_axon_terminals()
		network.neurons.append(self)
		self.thread = Thread(target = self.activate)
		#self.thread.start()
		#self.process = multiprocessing.Process(target=self.activate)

	def fully_connect(self,network):
		for neuron in network.neurons[len(self.connections):]:
			if id(neuron) != id(self):
				self.connections[id(neuron)] = round(random.uniform(0.1, 1.0), 2)

	def partially_connect(self,network):
		if len(self.connections) == 0:
			neuron_count = len(network.neurons)
			#for neuron in network.neurons:
			elected = random.sample(network.neurons,100)
			for neuron in elected:
				if id(neuron) != id(self):
					#if random.randint(1,neuron_count/100) == 1:
					self.connections[id(neuron)] = round(random.uniform(0.1, 1.0), 2)
			network.n += 1
			#print "Neuron ID: " + str(id(self))
			#print "    Potential: " + str(self.potential)
			#print "    Error: " + str(self.error)
			#print "    Connections: " + str(len(self.connections))

	def activate(self,network):
		while True:
			'''
			for dendritic_spine in self.connections:
				if dendritic_spine.axon_terminal is not None:
					dendritic_spine.potential = dendritic_spine.axon_terminal.potential
					print dendritic_spine.potential
				self.neuron_potential += dendritic_spine.potential * dendritic_spine.excitement
			terminal_potential = self.neuron_potential / len(self.axon_terminals)
			for axon_terminal in self.axon_terminals:
				axon_terminal.potential = terminal_potential
			'''
			#if len(self.connections) == 0:
			#	self.partially_connect()
			#else:
			self.partially_connect()
			pass

			'''
			if abs(len(network.neurons) - len(self.connections) + 1) > 0:
				self.create_connections()

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
		self.build_connections()
		#pool = Pool(4, self.init_worker)
		#pool.apply_async(self.build_connections(), arguments)
		#map(lambda x: x.partially_connect(),network.neurons)
		#map(lambda x: x.create_connections(),network.neurons)
		#map(lambda x: x.create_axon_terminals(),network.neurons)

	def build_connections(self):
		for neuron in self.neurons:
			#neuron.thread.start()
			neuron.partially_connect(self)
			print "Counter: " + str(self.n) + "\r",
			sys.stdout.flush()
		print "\n"

	def add_neurons(self,size):
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons added."
		self.build_connections()
