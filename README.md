<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/full.gif" alt="Plexus"/>
</p>

## Core Principles

These are the core principles of **exceptionally bio-inspired**, a revolutionary approach to the artificial neural networks:

 - **Neurons** must be **objects** not tensors between matrices.
 - Each neuron should have **its own thread** (ideally).
 - **Network** must be **architecture-free** (i.e. adaptive).
 - Network must have a **layerless design**.
 - There must be fundamentally two types of neurons: **sensory neuron**, **interneuron**.
 - Input of the network must be made of sensory neurons. Any interneuron can be picked as a **motor neuron** (an element of the output). There is literally no difference between an interneuron and a motor neuron except the intervene of the network for igniting the wick of learning process through the motor neurons. Any non-motor interneuron can be assumed as a **cognitive neuron** which collectively forms the cognition of network.
 - There can be arbitrary amount of I/O groups in a single network.
 - Forget about batch size, iteration, and epoch concepts, training examples must be fed on time basis with a manner like; *learn first sample for ten seconds, OK done? then learn second sample for twenty seconds*. By this approach, you can assign importance factors to your samples with maximum flexibility.
 - **Network** must be **retrainable**.
 - Network must be **modular**. In other words: You must be able to train a small network and then plug that network into a bigger network (we are talking about some kind of **self-fusing** here).
 - Neurons must exhibit the characteristics of **cellular automata**.
 - **Number of neurons** in the network can be increased or decreased (**scalability**).
 - There must be **no** need for a network-wide **oscillation**. Yet the execution of neurons should follow a path very similar to flow of electric current nevertheless it's not compulsory.
 - Network should use **randomness** and/or **uncertainty principle** flawlessly.
 - Most importantly, the network **must and can not iterate** through the whole dataset. Besides that, it's also generally impossible iterate the dataset on real life situations if the system is continuous like in robotics. Because of that the network must be designed to handle such a **continuous data stream** that literally endless and must be designed to handle that data stream chunk by chunk. Therefore, when you are feeding the network you should follow a path like; *on my left hand there is an apple and on my right hand there is a banana, apple... banana... apple, banana, apple, banana, ...* if you want to teach the difference between apple and banana and don't follow a path like; *apple, apple, apple, apple, banana, banana, banana, banana, ...* More technically; if you have two classes to train the network, use a diverse feed but not grouped feed (*ideally repetitive like 121212121212 but not 1111111222222*).

### Activation function

<sup>*( c : average connectivity of a neuron )*</sup>

<p align="left">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/activation.png" alt="Activation function"/>
</p>

<!-- LaTeX of above image:  \varphi (x) = \left |  \sin \bigg(\frac{ x^2 }{ \sqrt{c} }\bigg) \right |  -->

