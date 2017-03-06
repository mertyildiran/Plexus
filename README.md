<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/full.gif" alt="Plexus"/>
</p>

## Core Principles

These are the core principles of **exceptionally bio-inspired**, a revolutionary approach to the artificial neural networks:

 - **Neurons** must be **objects** not tensors between matrices.
 - Each neuron should have **its own thread**.
 - **Network** must be **architecture-free** (adaptive).
 - Network must have a **layerless design**.
 - There must be two types of neurons: **sensory neurons** and **interneurons**.
 - Input of network must be made of sensory neurons. Any neuron can be picked as an element of output.
 - There can be arbitrary amount of I/O groups in a single network.
 - Forget about batch size, iteration, and epoch concepts, training examples must be fed on time basis; *e.g. learn first sample for ten seconds, OK done? then learn second sample for twenty seconds*. By this approach, you can assign importance factors to your samples with maximum flexibility.
 - **Network** must be **retrainable**.
 - Network must be **modular**. In other words: You must be able to train a small network and then plug that network into a bigger network (I'm talking about some kind of **self-fusing** here).
 - Neurons must exhibit characteristics of **cellular automata**.
 - **Number of neurons** in network can be increased or decreased (**scalability**).
 - There must be **no** need for a network-wide **oscillation**.

### Activation function

<p align="left">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/activation-small.png" alt="Activation function"/>
</p>

### Installation

```Shell
sudo pip install plexus
```

### Usage Tips

Install Plexus with:

```Shell
pip install -e .
```

Create a new network:

```python
>>> import plexus
>>> net = plexus.Network(20000)


20000 neurons created.
Initiated: 20000

```

Network will automatically ignite itself when it is created. To freeze the network, call:

```python
net.freeze()
```

To reignite the network, call:

```python
net.ignite()
```

#### Basics

Each neuron will be referenced inside `net.neurons` array. Try to use `len` built-in function of Python to see how many neurons does your network have:

```python
>>> len(net.neurons)
20000
```

Try to use `id` built-in function of Python to get the id of the first neuron in your network:

```python
>>> id(net.neurons[0])
140432596060928
```

Now please freeze the network for a moment and take a look at the subscriptions of this first neuron:

```python
>>> net.neurons[0].subscriptions
{140432576391936: 0.37, 140432576768336: 0.53, 140432577685336: 0.12, 140432574942744: 0.48, 140432575327264: 0.96, 140432576273584: 0.61, 140432574976440: 0.62, 140432580006976: 0.97, 140432572508208: 0.15, 140432575822088: 0.81, 140432572736504: 0.36, 140432578098744: 0.15, 140432586556480: 0.21, 140432595873304: 0.42, 140432570339408: 0.12, 140432574261944: 0.36, 140432578023576: 0.6, 140432569275168: 0.21, 140432572436064: 0.12, 140432580310800: 0.17, 140432570534512: 0.18, 140432572361328: 0.23, 140432569274736: 0.31, 140432574105216: 0.39, 140432579888264: 0.16, 140432580154000: 0.31, 140432570451224: 0.42, 140432577989088: 0.58, 140432575398040: 0.22, 140432595982096: 0.78, 140432571187568: 0.82, 140432578749504: 0.76, 140432577612976: 0.32, 140432570681032: 0.92, 140432569699000: 0.43, 140432569917592: 0.9, 140432573270208: 0.88, 140432577338400: 0.74, 140432578631368: 0.7, 140432575665360: 0.24, 140432575024592: 0.66, 140432574488728: 0.21, 140432579162336: 0.35, 140432579392720: 0.48, 140432577380720: 0.96, 140432586378992: 0.38, 140432572894456: 0.57, 140432595909232: 0.79, 140432574792336: 0.85, 140432575857944: 0.87, 140432595725056: 0.11, 140432574492544: 0.27, 140432577071008: 0.36, 140432574904584: 0.89, 140432575592208: 0.43, 140432572433688: 0.78, 140432572737296: 0.59, 140432577188640: 0.8, 140432574676360: 0.91, 140432576730176: 0.34, 140432579247424: 0.67, 140432574984416: 0.12, 140432569965384: 0.56, 140432576848096: 0.79, 140432578677072: 0.52, 140432586483256: 0.74, 140432576503248: 0.46, 140432578520560: 0.36, 140432570414936: 0.38, 140432571565408: 0.51, 140432579162768: 0.16, 140432578675560: 0.13, 140432574528184: 0.14, 140432572662128: 0.95, 140432576582000: 0.5, 140432574976656: 0.8, 140432573767552: 0.2, 140432586630208: 0.53, 140432580726152: 0.38, 140432574032280: 0.41, 140432571832728: 0.91, 140432572966816: 0.78, 140432569618160: 0.36, 140432574563752: 0.64, 140432596242800: 0.26, 140432572208120: 0.94, 140432569688504: 0.52, 140432573536160: 0.88, 140432578715592: 0.21, 140432577261792: 0.25, 140432571870672: 0.28, 140432581108728: 0.99, 140432578292048: 0.3, 140432569809376: 0.37, 140432576802896: 0.33, 140432572627640: 0.5, 140432576538096: 0.57, 140432572618152: 0.78, 140432570453960: 0.49, 140432579281912: 0.19}
```

The above output tells us how the neuron gets its feed. Each individual key-value pair stores id of the subscribed neuron as the key and the weight of that subscription as the value. Learning process in a Plexus network is nothing more than updating those weights and/or adding neurons to this list or dropping neurons from the list.

Each individual neuron holds two floating point number called **potential** and **instability**. To get those values:

```python
>>> net.neurons[0].potential
0.91
>>> net.neurons[0].instability
0.45
```

Value of **potential** may only be updated by the **fire()** function of the same neuron and its being calculated by this simple formula each time when the neuron is fired (each time when the **fire()** function called):

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/calc_of_potential.gif" alt="Calculation of potential"/>
</p>

<!-- LaTeX of above image: Total = ( potential_{0} \times weight_{0} )\ +\ ( p_{1} \times w_{1} )\ +\ ( p_{2} \times w_{2} )\ +\ ...\ +\ ( p_{N} \times w_{N} ) \\ \center Potential = \left | sin(T^{2}) \right | -->

Value of **instability** may only be updated by the neurons which have been subscribed to the subject neuron with a similar manner with classical backward propagation of errors. But in Plexus networks the error is called **fault**. I'll explain the calculation of **fault** later in this article. Just like the updating of **potential**, the update of **instability** happens in the **fire()** function (when the neuron is fired). But as I said it updates the subscriptions not the same neuron, like this:

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/calc_of_instability.gif" alt="Calculation of instability"/>
</p>

<!-- LaTeX of above image: \center neuron_{0}instability_{1} = neuron_{0}instability_{0} \ \pm \ fault \\ \center neuron_{1}instability_{1} = neuron_{1}instability_{0} \ \pm \ fault \\ \center neuron_{2}instability_{1} = neuron_{2}instability_{0} \ \pm \ fault \\ \center \ \vdots -->

#### Sensory and Cognitive Neurons

Input Layer in classical neural networks renamed as **Sensory Neurons** in Plexus networks and Target/Ouput Layer renamed as **Cognitive Neurons**. This naming convention is necessary cause the built of the relevance of artificial neural networks with biological neural networks and Neuroscience.

The difference of sensory neurons from the interneurons (or I will just call it the other neurons that neither sensory nor cognitive ones) is, they do not fire. They just stand still for your **potential** assignments. As you can guess they do not have any subscriptions to other neurons (0 subscriptions). But they can be subscribed by the other neurons, including cognitive ones. They do not learn, they do not consume any CPU resource. They just stored in the memory. You can assign an image, a frame of a video, or a chunk of an audio to a group of sensory neurons. For example you can prepare the network for the assignment of a 64x64 RGB image like that:

```python
>>> net.pick_sensory_neurons(12288)
>>> len(net.sensory_neurons)
12288
>>> net.sensory_neurons[0]
<plexus.plexus.Neuron instance at 0x7f103d3473f8>
>>> net.sensory_neurons[0].subscriptions
{}
```

The difference of cognitive neurons form the other neurons is, they are only responsible to the network. They act as the source of the learning and calculation of the fault. The network dictates a desired potential on cognitive neuron. The cognitive neuron calculates its potential, compares it with desired potential, calculates fault then backpropagates it through the subscriptions. This is why they hold an additional potential variable called **desired_potential**. You can define the number of cognitive neurons similarly by using `net.pick_cognitive_neurons(number)` function.

As you can imagine, a neuron in a Plexus network holds an integer object variable called **type** to determine its type.

- `neuron.type = 1` means it's a sensory neuron.
- `neuron.type = 2` means it's a cognitive neuron.
- `neuron.type = 0` means it's neither a sensory nor a cognitive neuron. It means it's an interneuron.

#### Destroying The Network

Lastly, don't forget to call garbage collector when you want to stop and delete the network:

```python
>>> net.freeze()
>>> del net
>>> import gc
>>> gc.collect()
340000
```
