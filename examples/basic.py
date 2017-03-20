import plexus
import time
from itertools import repeat
import random

SIZE = 64
INPUT_SIZE = 4
OUTPUT_SIZE = 2
CONNECTIVITY = 0.5
PRECISION = 1

TRAINING_DURATION = 3
DOMINANCE_THRESHOLD = 0.5

RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = True

def generate_list_bigger():
    generated_list = []
    for i in repeat(None, 4):
        generated_list.append(round(random.uniform(0.6, 1.0), PRECISION))
    return generated_list

def generate_list_smaller():
    generated_list = []
    for i in repeat(None, 4):
        generated_list.append(round(random.uniform(0.0, 0.4), PRECISION))
    return generated_list


print "\n___ PLEXUS NETWORK BASIC EXAMPLE ___\n"

print "Create a Plexus network with " + str(SIZE) + " neurons, " + str(INPUT_SIZE) + " of them sensory, " + str(OUTPUT_SIZE) + " of them cognitive, " + str(CONNECTIVITY) + " connectivity rate, " + str(PRECISION) + " digit precision"
net = plexus.Network(SIZE,INPUT_SIZE,OUTPUT_SIZE,CONNECTIVITY,PRECISION,RANDOMLY_FIRE,DYNAMIC_OUTPUT)

print "\n*** LEARNING ***"

print "\nGenerate The Dataset (100 Items Long) To Classify The Numbers Bigger Than 0.5 & Learn for " + str(TRAINING_DURATION) + " Seconds Each"
for i in repeat(None, 100):
    generated_list = generate_list_bigger()
    print "Load Input: " + str(generated_list) + "\tOutput: [1.0, 0.0]\tand wait " + str(TRAINING_DURATION) + " seconds"
    net.load(generated_list, [1.0, 0.0])
    time.sleep(TRAINING_DURATION)

print "\nGenerate The Dataset (100 Items Long) To Classify The Numbers Smaller Than 0.5 & Learn for " + str(TRAINING_DURATION) + " Seconds Each"
for i in repeat(None, 100):
    generated_list = generate_list_smaller()
    print "Load Input: " + str(generated_list) + "\tOutput: [0.0, 1.0]\tand wait " + str(TRAINING_DURATION) + " seconds"
    net.load(generated_list, [0.0, 1.0])
    time.sleep(TRAINING_DURATION)

print "\n\n*** TESTING ***"

print "\nGenerate Test Data (100 Times) With The Numbers Bigger Than 0.5"
error1 = 0
error1_divisor = 0
for i in repeat(None, 100):
    generated_list = generate_list_bigger()
    net.load(generated_list)
    wave_zero = net.wave_counter
    while True:
        wave_current = net.wave_counter
        if wave_current > wave_zero:
            wave_zero = wave_current
            output = net.output
            if abs(output[1] - output[0]) > DOMINANCE_THRESHOLD:
                error1 += abs(1.0 - output[0])
                error1 += abs(0.0 - output[1])
                error1_divisor += 2
                break
        time.sleep(0.001)
    print "Load Input: " + str(generated_list) + "\tRESULT: " + str(output) + "\tExpected: [1.0, 0.0]"
error1 = error1 / error1_divisor

print "\nGenerate Test Data (100 Times) With The Numbers Smaller Than 0.5"
error2 = 0
error2_divisor = 0
for i in repeat(None, 100):
    generated_list = generate_list_smaller()
    net.load(generated_list)
    wave_zero = net.wave_counter
    while True:
        wave_current = net.wave_counter
        if wave_current > wave_zero:
            wave_zero = wave_current
            output = net.output
            if abs(output[1] - output[0]) > DOMINANCE_THRESHOLD:
                error2 += abs(0.0 - output[0])
                error2 += abs(1.0 - output[1])
                error2_divisor += 2
                break
        time.sleep(0.001)
    print "Load Input: " + str(generated_list) + "\tRESULT: " + str(output) + "\tExpected: [0.0, 1.0]"
error2 = error2 / error2_divisor

print "\n"
net.freeze()

#print ""
#for neuron in net.neurons:
#    print "A type " + str(neuron.type) + " neuron fired " + str(neuron.fire_counter) + " times"
#print ""

print "\n" + str(net.wave_counter) + " waves are executed throughout the network"

print "\nIn total: " + str(net.fire_counter) + " times a random non-sensory neuron fired\n"

error = (error1 + error2) / 2
print "\nOverall error: " + str(error) + "\n"

print "Exit the program"
