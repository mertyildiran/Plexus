import plexus
import time
from itertools import repeat

print "PLEXUS NETWORK BASIC EXAMPLE"

print "*** Create a Plexus network with 22 neurons, 4 of them sensory, 2 of them cognitive, 22 connectivity per neuron, 0.1 precision ***"
net = plexus.Network(22,4,2,1,1)

print "*** Load Input: [0.6, 0.7, 0.8, 0.9] - Output: [1.0, 0.0] and wait 5 seconds ***"
net.load([0.6, 0.7, 0.8, 0.9], [1.0, 0.0])
time.sleep(5)

print "*** Load Input: Input: [0.4, 0.3, 0.2, 0.1] - Output: [0.0, 1.0] and wait 5 seconds ***"
net.load([0.4, 0.3, 0.2, 0.1], [0.0, 1.0])
time.sleep(5)

print "*** Load Input: [0.6, 0.7, 0.8, 0.9] ***"
net.load([0.6, 0.7, 0.8, 0.9])
time.sleep(0.5)
print "*** Print potential of first cognitive neuron 10 times ***"
for i in repeat(None, 10):
    print net.cognitive_neurons[0].potential


print "*** Load Input: Input: [0.4, 0.3, 0.2, 0.1] ***"
net.load([0.4, 0.3, 0.2, 0.1])
time.sleep(0.5)
print "*** Print potential of first cognitive neuron 10 times ***"
for i in repeat(None, 10):
    print net.cognitive_neurons[0].potential

net.freeze()
print "*** Exit the program ***"
