import pickle
import numpy as np
import os
import cv2
import random
import plexus
from itertools import repeat

SIZE = 32 * 32 * 3 * 2
INPUT_SIZE = 32 * 32 * 3
OUTPUT_SIZE = 32 * 32 * 3
CONNECTIVITY = 0.0016
PRECISION = 3

TRAINING_DURATION = 3

TRAINING_SAMPLE_SIZE = 100
TESTING_SAMPLE_SIZE = 100

def load_batch(fpath, label_key='labels'):
    # Internal utility for parsing CIFAR data
    f = open(fpath, 'rb')
    d = pickle.load(f)
    f.close()
    data = d['data']
    labels = d[label_key]

    data = data.reshape(data.shape[0], 3, 32, 32)
    return data, labels


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

blue = np.full((32, 32, 3), [255, 0, 0])
red = np.full((32, 32, 3), [0, 0, 255])
blue_normalized = np.true_divide(blue, 255).flatten()
red_normalized = np.true_divide(red, 255).flatten()

print "Create a Plexus network with " + str(SIZE) + " neurons, " + str(INPUT_SIZE) + " of them sensory, " + str(OUTPUT_SIZE) + " of them cognitive, " + str(CONNECTIVITY) + " connectivity rate, " + str(PRECISION) + " digit precision"
net = plexus.Network(SIZE,INPUT_SIZE,OUTPUT_SIZE,CONNECTIVITY,PRECISION)
#net.freeze()

for cat in cats_sample:
    cat_normalized = np.true_divide(cat, 255).flatten()
    blue_normalized = np.true_divide(blue, 255).flatten()
    cv2.imshow("Input", cat)
    net.load(cat_normalized,blue_normalized)
    for i in repeat(None, 20 * TRAINING_DURATION):
        output = np.array(net.get_output()).reshape(32, 32, 3)
        output = np.multiply(output, 255)
        #print str(net.fire_counter)
        cv2.imshow("Output", output)
        cv2.waitKey(50)


#net.freeze()

cv2.imshow("Original Frame", blue)
key = cv2.waitKey(50)
cv2.imshow("Original Frame", red)
key = cv2.waitKey(1000)

print x_test[0].shape
