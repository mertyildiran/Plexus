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
import gc
from itertools import repeat

POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html
AVERAGE_SYNAPSES_PER_NEURON = 8200 # The average number of synapses per neuron: 8,200 --- http://www.ncbi.nlm.nih.gov/pubmed/2778101

# https://en.wikipedia.org/wiki/Neuron

class Neuron():

	def __init__(self,network):
		self.network = network
		self.subscriptions = {}
		self.potential = round(random.uniform(0.1, 1.0), self.network.precision)
		self.desired_potential = None
		self.fault = None
		self.instability = 0
		self.type = 0
		self.network.neurons.append(self)

	def fully_subscribe(self):
		for neuron in self.network.neurons[len(self.subscriptions):]:
			if id(neuron) != id(self):
				self.subscriptions[neuron] = round(random.uniform(0.1, 1.0), self.network.precision)

	def partially_subscribe(self):
		if len(self.subscriptions) == 0:
			#neuron_count = len(self.network.neurons)
			elected = random.sample(self.network.neurons, self.network.connectivity)
			for neuron in elected:
				if id(neuron) != id(self):
					self.subscriptions[neuron] = round(random.uniform(0.1, 1.0), self.network.precision)
			self.network.initiated_neurons += 1

	def get_neuron_by_id(self,neuron_id):
		#return ctypes.cast(neuron_id, ctypes.py_object)
		for neuron in self.network.neurons:
			if id(neuron) == neuron_id:
				return neuron
		raise Exception("No found")

	def calculate_potential(self):
		total = 0
		for neuron, weight in self.subscriptions.iteritems():
			total += neuron.potential * weight
		return round(self.activation_function(total), self.network.precision)

	def activation_function(self,value):
		return abs(math.sin(value**2))

	def fire(self):
		if self.type == 1:
			return False

		self.potential = self.calculate_potential()
		if self.desired_potential != None:
			self.fault = round(abs(self.desired_potential - self.potential), self.network.precision)

		improved_with_weight_update = 0
		potential_zero = self.potential
		subscriptions_zero = self.subscriptions
		fault_zero = self.fault

		if self.desired_potential != None and self.fault != None:
			for i in repeat(None, 8):
				for neuron, weight in self.subscriptions.iteritems():
					self.subscriptions[neuron] = round(random.uniform(0.1, 1.0), self.network.precision)
				self.potential = self.calculate_potential()
				self.fault = round(abs(self.desired_potential - self.potential), self.network.precision)
				if self.fault < fault_zero:
					improved_with_weight_update = 1
					break
			if not improved_with_weight_update:
				self.potential = potential_zero
				self.subscriptions = subscriptions_zero
				self.fault = fault_zero

		self.instability = random.randint(0,9)

class Network():

	def __init__(self,size,input_dim=0,output_dim=0,connectivity=0.01,precision=2):
		self.precision = precision
		print "\nPrecision of the network will be " + str( 1.0 / (10**precision) )
		self.connectivity = int(size * connectivity)
		print "Each individual neuron will subscribe to " + str(int(size * connectivity)) + " different neurons"

		self.neurons = []
		for i in range(size):
			Neuron(self)
		print "\n"
		print str(size) + " neurons created"

		self.initiated_neurons = 0
		self.initiate_subscriptions()

		self.sensory_neurons = []
		self.input_dim = input_dim
		self.pick_sensory_neurons(self.input_dim)

		self.cognitive_neurons = []
		self.output_dim = output_dim
		self.pick_cognitive_neurons(self.output_dim)

		print "\n"

		self.freezer = False
		self.thread = None
		self.ignite()

		print ""

	def initiate_subscriptions(self,only_new_ones=0):
		for neuron in self.neurons:
			if only_new_ones and len(neuron.subscriptions) != 0:
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
		self.initiate_subscriptions(1)

	def _ignite(self):
		while not self.freezer:
			random.sample(self.neurons,1)[0].fire()

	def ignite(self):
		self.freezer = False
		if not self.thread:
			self.thread = threading.Thread(target=self._ignite)
			self.thread.start()
		print "Network has been ignited"

	def freeze(self):
		self.freezer = True
		self.thread = None
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
			neuron.subscriptions = {}
			self.sensory_neurons.append(neuron)
		print str(input_dim) + " neuron picked as sensory neuron"

	def pick_cognitive_neurons(self,output_dim):
		available_neurons = []
		for neuron in self.neurons:
			if neuron.type is 0:
				available_neurons.append(neuron)
		for neuron in random.sample(available_neurons,output_dim):
			neuron.type = 2
			self.cognitive_neurons.append(neuron)
		print str(output_dim) + " neuron picked as cognitive neuron"

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
		if output_arr == None:
			step = 0
			for neuron in self.cognitive_neurons:
				neuron.desired_potential = None
				step += 1
		else:
			if len(self.cognitive_neurons) != len(output_arr):
				print "Size of the output/target array: " + str(len(output_arr))
				print "Number of the cognitive_neurons: " + str(len(self.cognitive_neurons))
				print "Size of the output/target array and number of the cognitive neurons are not matching! Please try again"
			else:
				step = 0
				for neuron in self.cognitive_neurons:
					neuron.desired_potential = output_arr[step]
					step += 1					
		print "Data was successfully loaded"
