import argparse
import time
from itertools import repeat
import random


ap = argparse.ArgumentParser()

ap.add_argument('difficulty', metavar='difficulty', type=int,
                help='Difficulty level of the problem. Can be 1, 2, 3, 4 or 5')
ap.add_argument('-l', '--language', type=str,
                help='Implementation language of Plexus. Can be "cpp" or "py"')
args = vars(ap.parse_args())

if args['language'] == 'cpp':
    import cplexus as plexus
else:
    import plexus

if args['difficulty'] == 1:
    SIZE = 14
    INPUT_SIZE = 4
    OUTPUT_SIZE = 2
    CONNECTIVITY = 1
    VISUALIZATION = True
    TRAINING_DURATION = 1
elif args['difficulty'] == 2:
    SIZE = 32 + 2 + 16
    INPUT_SIZE = 32
    OUTPUT_SIZE = 2
    CONNECTIVITY = 0.5
    VISUALIZATION = True
    TRAINING_DURATION = 1
elif args['difficulty'] == 3:
    SIZE = 256 + 2 + 32
    INPUT_SIZE = 256
    OUTPUT_SIZE = 2
    CONNECTIVITY = 0.5
    VISUALIZATION = True
    TRAINING_DURATION = 1
elif args['difficulty'] == 3:
    SIZE = 512 + 2 + 32
    INPUT_SIZE = 512
    OUTPUT_SIZE = 2
    CONNECTIVITY = 0.5
    VISUALIZATION = False
    TRAINING_DURATION = 2
elif args['difficulty'] == 5:
    SIZE = 1024 + 2 + 64
    INPUT_SIZE = 1024
    OUTPUT_SIZE = 2
    CONNECTIVITY = 0.25
    VISUALIZATION = False
    TRAINING_DURATION = 3


PRECISION = 2
DOMINANCE_THRESHOLD = 0.7
RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = True
TRAINING_SAMPLE_SIZE = 20
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


def notify_the_load(generated_list, output, training_duration):
    print("Load Input: {0}\tOutput: {1}\tand wait {2} seconds".format(
        str(generated_list),
        str(output),
        str(training_duration)
    ))


print("\n___ PLEXUS NETWORK BASIC EXAMPLE ___\n")

print("Create a Plexus network with {0} neurons, {1} of them sensory, {2} of\
them motor, {3} connectivity rate, {4} digit precision".format(
    str(SIZE),
    str(INPUT_SIZE),
    str(OUTPUT_SIZE),
    str(CONNECTIVITY),
    str(PRECISION)
))

net = plexus.Network(
    SIZE,
    INPUT_SIZE,
    OUTPUT_SIZE,
    CONNECTIVITY,
    PRECISION,
    RANDOMLY_FIRE,
    DYNAMIC_OUTPUT,
    VISUALIZATION
)

print("\n*** LEARNING ***")

print("\nGenerate The Dataset ({0} Items Long) To Classify The Numbers Bigger\
& Smaller Than 0.5 & Learn for {1} Seconds Each".format(
    str(TRAINING_SAMPLE_SIZE),
    str(TRAINING_DURATION)
))

for i in range(1, TRAINING_SAMPLE_SIZE):
    if (i % 2) == 0:
        output = [1.0, 0.0]
        generated_list = generate_list_bigger()
        notify_the_load(generated_list, output, TRAINING_DURATION)
        net.load(generated_list, output)
    else:
        output = [0.0, 1.0]
        generated_list = generate_list_smaller()
        notify_the_load(generated_list, output, TRAINING_DURATION)
        net.load(generated_list, output)
    time.sleep(TRAINING_DURATION)


print("\n\n*** TESTING ***")

print("\nTest the network with random data ({0} times)".format(
    str(TESTING_SAMPLE_SIZE)
))
error = 0
error_divisor = 0
for i in repeat(None, TESTING_SAMPLE_SIZE):
    binary_random = random.randint(0, 1)
    if binary_random == 0:
        generated_list = generate_list_bigger()
        expected = [1.0, 0.0]
    else:
        generated_list = generate_list_smaller()
        expected = [0.0, 1.0]

    net.load(generated_list)
    time.sleep(TRAINING_DURATION)

    output = net.output
    error += abs(expected[0] - output[0])
    error += abs(expected[1] - output[1])
    error_divisor += 2

    print("Load Input: {0}\tRESULT: {1}\tExpected: {2}".format(
        str(generated_list),
        str(output),
        str(expected)
    ))


print("\n")
net.freeze()

print("")
for neuron in net.neurons:
    print("A type {0} neuron fired {1} times".format(
        str(neuron.type),
        str(neuron.fire_counter)
    ))
print("")

print("\n{0} waves are executed throughout the network".format(
    str(net.wave_counter)
))

print("\nIn total: {0} times a random non-sensory neuron fired\n".format(
    str(net.fire_counter)
))

error = error / error_divisor
print("\nOverall error: {0}\n".format(
    str(error)
))

print("Exit the program")
