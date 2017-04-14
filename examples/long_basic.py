import plexus
import time
from itertools import repeat
import random
import matplotlib.pyplot as plt

SIZE = 256
INPUT_SIZE = 4
OUTPUT_SIZE = 2
CONNECTIVITY = 0.5
PRECISION = 1

TRAINING_DURATION = 0.01
DOMINANCE_THRESHOLD = 0.7

RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = True

TRAINING_SAMPLE_SIZE = 80
TESTING_SAMPLE_SIZE = 20

def generate_list_bigger():
    generated_list = []
    for i in repeat(None, INPUT_SIZE):
        generated_list.append(round(random.uniform(0.6, 1.0), PRECISION))
    return generated_list

def generate_list_smaller():
    generated_list = []
    for i in repeat(None, INPUT_SIZE):
        generated_list.append(round(random.uniform(0.0, 0.4), PRECISION))
    return generated_list

errors = []
minutes = []
start = time.time()
print "\n___ PLEXUS NETWORK BASIC EXAMPLE ___\n"

print "Create a Plexus network with " + str(SIZE) + " neurons, " + str(INPUT_SIZE) + " of them sensory, " + str(OUTPUT_SIZE) + " of them motor, " + str(CONNECTIVITY) + " connectivity rate, " + str(PRECISION) + " digit precision"
net = plexus.Network(SIZE,INPUT_SIZE,OUTPUT_SIZE,CONNECTIVITY,PRECISION,RANDOMLY_FIRE,DYNAMIC_OUTPUT)

for j in repeat(None, 60):

    print "\n*** LEARNING ***"

    print "\nGenerate The Dataset (" + str(TRAINING_SAMPLE_SIZE) + " Items Long) To Classify The Numbers Bigger & Smaller Than 0.5 & Learn for " + str(TRAINING_DURATION) + " Seconds Each"
    for i in range(1,TRAINING_SAMPLE_SIZE):
        if (i % 2) == 0:
            generated_list = generate_list_bigger()
            print "Load Input: " + str(generated_list) + "\tOutput: [1.0, 0.0]\tand wait " + str(TRAINING_DURATION) + " seconds"
            net.load(generated_list, [1.0, 0.0])
        else:
            generated_list = generate_list_smaller()
            print "Load Input: " + str(generated_list) + "\tOutput: [0.0, 1.0]\tand wait " + str(TRAINING_DURATION) + " seconds"
            net.load(generated_list, [0.0, 1.0])
        time.sleep(TRAINING_DURATION)



    print "\n\n*** TESTING ***"

    print "\nTest the network with random data (" + str(TESTING_SAMPLE_SIZE) + " times)"
    error = 0
    error_divisor = 0
    for i in repeat(None, TESTING_SAMPLE_SIZE):
        binary_random = random.randint(0,1)
        if binary_random == 0:
            generated_list = generate_list_bigger()
            expected = [1.0, 0.0]
        else:
            generated_list = generate_list_smaller()
            expected = [0.0, 1.0]

        net.load(generated_list)
        time.sleep(0.1)

        output = net.output
        error += abs(expected[0] - output[0])
        error += abs(expected[1] - output[1])
        error_divisor += 2

        print "Load Input: " + str(generated_list) + "\tRESULT: " + str(output) + "\tExpected: " + str(expected)



    print "\n"

    #print ""
    #for neuron in net.neurons:
    #    print "A type " + str(neuron.type) + " neuron fired " + str(neuron.fire_counter) + " times"
    #print ""

    print "\n" + str(net.wave_counter) + " waves are executed throughout the network"

    print "\nIn total: " + str(net.fire_counter) + " times a random non-sensory neuron fired\n"

    error = error / error_divisor
    print "\nOverall error: " + str(error) + "\n\n"

    errors.append(error)
    minutes.append( (time.time() - start) / 60 )


net.freeze()

print "\nDraw the Graph"

print minutes
print errors

plt.plot(minutes, errors)
plt.ylabel('Overall error')
plt.xlabel('Elapsed time (in minutes)')
plt.show()

print "Exit the program"
