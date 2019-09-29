#pragma once

#include <iostream>
#include <cstdlib>
#include <unordered_map>
#include <tuple>
#include <random>

#include "random.hpp"
using Random = effolkronium::random_static;

class Network;

class Neuron
{
    double desired_potential;
    double loss;
    int fire_counter = 0;
    std::tuple<int, int> position;
    unsigned int index;
    std::default_random_engine generator;

    double calculate_potential();
    double activation_function(double x);
    double derivative(double x);
    double calculate_loss();

public:
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
