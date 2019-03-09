#pragma once

#include <iostream>
#include <cstdlib>

#include "random.hpp"
using Random = effolkronium::random_static;

class Network;

class Neuron
{
    Network *network;
    //std::unordered_map<Neuron, double> subscriptions;
    //std::unordered_map<Neuron, double> publications;
    double potential = Random::get(0.0, 1.0);
    double desired_potential;
    double loss;
    int type = 0;
    int fire_counter = 0;
    int ban_counter = 0;
    std::tuple<int, int> position;
    unsigned int index;

public:
    Neuron(Network network);
    double get_potential();
};
