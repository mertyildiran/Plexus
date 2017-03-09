<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/full.gif" alt="Plexus"/>
</p>

## Core Principles

These are the core principles of **exceptionally bio-inspired**, a revolutionary approach to the artificial neural networks:

 - **Neurons** must be **objects** not tensors between matrices.
 - Each neuron should have **its own thread**.
 - **Network** must be **architecture-free** (adaptive).
 - Network must have a **layerless design**.
 - There must be three types of neurons: **sensory neurons**, **interneurons** and **cognitive neurons**.
 - Input of network must be made of sensory neurons. Any neuron can be picked as an element of output or input.
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

```Shell
>>> import plexus
>>> net = plexus.Network(10000)


10000 neurons created.
Initiated: 10000

```

Network will automatically ignite itself when it is created. To freeze the network, call:

```Shell
>>> net.freeze()
Network is now frozen.
```

To reignite the network, call:

```Shell
>>> net.ignite()
Network has been ignited.
```

#### Basics

Each neuron will be referenced inside `net.neurons` array. Try to use `len` built-in function of Python to see how many neurons does your network have:

```Shell
>>> len(net.neurons)
10000
```

Now please freeze the network for a moment and take a look at the subscriptions of this first neuron:

```Shell
>>> net.neurons[0].subscriptions
{<plexus.plexus.Neuron instance at 0x7f27fa600050>: 0.94, <plexus.plexus.Neuron instance at 0x7f27fa8de098>: 0.96, <plexus.plexus.Neuron instance at 0x7f27fafea0e0>: 0.89, <plexus.plexus.Neuron instance at 0x7f27fa76c1b8>: 0.81, <plexus.plexus.Neuron instance at 0x7f27fac5a2d8>: 0.13, <plexus.plexus.Neuron instance at 0x7f27faf54248>: 0.3, <plexus.plexus.Neuron instance at 0x7f27fad3a290>: 0.54, <plexus.plexus.Neuron instance at 0x7f27fa6242d8>: 0.87, <plexus.plexus.Neuron instance at 0x7f27fad14320>: 0.47, <plexus.plexus.Neuron instance at 0x7f27fa6fc7a0>: 0.39, <plexus.plexus.Neuron instance at 0x7f27fa722098>: 0.51, <plexus.plexus.Neuron instance at 0x7f27fa9a1b48>: 0.58, <plexus.plexus.Neuron instance at 0x7f27fad845f0>: 0.54, <plexus.plexus.Neuron instance at 0x7f27faa663f8>: 0.53, <plexus.plexus.Neuron instance at 0x7f27faf130e0>: 0.77, <plexus.plexus.Neuron instance at 0x7f27fadaa440>: 0.75, <plexus.plexus.Neuron instance at 0x7f27fac92488>: 0.46, <plexus.plexus.Neuron instance at 0x7f27fae6d638>: 0.19, <plexus.plexus.Neuron instance at 0x7f27fa8820e0>: 0.23, <plexus.plexus.Neuron instance at 0x7f27fa505bd8>: 0.84, <plexus.plexus.Neuron instance at 0x7f27fa8005a8>: 0.87, <plexus.plexus.Neuron instance at 0x7f27fb0585f0>: 0.29, <plexus.plexus.Neuron instance at 0x7f27fab32638>: 0.47, <plexus.plexus.Neuron instance at 0x7f27faac2680>: 0.28, <plexus.plexus.Neuron instance at 0x7f27fad4c6c8>: 0.54, <plexus.plexus.Neuron instance at 0x7f27fa933128>: 0.63, <plexus.plexus.Neuron instance at 0x7f27fab8ebd8>: 0.24, <plexus.plexus.Neuron instance at 0x7f27fa558758>: 0.54, <plexus.plexus.Neuron instance at 0x7f27fa9be7a0>: 0.57, <plexus.plexus.Neuron instance at 0x7f27fadc56c8>: 0.81, <plexus.plexus.Neuron instance at 0x7f27faeae8c0>: 0.99, <plexus.plexus.Neuron instance at 0x7f27fa5a2908>: 0.93, <plexus.plexus.Neuron instance at 0x7f27fababc68>: 0.91, <plexus.plexus.Neuron instance at 0x7f27fa6fc998>: 0.96, <plexus.plexus.Neuron instance at 0x7f27faee69e0>: 0.89, <plexus.plexus.Neuron instance at 0x7f27fac511b8>: 0.66, <plexus.plexus.Neuron instance at 0x7f27fad1dc68>: 0.52, <plexus.plexus.Neuron instance at 0x7f27fa517710>: 0.28, <plexus.plexus.Neuron instance at 0x7f27fb06cbd8>: 0.99, <plexus.plexus.Neuron instance at 0x7f27fa904c68>: 0.83, <plexus.plexus.Neuron instance at 0x7f27fae88cb0>: 0.7, <plexus.plexus.Neuron instance at 0x7f27fab1e320>: 0.72, <plexus.plexus.Neuron instance at 0x7f27fa600d88>: 0.68, <plexus.plexus.Neuron instance at 0x7f27fac9b248>: 0.39, <plexus.plexus.Neuron instance at 0x7f27fb0c8dd0>: 0.23, <plexus.plexus.Neuron instance at 0x7f27fab0ce60>: 0.31, <plexus.plexus.Neuron instance at 0x7f27fa668ef0>: 0.31, <plexus.plexus.Neuron instance at 0x7f27fac80f38>: 0.38, <plexus.plexus.Neuron instance at 0x7f27fadc57e8>: 0.64, <plexus.plexus.Neuron instance at 0x7f27faf1cf80>: 0.26, <plexus.plexus.Neuron instance at 0x7f27fa88b6c8>: 0.46, <plexus.plexus.Neuron instance at 0x7f27fa5050e0>: 0.2, <plexus.plexus.Neuron instance at 0x7f27faa372d8>: 0.61, <plexus.plexus.Neuron instance at 0x7f27fa599128>: 0.68, <plexus.plexus.Neuron instance at 0x7f27faf13830>: 0.34, <plexus.plexus.Neuron instance at 0x7f27fa6df1b8>: 0.2, <plexus.plexus.Neuron instance at 0x7f27fa517200>: 0.17, <plexus.plexus.Neuron instance at 0x7f27fa82f248>: 0.25, <plexus.plexus.Neuron instance at 0x7f27fa6cd2d8>: 0.67, <plexus.plexus.Neuron instance at 0x7f27fac24dd0>: 0.49, <plexus.plexus.Neuron instance at 0x7f27fab3b3b0>: 0.67, <plexus.plexus.Neuron instance at 0x7f27facd33f8>: 0.75, <plexus.plexus.Neuron instance at 0x7f27fa90dbd8>: 0.51, <plexus.plexus.Neuron instance at 0x7f27faa37440>: 0.65, <plexus.plexus.Neuron instance at 0x7f27fafa9488>: 0.98, <plexus.plexus.Neuron instance at 0x7f27fb0c88c0>: 0.83, <plexus.plexus.Neuron instance at 0x7f27fb527518>: 0.76, <plexus.plexus.Neuron instance at 0x7f27fa683560>: 0.35, <plexus.plexus.Neuron instance at 0x7f27fae7f5a8>: 0.62, <plexus.plexus.Neuron instance at 0x7f27fa695638>: 0.83, <plexus.plexus.Neuron instance at 0x7f27faff3680>: 0.62, <plexus.plexus.Neuron instance at 0x7f27fa90d6c8>: 0.47, <plexus.plexus.Neuron instance at 0x7f27fab4d710>: 0.82, <plexus.plexus.Neuron instance at 0x7f27faa81758>: 0.6, <plexus.plexus.Neuron instance at 0x7f27fa9ff7a0>: 0.55, <plexus.plexus.Neuron instance at 0x7f27fab4d3f8>: 0.27, <plexus.plexus.Neuron instance at 0x7f27fa8537e8>: 0.52, <plexus.plexus.Neuron instance at 0x7f27fa7e5830>: 0.55, <plexus.plexus.Neuron instance at 0x7f27fac19908>: 0.37, <plexus.plexus.Neuron instance at 0x7f27fa5d1950>: 0.28, <plexus.plexus.Neuron instance at 0x7f27fa76c998>: 0.75, <plexus.plexus.Neuron instance at 0x7f27facca440>: 0.98, <plexus.plexus.Neuron instance at 0x7f27fadb39e0>: 0.87, <plexus.plexus.Neuron instance at 0x7f27facd3a70>: 0.48, <plexus.plexus.Neuron instance at 0x7f27fa7d1b48>: 0.94, <plexus.plexus.Neuron instance at 0x7f27fa9579e0>: 0.52, <plexus.plexus.Neuron instance at 0x7f27fbea16c8>: 0.99, <plexus.plexus.Neuron instance at 0x7f27faac20e0>: 0.29, <plexus.plexus.Neuron instance at 0x7f27faeefbd8>: 0.34, <plexus.plexus.Neuron instance at 0x7f27faf13c20>: 0.24, <plexus.plexus.Neuron instance at 0x7f27fa9c7c68>: 0.57, <plexus.plexus.Neuron instance at 0x7f27fa879cf8>: 0.72, <plexus.plexus.Neuron instance at 0x7f27fac07f80>: 0.9, <plexus.plexus.Neuron instance at 0x7f27fa6a9d40>: 0.41, <plexus.plexus.Neuron instance at 0x7f27fa695710>: 0.36, <plexus.plexus.Neuron instance at 0x7f27fa609518>: 0.86, <plexus.plexus.Neuron instance at 0x7f27fb005ea8>: 0.47, <plexus.plexus.Neuron instance at 0x7f27fa85ca70>: 0.78, <plexus.plexus.Neuron instance at 0x7f27fa945ef0>: 0.29, <plexus.plexus.Neuron instance at 0x7f27fa867f80>: 0.57}
```

