import plexus
import time
from itertools import repeat
import random

SIZE = 32 + 2 + 16
INPUT_SIZE = 32
OUTPUT_SIZE = 1
CONNECTIVITY = 0.5
PRECISION = 2

TRAINING_DURATION = 1
DOMINANCE_THRESHOLD = 0.7

RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = True
VISUALIZATION = False

TRAINING_SAMPLE_SIZE = 20
TESTING_SAMPLE_SIZE = 20

def is_prime(x):
    return x > 1 and all(x % i for i in xrange(2, x))

def generate_data():
    generated_input = []
    number = random.randint(1, INPUT_SIZE)
    for i in range(1, INPUT_SIZE+1):
        if i == number:
            generated_input.append(1.0)
        else:
            generated_input.append(0.0)
    generated_output = []
    if is_prime(number):
        generated_output = [1.0]
    else:
        generated_output = [0.0]
    return (generated_input, generated_output)


print "\n___ PLEXUS NETWORK PRIME NUMBER CLASSIFICATION EXAMPLE ___\n"

print "Create a Plexus network with " + str(SIZE) + " neurons, " + str(INPUT_SIZE) + " of them sensory, " + str(OUTPUT_SIZE) + " of them motor, " + str(CONNECTIVITY) + " connectivity rate, " + str(PRECISION) + " digit precision"
net = plexus.Network(SIZE,INPUT_SIZE,OUTPUT_SIZE,CONNECTIVITY,PRECISION,RANDOMLY_FIRE,DYNAMIC_OUTPUT,VISUALIZATION)

print "\n*** LEARNING ***"

print "\nGenerate The Dataset (" + str(TRAINING_SAMPLE_SIZE) + " Items Long) To Classify The Prime Numbers & Learn for " + str(TRAINING_DURATION) + " Seconds Each"
for i in range(1,TRAINING_SAMPLE_SIZE):
    data = generate_data()
    print "Load Input: " + str(data) + "\tand wait " + str(TRAINING_DURATION) + " seconds"
    net.load(data[0], data[1])
    time.sleep(TRAINING_DURATION)


print "\n\n*** TESTING ***"

print "\nTest the network with random data (" + str(TESTING_SAMPLE_SIZE) + " times)"
error = 0
error_divisor = 0
for i in repeat(None, TESTING_SAMPLE_SIZE):
    data = generate_data()
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
