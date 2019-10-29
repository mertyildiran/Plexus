#pragma once

#include <iostream>
#include <cstdlib>
#include <unordered_map>
#include <tuple>
#include <random>

#include "random.hpp"
using Random = effolkronium::random_thread_local;

class Network;

class Neuron
{
public:
    double desired_potential;
    double loss;
    int fire_counter = 0;
    std::tuple<int, int> position;
    unsigned long index;

    double calculate_potential() const;
    double activation_function(double x) const;
    double derivative(double x) const;
    double calculate_loss() const;

//public:
    Network *network;
    std::unordered_map<Neuron*, double> subscriptions;
    std::unordered_map<Neuron*, double> publications;
    double potential = Random::get(0.0, 1.0);
    int type = 0;
    int ban_counter = 0;
    Neuron(Network &network);
    void partially_subscribe();
    bool fire();
};