The above output tells us how the neuron gets its feed. Each individual key-value pair stores a reference to the subscribed neuron as the key and the weight of that subscription as the value. Learning process in a Plexus network is nothing more than updating those weights and/or adding neurons to this list or dropping neurons from the list.

Each individual neuron holds two floating point number called **potential** and **instability**. To get those values:

```Shell
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

#### How an individual neuron is fired?

Currently, an individual neuron in a Plexus network is fired randomly by a single-core threaded process. The process picks a neuron from the network randomly and fires it. Firing a neuron literally means calling an instance method named **fire()** of the neuron instance and nothing more.

Because the Plexus network project rely on the complex data structures and [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) of Python programming language and because [CPython](https://en.wikipedia.org/wiki/CPython) (the most common implementation of Python) has a headache called [GIL](https://wiki.python.org/moin/GlobalInterpreterLock), it is currently impossible to gain the advantage of multi-core processing. But I'm planning to implement a workaround in the future for this specific limitation.

#### Sensory and Cognitive Neurons

Input Layer in classical neural networks renamed as **Sensory Neurons** in Plexus networks and Target/Output Layer renamed as **Cognitive Neurons**. This naming convention is necessary cause the built of the relevance of artificial neural networks with biological neural networks and Neuroscience.

The difference of sensory neurons from the interneurons (that neither sensory nor cognitive ones) is, they do not actually fire. They just stand still for your **potential** assignments. As you can guess they do not have any subscriptions to the other neurons (0 subscriptions). But they can be subscribed by the other neurons, including cognitive ones. They do not learn, they do not consume any CPU resource. They just stored in the memory. You can assign an image, a frame of a video, or a chunk of an audio to a group of sensory neurons. For example you can prepare the network for the assignment of a 64x64 RGB image like that:

```Shell
>>> net.pick_sensory_neurons(12288)
12288 neuron picked as sensory neuron.
>>> len(net.sensory_neurons)
12288
>>> net.sensory_neurons[0]
<plexus.plexus.Neuron instance at 0x7f103d3473f8>
>>> net.sensory_neurons[0].subscriptions
{}
```

The difference of cognitive neurons form the other neurons is, they are only responsible to the network. They act as the source of the learning and calculation of the fault. The network dictates a desired potential on a cognitive neuron. The cognitive neuron calculates its potential, compares it with desired potential, calculates fault then backpropagates it through the subscriptions. This is why they hold an additional potential variable called **desired_potential**. You can define the number of cognitive neurons similarly by using `net.pick_cognitive_neurons(output_dim)` function.

As you can imagine, a neuron in a Plexus network holds an integer object variable called **type** to determine its type.

- `neuron.type = 1` means it's a sensory neuron.
- `neuron.type = 2` means it's a cognitive neuron.
- `neuron.type = 0` means it's neither a sensory nor a cognitive neuron. It means it's an interneuron.

#### Destroying The Network

Lastly, don't forget to call garbage collector when you want to stop and delete the network:

```Shell
>>> net.freeze()
Network is now frozen.
>>> net.breakit()
All subscriptions in the network is now broken.
>>> del net
>>> import gc
>>> gc.collect()
340000
```
