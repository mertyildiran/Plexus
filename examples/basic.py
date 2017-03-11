import plexus
import time
from itertools import repeat
import random

def generate_list_bigger():
    generated_list = []
    for i in repeat(None, 4):
        generated_list.append(round(random.uniform(0.6, 1.0), 1))
    return generated_list

def generate_list_smaller():
    generated_list = []
    for i in repeat(None, 4):
        generated_list.append(round(random.uniform(0.0, 0.4), 1))
    return generated_list


print "PLEXUS NETWORK BASIC EXAMPLE"

print "Create a Plexus network with 22 neurons, 4 of them sensory, 2 of them cognitive, 22 connectivity per neuron, 0.1 precision"
net = plexus.Network(262,4,2,0.25,1)

print "\n*** LEARNING ***\n"

print "Generate The Dataset (10 Items Long) To Classify The Numbers Bigger Than 0.5 & Learn for 3 Seconds Each"
for i in repeat(None, 10):
    generated_list = generate_list_bigger()
    print "Load Input: " + str(generated_list) + " - Output: [1.0, 0.0] and wait 3 seconds"
    net.load(generated_list, [1.0, 0.0])
    time.sleep(3)

print "Generate The Dataset (10 Items Long) To Classify The Numbers Smaller Than 0.5 & Learn for 3 Seconds Each"
for i in repeat(None, 10):
    generated_list = generate_list_smaller()
    print "Load Input: " + str(generated_list) + " - Output: [0.0, 1.0] and wait 3 seconds"
    net.load(generated_list, [0.0, 1.0])
    time.sleep(3)

print "\n*** TESTING ***\n"

print "Generate Test Data (10 Items Long) With The Numbers Bigger Than 0.5 & Test The Network for a Second Each"
for i in repeat(None, 10):
    generated_list = generate_list_bigger()
    print "Load Input: " + str(generated_list) + ""
    net.load(generated_list)
    time.sleep(0.5)
    #print "Calculate The Avarage Output by Testing 10 Times Each 50 Milliseconds"
    output = [0,0]
    for i in repeat(None, 10):
        output[0] += net.cognitive_neurons[0].potential
        output[1] += net.cognitive_neurons[1].potential
        time.sleep(0.05)
    output[0] = round(output[0] / 10, 1)
    output[1] = round(output[1] / 10, 1)
    print "AVARAGE: " + str(output) + " - Expected: [1.0, 0.0]"


print "Generate Test Data (10 Items Long) With The Numbers Smaller Than 0.5 & Test The Network for a Second Each"
for i in repeat(None, 10):
    generated_list = generate_list_smaller()
    print "Load Input: " + str(generated_list) + ""
    net.load(generated_list)
    time.sleep(0.5)
    #print "Calculate The Avarage Output by Testing 10 Times Each 50 Milliseconds"
    output = [0,0]
    for i in repeat(None, 10):
        output[0] += net.cognitive_neurons[0].potential
        output[1] += net.cognitive_neurons[1].potential
        time.sleep(0.05)
    output[0] = round(output[0] / 10, 1)
    output[1] = round(output[1] / 10, 1)
    print "AVARAGE: " + str(output) + " - Expected: [0.0, 1.0]"

net.freeze()
print "Exit the program"
