import plexus
import time
from itertools import repeat


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


def notify_the_load(generated_list, output, training_duration):
    print("Load Input: {0}\tOutput: {1}\tand wait {2} seconds".format(
        str(generated_list),
        str(output),
        str(training_duration)
    ))


print("\n___ PLEXUS NETWORK BASIC SEQUENCE RECOGNITION EXAMPLE ___\n")

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

print("\nGenerate The Dataset ({0} Items Long) To Recognize a Sequence & Learn\
for {1} Seconds Each".format(
    str(TRAINING_SAMPLE_SIZE),
    str(TRAINING_DURATION)
))

for i in range(1, TRAINING_SAMPLE_SIZE):
    dataset = generate_dataset()
    for data in dataset:
        notify_the_load(data[0], data[1], TRAINING_DURATION)
        net.load(data[0], data[1])
        time.sleep(TRAINING_DURATION)


print("\n\n*** TESTING ***")

print("\nTest the network with random data ({0} times)".format(
    str(TESTING_SAMPLE_SIZE)
))
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

        print("Load Input: " + str(data) + "\tRESULT: " + str(output[0]))


print("\n")
net.freeze()


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
