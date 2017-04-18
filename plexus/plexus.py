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
		self.blame_lock = None
		self.ban_counter = 0

	def partially_subscribe(self):
		if len(self.subscriptions) == 0:
			sample_length = int(random.normalvariate(self.network.connectivity, self.network.connectivity_sqrt))
			if sample_length > len(self.network.nonmotor_neurons):
				sample_length = len(self.network.nonmotor_neurons)
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

	def activation_function(self,value):
		return 1 / (1 + math.exp(-value))

	def calculate_loss(self):
		try:
			return self.desired_potential - self.potential
		except:
			return None

	def fire(self):
		if self.type != 1:

			self.potential = self.calculate_potential()
			self.network.fire_counter += 1
			self.fire_counter += 1

			if self.desired_potential != None:

				if self.blame_lock:
					if (self.network.wave_counter - self.blame_lock) < self.network.connectivity:
						return True
					else:
						self.blame_lock = None

				self.loss = self.calculate_loss()
				if self.loss > 0:
					alteration_sign = 1
				elif self.loss < 0:
					alteration_sign = -1
				else:
					self.desired_potential = None
					return True

				alteration_value = (self.loss ** 2) / (len(self.subscriptions) + 1)

				for neuron, weight in self.subscriptions.iteritems():
					neuron.desired_potential = neuron.potential + (alteration_value * alteration_sign)
					self.subscriptions[neuron] = weight + (alteration_value * alteration_sign)
					self.blame_lock = self.network.wave_counter


class Network():

	def __init__(self,size,input_dim=0,output_dim=0,connectivity=0.01,precision=2,randomly_fire=False,dynamic_output=False):
		self.precision = precision
		print "\nPrecision of the network will be " + str( 1.0 / (10**precision) )
		self.connectivity = int(size * connectivity)
		self.connectivity_sqrt = int(math.sqrt(self.connectivity))
		self.connectivity_sqrt_sqrt = int(math.sqrt(self.connectivity_sqrt))
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

		self.nonsensory_neurons = [x for x in self.neurons if x not in self.sensory_neurons]
		self.nonmotor_neurons = [x for x in self.neurons if x not in self.motor_neurons]
		self.randomly_fire = randomly_fire
		self.motor_randomly_fire_rate = int(math.sqrt( len(self.nonsensory_neurons)/len(self.motor_neurons) ))

		self.reasoning_length = int(math.sqrt(self.input_dim))
		self.mini_batch = []

		self.dynamic_output = dynamic_output

		self.initiated_neurons = 0
		self.initiate_subscriptions()

		self.fire_counter = 0
		self.first_queue = {}
		self.next_queue = {}
		self.output = []
		self.wave_counter = 0

		print "\n"

		self.freezer = False
		self.thread = None
		self.ignite()

		print ""

	def initiate_subscriptions(self,only_new_ones=0):
		print ""
		for neuron in self.neurons:
			if neuron.type == 1:
				continue
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

					if self.mini_batch:
						[input_arr, output_arr] = random.sample(self.mini_batch,1)[0]
						step = 0
						for neuron in self.sensory_neurons:
							neuron.potential = input_arr[step]
							step += 1
						step = 0
						for neuron in self.motor_neurons:
							neuron.desired_potential = output_arr[step]
							step += 1
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

					if self.mini_batch:
						[input_arr, output_arr] = random.sample(self.mini_batch,1)[0]
						step = 0
						for neuron in self.sensory_neurons:
							neuron.potential = input_arr[step]
							step += 1
						step = 0
						for neuron in self.motor_neurons:
							neuron.desired_potential = output_arr[step]
							step += 1

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
			self.mini_batch = []
			step = 0
			for neuron in self.neurons:
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
				self.mini_batch.append([input_arr,output_arr])
				if len(self.mini_batch) > self.reasoning_length:
					self.mini_batch.pop(0)

	def get_output(self):
		output = []
		for neuron in self.motor_neurons:
			output.append( round(neuron.potential, self.precision) )
		return output
