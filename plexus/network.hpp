#pragma once

#include <iostream>
#include <cstdlib>
#include <thread>

class Neuron;

enum NeuronType
{
    INTER_NEURON,
    SENSORY_NEURON,
    MOTOR_NEURON,
    NON_MOTOR_NEURON,
    NON_SENSORY_NEURON
};

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
    std::vector<Neuron*> interneurons;
    bool randomly_fire;
    int motor_randomly_fire_rate;

    bool dynamic_output;
    double decay_factor;

    int initiated_neurons;

    std::unordered_map<Neuron*, double> first_queue;
    std::unordered_map<Neuron*, double> next_queue;
    std::vector<double> output;
    int wave_counter;

    bool freezer;
    std::thread thread1;
    std::thread thread2;
    bool thread_kill_signal;

    void initiate_subscriptions();
    void pick_neurons_by_type(int output_dim, NeuronType neuron_type);
    void get_neurons_by_type(NeuronType neuron_type);
    static void _ignite(Network* network);
    void ignite();
    std::vector<double> get_output();
    void print_output();

public:
    std::vector<Neuron*> neurons;
    std::vector<Neuron*> nonmotor_neurons;
    int fire_counter;
    Network(int size, int input_dim, int output_dim, double connectivity, int precision, bool randomly_fire, bool dynamic_output, bool visualization, double decay_factor);
    int get_connectivity();
    int get_connectivity_sqrt();
    int get_decay_factor();
    void increase_initiated_neurons();
    void freeze();
    void breakit();
    void load(std::vector<double> input_arr, std::vector<double> output_arr);
};

// Function to get a random sampling from a vector using Fisher-Yates shuffle method
template<class BidiIter >
BidiIter random_unique(BidiIter begin, BidiIter end, size_t num_random) {
    size_t left = std::distance(begin, end);
    while (num_random--) {
        BidiIter r = begin;
        std::advance(r, rand()%left);
        std::swap(*begin, *r);
        ++begin;
        --left;
    }
    return begin;
}
