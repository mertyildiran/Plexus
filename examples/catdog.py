import pickle
import numpy as np
import os
import cv2
import random
import plexus
from itertools import repeat
import sys
import time

SIZE = 32 * 32 * 3 + 3
INPUT_SIZE = 32 * 32 * 3
OUTPUT_SIZE = 3
CONNECTIVITY = 0.01
PRECISION = 3

TRAINING_DURATION = 3
RANDOMLY_FIRE = True

TRAINING_SAMPLE_SIZE = 10
TESTING_SAMPLE_SIZE = 10

def load_batch(fpath, label_key='labels'):
    # Internal utility for parsing CIFAR data
    f = open(fpath, 'rb')
    d = pickle.load(f)
    f.close()
    data = d['data']
    labels = d[label_key]

    data = data.reshape(data.shape[0], 3, 32, 32)
    return data, labels

def show_output(net):
    for i in repeat(None, 10 * TRAINING_DURATION):
        output = net.get_output()
        output = [round(x*255) for x in output]
        print "Red: " + str(output[2]) + "\t" + "Green: " + str(output[1]) + "\t" + "Blue: " + str(output[0]) + "\r",
        sys.stdout.flush()
        output = np.full((32, 32, 3), output, dtype='uint8')
        cv2.imshow("Output", output)
        cv2.waitKey(100)


print "\n___ PLEXUS NETWORK CATDOG EXAMPLE ___\n"

print "Load CIFAR-10 dataset"
print "Pick random " + str(TRAINING_SAMPLE_SIZE) + " cat and " + str(TRAINING_SAMPLE_SIZE) + " dog images from the CIFAR-10 data batch to TRAIN the network"
print "Pick random " + str(TESTING_SAMPLE_SIZE) + " cat and " + str(TESTING_SAMPLE_SIZE) + " dog images from the CIFAR-10 test batch to TEST the network"

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

cats_sample = random.sample(cats, TRAINING_SAMPLE_SIZE)
dogs_sample = random.sample(dogs, TRAINING_SAMPLE_SIZE)

# Generate the testing data
test_cats = []
for i in range(0, num_train_samples/5 - 1):
    if y_test[i] == 3:
        test_cats.append(x_test[i])

test_dogs = []
for i in range(0, num_train_samples/5 - 1):
    if y_test[i] == 5:
        test_dogs.append(x_test[i])

test_cats_sample = random.sample(test_cats, TESTING_SAMPLE_SIZE)
test_dogs_sample = random.sample(test_dogs, TESTING_SAMPLE_SIZE)

blue = np.array([255, 0, 0])
red = np.array([0, 0, 255])
blue_normalized = np.true_divide(blue, 255)
red_normalized = np.true_divide(red, 255)

print "Create a Plexus network with " + str(SIZE) + " neurons, " + str(INPUT_SIZE) + " of them sensory, " + str(OUTPUT_SIZE) + " of them cognitive, " + str(CONNECTIVITY) + " connectivity rate, " + str(PRECISION) + " digit precision"
net = plexus.Network(SIZE,INPUT_SIZE,OUTPUT_SIZE,CONNECTIVITY,PRECISION,RANDOMLY_FIRE)

print "\n*** LEARNING ***"

print "\nMap " + str(TRAINING_SAMPLE_SIZE) + " Different Cat Images to Color Blue - Training Duration: " + str(TRAINING_DURATION * TRAINING_SAMPLE_SIZE) + " seconds"
for cat in cats_sample:
    cat_normalized = np.true_divide(cat, 255).flatten()
    blue_normalized = np.true_divide(blue, 255).flatten()
    cv2.imshow("Input", cat)
    net.load(cat_normalized,blue_normalized)
    show_output(net)

print "\nMap " + str(TRAINING_SAMPLE_SIZE) + " Different Dog Images to Color Red - Training Duration: " + str(TRAINING_DURATION * TRAINING_SAMPLE_SIZE) + " seconds"
for dog in dogs_sample:
    dog_normalized = np.true_divide(dog, 255).flatten()
    red_normalized = np.true_divide(red, 255).flatten()
    cv2.imshow("Input", dog)
    net.load(dog_normalized,red_normalized)
    show_output(net)

print "\nTest " + str(TESTING_SAMPLE_SIZE) + " Different Cat Images - Testing Duration: " + str(TRAINING_DURATION * TESTING_SAMPLE_SIZE) + " seconds"
for cat in test_cats_sample:
    cat_normalized = np.true_divide(cat, 255).flatten()
    cv2.imshow("Input", cat)
    net.load(cat_normalized)
    show_output(net)

print "\nTest " + str(TESTING_SAMPLE_SIZE) + " Different Dog Images - Testing Duration: " + str(TRAINING_DURATION * TESTING_SAMPLE_SIZE) + " seconds"
for dog in test_dogs_sample:
    dog_normalized = np.true_divide(dog, 255).flatten()
    cv2.imshow("Input", dog)
    net.load(dog_normalized)
    show_output(net)


net.freeze()
cv2.destroyAllWindows()

print "\nIn total: " + str(net.fire_counter) + " times a random non-sensory neuron fired\n"
print "Exit the program"
