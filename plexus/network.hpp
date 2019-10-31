#pragma once

#include <iostream>
#include <cstdlib>
#include <thread>
#include <vector>
#include <unordered_map>
#include <random>
#include <algorithm>

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
public:
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

    bool freezer;
    std::thread master_thread;
    std::thread thread2;
    bool thread_kill_signal;

    void initiate_subscriptions();
    void pick_neurons_by_type(int output_dim, NeuronType neuron_type);
    void get_neurons_by_type(NeuronType neuron_type);
    static void _ignite(Network* network);
    void ignite();
    void print_output() const;

//public:
    std::vector<Neuron*> neurons;
    std::vector<Neuron*> nonmotor_neurons;
    unsigned long long int wave_counter;
    unsigned long long int fire_counter;
    Network(
        int size,
        int input_dim,
        int output_dim,
        double connectivity,
        int precision,
        bool randomly_fire,
        bool dynamic_output,
        bool visualization,
        double decay_factor
    );
    int get_connectivity() const;
    int get_connectivity_sqrt() const;
    int get_decay_factor() const;
    void increase_initiated_neurons();
    void freeze();
    void breakit() const;
    std::vector<double> get_output() const;
    void load(std::vector<double> input_arr, std::vector<double> output_arr);
    std::vector<std::thread> threads;
};


// Requires -std=c++17 compilation flag
template<class RandomSampling>
RandomSampling random_sample(
    RandomSampling neurons,
    unsigned int sample_length
)
{
    RandomSampling sample;
    std::sample(neurons.begin(), neurons.end(), std::back_inserter(sample),
        sample_length, std::mt19937{std::random_device{}()});
    return sample;
}
