#pragma once

#include <iostream>
#include <cstdlib>

#include "neuron.h"

class Network
{
    int precision;
    int connectivity;
    int connectivity_sqrt;

    std::vector<Neuron> neurons;
    std::vector<Neuron> sensory_neurons;
    int input_dim;
    std::vector<Neuron> motor_neurons;
    int output_dim;

    std::vector<Neuron> nonsensory_neurons;
    std::vector<Neuron> nonmotor_neurons;
    std::vector<Neuron> interneurons;
    bool randomly_fire;
    int motor_randomly_fire_rate;

    bool dynamic_output;
    float decay_factor;

    int initiated_neurons;

    int fire_counter;
    std::unordered_map<double, double> first_queue;
    std::unordered_map<double, double> next_queue;
    std::vector<double> output;
    int wave_counter;

    bool freezer;
    bool thread_kill_signal;
};
