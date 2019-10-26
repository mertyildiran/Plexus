import random
import threading
import time


def visualize(self):
    thread2 = threading.Thread(target=_visualize, args=(self,))
    thread2.start()
    print("Visualization initiated")


def _visualize(self):
    import pyqtgraph as pg
    import numpy as np

    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)

    w = pg.GraphicsWindow()
    w.setWindowTitle('Visualization of the Network')
    v = w.addViewBox()
    v.setAspectLocked()

    g = pg.GraphItem()
    v.addItem(g)

    positions = []
    symbols = []
    symbol_brushes = []
    x = 0
    y = 0

    x += 1
    for neuron in self.sensory_neurons:
        y += 1
        neuron.position = (float(x), float(y))
        positions.append(neuron.position)
        symbols.append('t')
        symbol_brushes.append((250, 194, 5))
        neuron.index = len(positions) - 1

    x += len(self.sensory_neurons)
    y = (len(self.sensory_neurons) - len(self.interneurons)) / 2
    for neuron in self.interneurons:
        y += 1
        neuron.position = (
            random.uniform(
                x - len(self.sensory_neurons)/1.5,
                x + len(self.sensory_neurons)/1.5
            ),
            float(y)
        )
        positions.append(neuron.position)
        symbols.append('h')
        symbol_brushes.append((195, 46, 212))
        neuron.index = len(positions) - 1

    x += len(self.sensory_neurons)
    y = (len(self.sensory_neurons) - len(self.motor_neurons)) / 2
    for neuron in self.motor_neurons:
        y += 1
        neuron.position = (float(x), float(y))
        positions.append(neuron.position)
        symbols.append('s')
        symbol_brushes.append((19, 234, 201))
        neuron.index = len(positions) - 1

    while True:
        connections = []
        lines = []
        for neuron2 in self.neurons:
            for neuron1, weight in neuron2.subscriptions.items():
                connections.append((neuron1.index, neuron2.index))
                lines.append((55, 55, 55, ((weight+1)/2)*255, (weight+1)))

        positions = np.asarray(positions)
        connections = np.asarray(connections)
        lines = np.asarray(lines, dtype=[
            ('red', np.ubyte),
            ('green', np.ubyte),
            ('blue', np.ubyte),
            ('alpha', np.ubyte),
            ('width', float)
        ])
        g.setData(
            pos=positions,
            adj=connections,
            pen=lines,
            size=0.1,
            symbolBrush=symbol_brushes,
            symbol=symbols,
            pxMode=False
        )  # Update the graph

        pg.QtGui.QApplication.processEvents()
        if self.thread_kill_signal:
            break
        time.sleep(0.0333)
