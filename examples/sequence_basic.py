import plexus
import time
from itertools import repeat
import random

SIZE = 14
INPUT_SIZE = 4
OUTPUT_SIZE = 1
CONNECTIVITY = 1
PRECISION = 2

TRAINING_DURATION = 0.1
DOMINANCE_THRESHOLD = 0.7

RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = True
VISUALIZATION = True

TRAINING_SAMPLE_SIZE = 20
TESTING_SAMPLE_SIZE = 20

def shift(seq):
    return seq[-1:] + seq[:-1]

def generate_dataset():
    generated_dataset = []
    sequence = [0.0] * INPUT_SIZE
    sequence[-1] = 1.0
    for i in range(1, (INPUT_SIZE*2)+1):
        sequence = shift(sequence)
        if i == (INPUT_SIZE*2):
            output = [1.0]
        else:
            output = [0.0]
        generated_dataset.append((sequence, output))
    return generated_dataset



print "\n___ PLEXUS NETWORK BASIC SEQUENCE RECOGNITION EXAMPLE ___\n"

print "Create a Plexus network with " + str(SIZE) + " neurons, " + str(INPUT_SIZE) + " of them sensory, " + str(OUTPUT_SIZE) + " of them motor, " + str(CONNECTIVITY) + " connectivity rate, " + str(PRECISION) + " digit precision"
net = plexus.Network(SIZE,INPUT_SIZE,OUTPUT_SIZE,CONNECTIVITY,PRECISION,RANDOMLY_FIRE,DYNAMIC_OUTPUT,VISUALIZATION)

print "\n*** LEARNING ***"

print "\nGenerate The Dataset (" + str(TRAINING_SAMPLE_SIZE) + " Items Long) To Recognize a Sequence & Learn for " + str(TRAINING_DURATION) + " Seconds Each"
for i in range(1,TRAINING_SAMPLE_SIZE):
    dataset = generate_dataset()
    for data in dataset:
        print "Load Input: " + str(data) + "\tand wait " + str(TRAINING_DURATION) + " seconds"
        net.load(data[0], data[1])
        time.sleep(TRAINING_DURATION)


print "\n\n*** TESTING ***"

print "\nTest the network with random data (" + str(TESTING_SAMPLE_SIZE) + " times)"
error = 0
error_divisor = 0
for i in repeat(None, TESTING_SAMPLE_SIZE):
    dataset = generate_dataset()
    for data in dataset:
        net.load(data[0], data[1])
        time.sleep(TRAINING_DURATION*2)

        output = net.output
        error += abs(data[1][0] - output[0])
        error_divisor += 1

        print "Load Input: " + str(data) + "\tRESULT: " + str(output[0])


print "\n"
net.freeze()


print "\n" + str(net.wave_counter) + " waves are executed throughout the network"

print "\nIn total: " + str(net.fire_counter) + " times a random non-sensory neuron fired\n"

error = error / error_divisor
print "\nOverall error: " + str(error) + "\n"

print "Exit the program"