<sup>[Draw the graph](https://www.desmos.com/calculator/1al0bavp78) of this equation to see how it's insanely suitable to make random normalizations for any values between (-∞,+∞). It's also becoming more crazy, less stable when you move away from 0. In other words, it's not completely repetitive so a neuron freely walk on this equation without being trapped.</sup>

Rest of the paper will explain the algorithm's itself and usage. An algorithm that implemented by following the criteria listed in Core Principles and by relying on the given activation function above.

Implementation of this algorithm in Python programming language is publicly accessible through this link: https://github.com/mertyildiran/Plexus/blob/master/plexus/plexus.py

Reading this paper requires basic knowledge of Computer Science and Neuroscience.

## Algorithm

### Basics

The algorithm is named as **Plexus Network**. Plexus Network has only two classes; **Network** and **Neuron**. In a Plexus Network, there are many instances of Neuron class but there is only one instance of Network class.

When you crate a new Plexus Network you give these five parameters to the Network class: *size of the network*, *input dimension*, *output dimension*, *connectivity rate*, *precision of the network* So that the network builds itself.

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/init.png" alt="Network init function"/>
</p>

<!-- LaTeX of above image:  \Theta (n,i,o,c, \rho )  -->

 - **size** is literally equal to total number of neurons in the network. All neurons are referenced in an instance variable called `Network.neurons`
 - **input dimension** specifies the number of sensory neurons. Sensory neurons are randomly selected from neurons.
 - **output dimension** specifies the number of motor neurons. Motor neurons are randomly selected from non-sensory neurons.
 - number of neurons multiplied by **connectivity rate** gives the average number of subscriptions made by a single neuron.
 - **precision** simply defines the precision of the all calculations will be made by neurons (how many digits after the decimal point).

After the network has been successfully created. It will ignite itself automatically. Ignition in simple terms, no matter if you have plugged in some data or not, it will fire the neurons with using some mechanism very similar to flow of electric current (*will be explained later on this paper*).

#### Anatomy of a Single Neuron

A single neuron in a Plexus Network holds these seven very important information (in it's instance variables): *subscriptions*, *publications*, *potential*, *desired_potential*, *loss* and *type*

There are eventually there types of neurons:

 - `Neuron.type = 1` means it's a sensory neuron.
 - `Neuron.type = 2` means it's a motor neuron.
 - `Neuron.type = 0` means it's neither a sensory nor a motor neuron. It means it's an cognitive interneuron (or just cognitive neuron).

Functionality of a neuron is relative to its type.

**subscriptions** is neuron's indirect data feed. Each non-sensory neuron subscribes to some other neurons of any type. For sensory neurons subscriptions are completely meaningless and empty by default because it gets its data feed from outside world by assignments of the network. It is literally the Plexus Network equivalent of **Dendrites** in biological neurons. *subscriptions* is a dictionary that holds **Neuron(reference)** as key and **Weight** as value.

**publications** holds literally the mirror data of *subscriptions* in the target neurons. In other words; any subscription creates also a publication reference in the target neuron. Similarly, *publications* is the Plexus Network equivalent of **Axons** in biological neurons.

**potential** is the overall total potential value of all subscriptions multiplied by the corresponding weights. Only in sensory neurons, it is directly assigned by the network. Value of **potential** may only be updated by the neuron's itself and its being calculated by this simple formula each time when the neuron is fired:

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/total_potential.png" alt="Total potential"/>
</p>

<!-- LaTeX of above image:  \underline{t}otal = ( \underline{p}otential_{0} \times \underline{w}eight_{0} )\ +\ ( p_{1} \times w_{1} )\ +\ ( p_{2} \times w_{2} )\ +\ ...\ +\ ( p_{n} \times w_{n} )  -->

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/apply_activation.png" alt="Apply activation"/>
</p>

<!-- LaTeX of above image:  \underline{p}otential =  \varphi (t)  -->

**desired_potential** is the ideal value of the neuron's potential that is desired to eventually reach. For sensory neurons, it is meaningless. For motor neurons, it is assigned by the network. If it's **None** then neuron don't learn anything and just calculates potential when it's fired.

**loss** is calculated not just at the output but in every neuron except sensory ones and it is equal to absolute difference (*distance*) between desired potential and current potential.

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/calc_of_loss.png" alt="Calculation of loss"/>
</p>

<!-- LaTeX of above image:  \underline{f} ault = \left | \Delta p \right |  -->

All numerical values inside a neuron are floating point numbers and all the calculations obey to precision that given at start.

#### Sensory and Motor Neurons

Input Layer in classical neural networks renamed as **Sensory Neurons** in Plexus networks, and Target/Output Layer renamed as **Motor Neurons**. This naming convention is necessary cause the built of the relevance of artificial neural networks with biological neural networks and Neuroscience.

The difference of sensory neurons from the cognitive neurons (that neither sensory nor motor ones) is, they do not actually fire. They just stand still for the data load. They do not have any subscriptions to the other neurons (literally no subscriptions). But they can be subscribed by the other neurons, including motor ones. They do not learn, they do not consume any CPU resources. They just stored in the memory. You can assign an image, a frame of a video, or a chunk of an audio to a group of sensory neurons.

The difference of motor neurons form the other neurons is, they are only responsible to the network. They act as the fuse of the learning and calculation of the loss. The network dictates a desired potential on each motor neuron. The motor neuron calculates its potential, compares it with desired potential, calculates the loss then tries to update its weights randomly many times and if it fails, it blames its subscriptions. So just like the network, motor neurons can also dictates a desired potential on the other non-motor neurons. This is why any neuron holds an additional potential variable called **desired_potential**.

#### Partially Subscribe

On the second phase of the network initiation, any non-sensory neurons are forced to subscribe to some non-motor neurons which are selected by random sampling. Length of this sample is also selected by a random sampling (*rounds to nearest integer*) is done from a normal distribution. Such a normal distribution that, the average connectivity of a neuron is the mean, and square root of the mean is the standard deviation. (*e.g. if neurons on average has 100 subscriptions then the mean is 100 and the standard deviation is 10*)

<p align="center">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/normal_distribution.png" alt="Normal distribution"/>
</p>

<!-- LaTeX of above image:  P(x) = \frac{1}{{ \sqrt {2\pi c } }} \ e^{ - \frac{( x - c )^2}{2c}}  -->

### Installation

```Shell
sudo pip install plexus
```

## Details & Usage

Install Plexus with:

```Shell
pip install -e .
```

Create a new network:

```Shell
>>> import plexus
>>> net = plexus.Network(10000)

Precision of the network will be 0.01
Each individual neuron will subscribe to 100 different neurons


10000 neurons created
Initiated: 10000 neurons

0 neuron picked as sensory neuron
0 neuron picked as motor neuron


Network has been ignited

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

### Basics

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

Each individual neuron holds a floating point number called **potential** which is the only meaningful value except weight. If you want to investigate this word choice, please take a look to its biological counterpart [Action potential](https://en.wikipedia.org/wiki/Action_potential). To read this value:

```Shell
>>> net.neurons[0].potential
0.91
```

#### How an individual neuron is fired?

Currently, an individual neuron in a Plexus network is fired randomly by a single-core threaded process. The process picks a neuron from the network randomly and fires it. Firing a neuron literally means calling an instance method named **fire()** and nothing more.

Because of this implementation of the Plexus network relies on the complex data structures and [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) of Python programming language and because [CPython](https://en.wikipedia.org/wiki/CPython) (the most common implementation of Python) has a headache called [GIL](https://wiki.python.org/moin/GlobalInterpreterLock), it is currently impossible to gain the advantage of multi-core processing. But I'm planning to implement a workaround in the future for this specific limitation.





### Let's Start

#### Basic Example

<sup>*(you can alternatively run this example with `python examples/basic.py` command using a pre-written script version of below commands)*</sup>

If you have internalized the concept and the terminology which is unique to the Plexus network, at this point, we can actually start to use it in a simple real life example. Now let's start with creating a relatively small network:

```Shell
>>> import plexus
>>> net = plexus.Network(22,4,2,1,1)

Precision of the network will be 0.1
Each individual neuron will subscribe to 22 different neurons


22 neurons created
Initiated: 22 neurons

4 neuron picked as sensory neuron
2 neuron picked as motor neuron


Network has been ignited

```

Here is a simple dataset aiming to classify numbers bigger and smaller than 0.5 for this network:

```no-highlight
Input: [0.6, 0.7, 0.8, 0.9] - Output: [1.0, 0.0]
Input: [0.4, 0.3, 0.2, 0.1] - Output: [0.0, 1.0]
```

Now let's load the first data:

```Shell
>>> net.load([0.6, 0.7, 0.8, 0.9], [1.0, 0.0])
Data was successfully loaded
```

The network will automatically start learning because it's already ignited. Now examine the potential of first motor neuron with entering `net.motor_neurons[0].potential` command through the Python Interactive Shell repeatedly. You should mostly see that the value is either 1.0 or is a very close number to 1.0 like 0.9, 0.8, etc. This is the very simple proof that the Plexus network is learning the data that you have just loaded and echoing the effect through the whole network.

*Note that, later on a Freeze Lock added to the load process to prevent corruption.*

Now make sure you have waited at least a few seconds and then plug in the second data:

```Shell
>>> net.load([0.4, 0.3, 0.2, 0.1], [0.0, 1.0])
Data was successfully loaded
```

Just like the previous data, you should experience the similar effect when you examine the value of `net.motor_neurons[0].potential` using the Python Interactive Shell.

You will continue to observe similar trends in the network even if you just plug in only the input arrays like below. Which is the true confirmation that our network successfully learned the dataset.

```Shell
>>> net.load([0.6, 0.7, 0.8, 0.9])
Data was successfully loaded
>>> net.motor_neurons[0].potential
0.9
>>> net.load([0.4, 0.3, 0.2, 0.1])
Data was successfully loaded
>>> net.motor_neurons[0].potential
0.2
```

As you can see, maybe the one of the most unique features of Plexus network is, learning process is non-blocking, real-time and interactive.

#### Destroying The Network

Lastly, don't forget to call garbage collector when you want to stop and delete the network:

```Shell
>>> net.freeze()
Network is now frozen.
>>> net.breakit()
All the subscriptions are now broken.
>>> del net
>>> import gc
>>> gc.collect()
340000
```
