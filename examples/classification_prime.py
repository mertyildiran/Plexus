import argparse
import time
from itertools import repeat
import random


ap = argparse.ArgumentParser()

ap.add_argument('difficulty', metavar='difficulty', type=int,
                help='Difficulty level of the problem. Can be 1, 2, 3, 4')
ap.add_argument('-l', '--language', type=str,
                help='Implementation language of Plexus. Can be "cpp" or "py"')
args = vars(ap.parse_args())

if args['language'] == 'cpp':
    import cplexus as plexus
else:
    import plexus

if args['difficulty'] == 1:
    SIZE = 32 + 1 + 16
    INPUT_SIZE = 32
    TRAINING_DURATION = 1
    CONNECTIVITY = 0.5
elif args['difficulty'] == 2:
    SIZE = 256 + 1 + 32
    INPUT_SIZE = 256
    TRAINING_DURATION = 1
    CONNECTIVITY = 0.5
elif args['difficulty'] == 3:
    SIZE = 512 + 1 + 32
    INPUT_SIZE = 512
    TRAINING_DURATION = 2
    CONNECTIVITY = 0.5
elif args['difficulty'] == 4:
    SIZE = 1024 + 1 + 64
    INPUT_SIZE = 1024
    TRAINING_DURATION = 3
    CONNECTIVITY = 0.25
else:
    print('Difficulty level should not exceed 4. \
The value of you supplied was: {0}'.format(args['difficulty']))
    exit(0)


OUTPUT_SIZE = 1
PRECISION = 2

DOMINANCE_THRESHOLD = 0.7

RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = True
VISUALIZATION = False

TRAINING_SAMPLE_SIZE = 20
TESTING_SAMPLE_SIZE = 20


def is_prime(x):
    return x > 1 and all(x % i for i in range(2, x))


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


def notify_the_load(generated_list, output, training_duration):
    print("Load Input: {0}\tOutput: {1}\tand wait {2} seconds".format(
        str(generated_list),
        str(output),
        str(training_duration)
    ))


print("\n___ PLEXUS NETWORK PRIME NUMBER CLASSIFICATION EXAMPLE ___\n")

print("Create a Plexus network with {0} neurons, {1} of them sensory, {2} of \
them motor, {3} connectivity rate, {4} digit precision".format(
    str(SIZE),
    str(INPUT_SIZE),
    str(OUTPUT_SIZE),
    str(CONNECTIVITY),
    str(PRECISION),
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

print("\nGenerate The Dataset ({0} Items Long) To Classify The Prime Numbers & \
Learn for {1} Seconds Each".format(
    str(TRAINING_SAMPLE_SIZE),
    str(TRAINING_DURATION)
))

for i in range(1, TRAINING_SAMPLE_SIZE):
    data = generate_data()
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
    data = generate_data()
    net.load(data[0], data[1])
    time.sleep(TRAINING_DURATION*2)

    output = net.output
    error += abs(data[1][0] - output[0])
    error_divisor += 1

    notify_the_load(data, output[0], TRAINING_DURATION)


print("\n")
net.freeze()


print("\n{0} waves are executed throughout the network".format(
    str(net.wave_counter)
))

print("\nIn total: {0} times a random non-sensory neuron is fired\n".format(
    str(net.fire_counter)
))

error = error / error_divisor
print("\nOverall error: {0}\n".format(
    str(error)
))

print("Exit the program")
