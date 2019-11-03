#pragma once

#include <iostream>
#include <cstdlib>
#include <deque>
#include <tuple>
#include <random>

#include "random.hpp"
using Random = effolkronium::random_thread_local;

class Network;

class Neuron
{
public:
    double desired_potential;
    double loss = 0.0;
    int fire_counter = 0;
    std::tuple<int, int> position;
    unsigned long index;

    static double calculate_potential_hypo(
        std::deque<std::pair<double, double>> candidate
    );
    double calculate_potential() const;
    static double activation_function(double x);
    static double derivative(double x, int n);
    static double calculate_loss(double potential, double desired_potential);

//public:
    Network *network;
    std::deque<std::pair<Neuron*, double>> subscriptions;
    std::deque<std::pair<Neuron*, double>> publications;
    double potential = Random::get(0.0, 1.0);
    int type = 0;
    int ban_counter = 0;
    explicit Neuron(Network &network);
    void partially_subscribe();
    bool fire();
    static void live(Neuron* neuron);

    std::deque<double> requests;
    void update_requests();
    bool train();
};
