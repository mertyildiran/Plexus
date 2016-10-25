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
 - Network must be **modular**. In other words: You must be able to train a small network and then plug that network into a bigger network (we are talking about some kind of **self-fusing** here).
 - Neurons must exhibit characteristics of **cellular automata**.
 - **Number of neurons** in network can be increased or decreased (**scalability**).
 - There must be **no** need for a network-wide **oscillation**.

### Activation function

<p align="left">
  <img src="https://raw.githubusercontent.com/mertyildiran/Plexus/master/docs/img/activation-big.png" alt="Activation function"/>
</p>

### Installation

```Shell
sudo pip install plexus
```
