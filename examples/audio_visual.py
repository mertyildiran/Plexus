import time
from pathlib import Path
import cv2
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import cplexus as plexus

VIDEO_FILE = 'videos/lower3.mp4'

Path("videos/output/original").mkdir(parents=True, exist_ok=True)
Path("videos/output/training").mkdir(parents=True, exist_ok=True)
Path("videos/output/evaluation").mkdir(parents=True, exist_ok=True)

audio = AudioSegment.from_file(VIDEO_FILE, "mp4")
audio_samples = audio.get_array_of_samples()

print('Normalizing audio...')
max_hz = max(audio_samples)
min_hz = min(audio_samples)
#audio_samples = [x + (abs(min_hz)) for x in audio_samples]
#audio_samples = [x / (max_hz + abs(min_hz)) for x in audio_samples]
audio_samples = np.array(audio_samples)
audio_samples = audio_samples + (abs(min_hz))
audio_samples = np.true_divide(audio_samples, (max_hz + abs(min_hz)))

cap = cv2.VideoCapture(VIDEO_FILE)
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

buf = np.empty((frameHeight, frameWidth, 3), np.dtype('uint8'))

ret = True
chunk_size = int((1) / frameCount * len(audio_samples)) - int(0 / frameCount * len(audio_samples))

SIZE = chunk_size + frameWidth * frameHeight * 3 + 2048
INPUT_SIZE = chunk_size
OUTPUT_SIZE = frameWidth * frameHeight * 3
CONNECTIVITY = 16 / SIZE
PRECISION = 3

TRAINING_DURATION = 0.01
RANDOMLY_FIRE = False
DYNAMIC_OUTPUT = False
VISUALIZATION = False

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
for n in range(1):
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    print("Doing iteration {0}.".format(str(n + 1)))
    fc = 0
    while (fc < frameCount and ret):
        print(fc)
        (i, j) = ([fc * chunk_size, (fc + 1) * chunk_size])
        chunk = audio_samples[i:j]

        ret, buf = cap.read()
        buf_normalized = np.true_divide(buf, 255).flatten()

        # Load data into network
        net.load(chunk, buf_normalized)

        cv2.namedWindow('video')
        cv2.imshow('video', buf)

        output = net.output
        output = np.array(output) * 255
        learn = output.reshape((frameHeight, frameWidth, 3))
        learn = learn.astype(np.uint8)
        cv2.namedWindow('learn')
        cv2.imshow('learn', learn)

        cv2.imwrite("videos/output/original/{0}.png".format(str(fc)), buf)
        cv2.imwrite("videos/output/training/{0}.png".format(str(fc)), learn)

        cv2.waitKey(int(1000 * TRAINING_DURATION))
        fc += 1
    net.load(chunk)

#cap.release()

print("\n\n*** TESTING ***")

fc = 0

while (fc < frameCount):
    print(fc)
    (i, j) = ([fc * chunk_size, (fc + 1) * chunk_size])
    chunk = audio_samples[i:j]

    # Wait for the data to propagate and get the output
    net.load(chunk)
    output = net.output

    output = np.array(output) * 255
    buf = output.reshape((frameHeight, frameWidth, 3))
    buf = buf.astype(np.uint8)

    cv2.namedWindow('output')
    cv2.imshow('output', buf)

    cv2.imwrite("videos/output/evaluation/{0}.png".format(str(fc)), buf)

    cv2.waitKey(int(1000 * TRAINING_DURATION))
    fc += 1

net.freeze()

print("\n{0} waves are executed throughout the network".format(
    str(net.wave_counter)
))

print("\nIn total: {0} times a random non-sensory neuron is fired\n".format(
    str(net.fire_counter)
))

print("Exit the program")
