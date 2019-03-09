#pragma once

#include <iostream>
#include <cstdlib>

class Neuron;

class Network
{
    int precision;
    int connectivity;
    int connectivity_sqrt;

    std::vector<Neuron*> sensory_neurons;
    int input_dim;
    std::vector<Neuron*> motor_neurons;
    int output_dim;

    std::vector<Neuron*> nonsensory_neurons;
    std::vector<Neuron*> nonmotor_neurons;
    std::vector<Neuron*> interneurons;
    bool randomly_fire;
    int motor_randomly_fire_rate;

    bool dynamic_output;
    double decay_factor;

    int initiated_neurons;

    int fire_counter;
    std::unordered_map<double, double> first_queue;
    std::unordered_map<double, double> next_queue;
    std::vector<double> output;
    int wave_counter;

    bool freezer;
    bool thread_kill_signal;

public:
    std::vector<Neuron*> neurons;
    Network(int size, int input_dim, int output_dim, double connectivity, int precision, bool randomly_fire, bool dynamic_output, bool visualization, double decay_factor);
    void pick_sensory_neurons(int input_dim);
    void pick_motor_neurons(int output_dim);
    void get_nonsensory_neurons();
    void get_nonmotor_neurons();
    void get_interneurons();
};
