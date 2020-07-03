import pickle
import numpy as np
import os
import cv2
import random
import cplexus as plexus
# import sys
import time
import tarfile
from tqdm import tqdm
import requests


basepath = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(basepath + '/cifar-10-python.tar.gz'):
    url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(basepath + '/cifar-10-python.tar.gz', 'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR, something went wrong")
        exit(1)

if not os.path.exists(basepath + '/cifar-10-batches-py/'):
    tar = tarfile.open(basepath + '/cifar-10-python.tar.gz', "r:gz")
    tar.extractall(basepath)
    tar.close()


SIZE = 32 * 32 * 3 + 3 + 256
INPUT_SIZE = 32 * 32 * 3
OUTPUT_SIZE = 3
CONNECTIVITY = 0.005
PRECISION = 3

TRAINING_DURATION = 3
RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = False
VISUALIZATION = False

TRAINING_SAMPLE_SIZE = 20
TESTING_SAMPLE_SIZE = 20

DOMINANCE_THRESHOLD = 0.7
error = 0
error_divisor = 0


def load_batch(fpath, label_key='labels'):
    # Internal utility for parsing CIFAR data
    f = open(fpath, 'rb')
    d = pickle.load(f, encoding='latin1')
    f.close()
    data = d['data']
    labels = d[label_key]

    data = data.reshape(data.shape[0], 3, 32, 32)
    return data, labels


def show_output(net, testing=False):
    global error
    global error_divisor

    if testing:
        time.sleep(TRAINING_DURATION/2)
        output = net.output
        output_init = output  # Only different line
        output = [round(x*255) for x in output]
        # print("Red: {0}\tGreen: {1}\tBlue: {2}\r".format(
        #     str(output[2]),
        #     str(output[1]),
        #     str(output[0])
        # ))
        # sys.stdout.flush()
        output = np.full((32, 32, 3), output, dtype='uint8')
        cv2.imshow("Output", output)
        cv2.waitKey(int(1000 * TRAINING_DURATION / 2))

        error += abs(testing[2] - output_init[2])
        error += abs(testing[0] - output_init[0])
        error_divisor += 2
    else:
        time.sleep(TRAINING_DURATION/2)
        output = net.output
        output = [round(x*255) for x in output]
        # print("Red: {0}\tGreen: {1}\tBlue: {2}\r".format(
        #     str(output[2]),
        #     str(output[1]),
        #     str(output[0])
        # ))
        # sys.stdout.flush()
        output = np.full((32, 32, 3), output, dtype='uint8')
        cv2.imshow("Output", output)
        cv2.waitKey(int(1000 * TRAINING_DURATION / 2))


print("\n___ PLEXUS NETWORK CATDOG EXAMPLE ___\n")

print("Load CIFAR-10 dataset")
print("Pick random {0} cat and {0} dog images from the CIFAR-10 data batch to \
TRAIN the network".format(
    str(TRAINING_SAMPLE_SIZE)
))
print("Pick random {0} cat and {0} dog images from the CIFAR-10 test batch to\
TEST the network".format(
    str(TESTING_SAMPLE_SIZE)
))

# Load CIFAR-10 dataset
path = './examples/cifar-10-batches-py/'
num_train_samples = 50000

x_train = np.zeros((num_train_samples, 3, 32, 32), dtype='uint8')
y_train = np.zeros((num_train_samples,), dtype='uint8')

for i in range(1, 6):
    fpath = os.path.join(path, 'data_batch_' + str(i))
    data, labels = load_batch(fpath)
    x_train[(i - 1) * 10000: i * 10000, :, :, :] = data
    y_train[(i - 1) * 10000: i * 10000] = labels

fpath = os.path.join(path, 'test_batch')
x_test, y_test = load_batch(fpath)

y_train = np.reshape(y_train, (len(y_train), 1))
y_test = np.reshape(y_test, (len(y_test), 1))

# channels last
x_train = x_train.transpose(0, 2, 3, 1)
x_test = x_test.transpose(0, 2, 3, 1)

# Generate the training data
cats = []
for i in range(0, num_train_samples - 1):
    if y_train[i] == 3:
        cats.append(x_train[i])

dogs = []
for i in range(0, num_train_samples - 1):
    if y_train[i] == 5:
        dogs.append(x_train[i])


# Generate the testing data
test_cats = []
for i in range(0, int(num_train_samples/5 - 1)):
    if y_test[i] == 3:
        test_cats.append(x_test[i])

test_dogs = []
for i in range(0, int(num_train_samples/5 - 1)):
    if y_test[i] == 5:
        test_dogs.append(x_test[i])


blue = np.array([255, 0, 0])
red = np.array([0, 0, 255])
blue_normalized = np.true_divide(blue, 255)
red_normalized = np.true_divide(red, 255)

print("Create a Plexus network with {0} neurons, {1} of them sensory, {2} of \
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

print("\nMap {0} Different Cat Images to Color Blue & {0} Different Dog Images \
to Color Red - Training Duration: {1} seconds (OpenCV latency not \
included)".format(
    str(TRAINING_SAMPLE_SIZE/2),
    str(TRAINING_DURATION * TRAINING_SAMPLE_SIZE)
))

for i in range(1, TRAINING_SAMPLE_SIZE):
    if (i % 2) == 0:
        cat = random.sample(cats, 1)[0]
        cat_normalized = np.true_divide(cat, 255).flatten()
        blue_normalized = np.true_divide(blue, 255).flatten()
        cv2.imshow("Input", cat)
        net.load(cat_normalized, blue_normalized)
    else:
        dog = random.sample(dogs, 1)[0]
        dog_normalized = np.true_divide(dog, 255).flatten()
        red_normalized = np.true_divide(red, 255).flatten()
        cv2.imshow("Input", dog)
        net.load(dog_normalized, red_normalized)
    show_output(net)


print("\nTest {0} Different Cat Images & {0} Different Dog Images \
- Testing Duration: {1} seconds (OpenCV latency not included)".format(
    str(TRAINING_SAMPLE_SIZE/2),
    str(TRAINING_DURATION * TESTING_SAMPLE_SIZE)
))

for i in range(1, TESTING_SAMPLE_SIZE):
    binary_random = random.randint(0, 1)
    if binary_random == 0:
        cat = random.sample(test_cats, 1)[0]
        cat_normalized = np.true_divide(cat, 255).flatten()
        cv2.imshow("Input", cat)
        net.load(cat_normalized)
        show_output(net, [1.0, 0.0, 0.0])
    else:
        dog = random.sample(test_dogs, 1)[0]
        dog_normalized = np.true_divide(dog, 255).flatten()
        cv2.imshow("Input", dog)
        net.load(dog_normalized)
        show_output(net, [0.0, 0.0, 1.0])


net.freeze()
cv2.destroyAllWindows()

print("\n{0} waves are executed throughout the network".format(
    str(net.wave_counter)
))

print("\nIn total: {0} times a random non-sensory neuron is fired\n".format(
    str(net.fire_counter)
))

print("\nOverall error: {0}\n".format(
    str(error/error_divisor)
))

print("Exit the program")
