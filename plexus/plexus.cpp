#include <iostream>
#include <cstdlib>
#include <unordered_map>
#include <math.h>
#include <utility>
#include <thread>
#include <stdexcept>
#include <ostream>

#include "random.hpp"
using Random = effolkronium::random_static;

#include "neuron.hpp"
#include "network.hpp"


Neuron::Neuron(Network& network)
{
    this->network = &network;
    this->network->neurons.push_back(&(*this));
}

void Neuron::partially_subscribe()
{
    if (this->subscriptions.size() == 0) {
        std::normal_distribution<double> distribution(this->network->get_connectivity(), this->network->get_connectivity_sqrt());
        unsigned int sample_length = static_cast<unsigned int>(roundf(distribution(this->generator)));
        if (sample_length > this->network->nonmotor_neurons.size())
            sample_length = this->network->nonmotor_neurons.size();
        if (sample_length <= 0)
            sample_length = 0;
        this->subscriptions.reserve(sample_length);
        for (unsigned int i = 0; i < sample_length; i++) {
            Neuron* target_neuron = this->network->nonmotor_neurons[i];
            if (target_neuron != this) {
                this->subscriptions.insert( std::pair<Neuron*, double>(target_neuron, Random::get(-1.0, 1.0)) );
                target_neuron->publications.insert( std::pair<Neuron*, double>(&(*this), 0.0) );
            }
        }
        this->network->increase_initiated_neurons();
    }
}

double Neuron::calculate_potential()
{
    double total = 0;
    for (auto& it: this->subscriptions) {
        total += it.first->potential * it.second;
    }
    return this->activation_function(total);
}

double Neuron::activation_function(double x)
{
    return 1 / (1 + exp(-x));
}

double Neuron::derivative(double x)
{
    return x * (1 - x);
}

double Neuron::calculate_loss()
{
    try {
        return this->potential - this->desired_potential;
    } catch (const std::exception& e) {
        return 0;
    }
}

bool Neuron::fire()
{
    if (this->type != SENSORY_NEURON) {

        this->potential = this->calculate_potential();
        this->network->fire_counter++;
        this->fire_counter++;

        if (this->desired_potential != 0) {

            this->loss = this->calculate_loss();
            int alteration_sign;
            if (this->loss > 0) {
                alteration_sign = -1;
            } else if (this->loss < 0) {
                alteration_sign = 1;
            } else {
                this->desired_potential = 0;
                return true;
            }

            double alteration_value = pow(fabs(this->loss), 2);
            alteration_value = alteration_value * pow(this->network->get_decay_factor(), (this->network->fire_counter/1000));

            for (auto& it: this->subscriptions) {
                it.first->desired_potential = it.first->potential + alteration_sign * this->derivative(it.first->potential);
                this->subscriptions[it.first] = it.second + (alteration_value * alteration_sign) * this->derivative(it.first->potential);
            }
        }
    }
}


Network::Network(int size, int input_dim = 0, int output_dim = 0, double connectivity = 0.01, int precision = 2, bool randomly_fire = false, bool dynamic_output = false, bool visualization = false, double decay_factor = 1.0)
{
    this->precision = precision;
    std::cout << "\nPrecision of the network will be " << 1.0 / pow(10, precision) << '\n';
    this->connectivity = std::ceil(size * connectivity);
    this->connectivity_sqrt = std::ceil(sqrt(connectivity));
    std::cout << "Each individual non-sensory neuron will subscribe to " << this->connectivity << " different neurons" << '\n';

    this->neurons.reserve(size);
    for (int i = 0; i < size; i++) {
        new Neuron(*this);
    }
    std::cout << size << " neurons created" << '\n';

    this->input_dim = input_dim;
    this->sensory_neurons.reserve(this->input_dim);
    this->pick_neurons_by_type(this->input_dim, SENSORY_NEURON);

    this->output_dim = output_dim;
    this->motor_neurons.reserve(this->output_dim);
    this->pick_neurons_by_type(this->output_dim, MOTOR_NEURON);

    this->get_neurons_by_type(NON_SENSORY_NEURON);
    this->get_neurons_by_type(NON_MOTOR_NEURON);
    this->get_neurons_by_type(INTER_NEURON);
    this->randomly_fire = randomly_fire;
    this->motor_randomly_fire_rate = sqrt( this->nonsensory_neurons.size() / this->motor_neurons.size() );

    this->dynamic_output = dynamic_output;

    this->decay_factor = decay_factor;

    this->initiated_neurons = 0;
    this->initiate_subscriptions();

    this->fire_counter = 0;
    this->output.reserve(this->output_dim);
    this->wave_counter = 0;

    this->freezer = false;
    this->thread_kill_signal = false;
    this->ignite();
}

void Network::initiate_subscriptions()
{
    std::vector<Neuron*> available_neurons;
    std::vector<Neuron*>::iterator neuron;
    unsigned int i = 0;
    for (neuron = this->neurons.begin(); neuron != this->neurons.end(); neuron++, i++) {
        if ((*neuron)->type != SENSORY_NEURON) {
            (*neuron)->partially_subscribe();
            std::cout << "Initiated: " << this->initiated_neurons << " neuron(s)\r" << std::flush;
        }
        if (i == this->neurons.size()) {
            break;
        }
    }
}

void Network::_ignite(Network* network)
{
    unsigned int motor_fire_counter = 0;
    std::vector<Neuron*> ban_list;
    while (network->freezer == false) {
        if (network->randomly_fire) {
            Neuron* neuron = random_unique(network->sensory_neurons.begin(), network->sensory_neurons.end(), 1)[0];
            if (neuron->type == MOTOR_NEURON) {
                if (1 != Random::get(1, network->motor_randomly_fire_rate))
                    continue;
                else
                    motor_fire_counter++;
            }
            neuron->fire();
            if (motor_fire_counter >= network->motor_neurons.size()) {
                if (network->dynamic_output) {
                    network->print_output();
                }
                network->output = network->get_output();
                network->wave_counter++;
                motor_fire_counter = 0;
            }
        } else {
            if (network->next_queue.empty()) {
                for (auto& neuron: network->motor_neurons) {
                    neuron->fire();
                }
                for (auto& neuron: ban_list) {
                    neuron->ban_counter = 0;
                }
                ban_list.clear();
                if (network->dynamic_output) {
                    network->print_output();
                }
                network->output = network->get_output();
                network->wave_counter++;

                if (network->first_queue.empty()) {
                    for (auto& neuron: network->sensory_neurons) {
                        network->first_queue.insert(neuron->publications.begin(), neuron->publications.end());
                    }
                }
                network->next_queue = network->first_queue;
            }

            std::unordered_map<Neuron*, double> current_queue = network->next_queue;
            network->next_queue.clear();
            for (auto& neuron: ban_list) {
                if (neuron->ban_counter > network->get_connectivity_sqrt())
                    current_queue.erase(neuron);
            }
            while (current_queue.size() > 0) {
                auto it = current_queue.begin();
                std::advance(it, rand() % current_queue.size());
                Neuron* neuron = it->first;
                current_queue.erase(neuron);
                if (neuron->ban_counter <= network->get_connectivity_sqrt()) {
                    if (neuron->type == MOTOR_NEURON) {
                        continue;
                    }
                    neuron->fire();
                    ban_list.push_back(neuron);
                    neuron->ban_counter++;
                    network->next_queue.insert(neuron->publications.begin(), neuron->publications.end());
                }
            }
        }
        //break;
    }
}

void Network::ignite()
{
    this->freezer = false;
    this->thread1 = std::thread{&this->_ignite, this};
    //this->thread1.detach();
    //this->thread1.join();
    std::cout << "Network has been ignited" << '\n';
}

void Network::freeze()
{
    this->freezer = true;
    this->thread_kill_signal = true;
    std::cout << "Network is now frozen" << '\n';
}

void Network::breakit()
{
    for (auto& neuron: this->neurons) {
        neuron->subscriptions.clear();
    }
    std::cout << "All the subscriptions are now broken" << '\n';
}

void Network::pick_neurons_by_type(int input_dim, NeuronType neuron_type)
{
    std::vector<Neuron*> available_neurons;
    std::vector<Neuron*>::iterator neuron;
    unsigned int i = 0;
    for (neuron = this->neurons.begin(); neuron != this->neurons.end(); neuron++, i++) {
        if ((*neuron)->type == INTER_NEURON) {
            available_neurons.push_back((*neuron));
        }
        if (i == this->neurons.size()) {
            break;
        }
    }
    for (int j = 0; j < input_dim; j++) {
        switch (neuron_type) {
            case SENSORY_NEURON:
                available_neurons[j]->type = SENSORY_NEURON;
                this->sensory_neurons.push_back(available_neurons[j]);
                break;
            case MOTOR_NEURON:
                available_neurons[j]->type = MOTOR_NEURON;
                this->motor_neurons.push_back(available_neurons[j]);
                break;
            default:
                throw std::invalid_argument("Network::pick_neurons_by_type(int input_dim, NeuronType neuron_type) function only accepts SENSORY_NEURON or MOTOR_NEURON as the neuron type!");
                break;
        }
    }
    switch (neuron_type) {
        case SENSORY_NEURON:
            std::cout << input_dim << " neuron picked as sensory neuron" << '\n';
            break;
        case MOTOR_NEURON:
            std::cout << input_dim << " neuron picked as motor neuron" << '\n';
            break;
        default:
            throw std::invalid_argument("Network::pick_neurons_by_type(int input_dim, NeuronType neuron_type) function only accepts SENSORY_NEURON or MOTOR_NEURON as the neuron type!");
            break;
    }
}

void Network::get_neurons_by_type(NeuronType neuron_type)
{
    std::vector<Neuron*> available_neurons;
    std::vector<Neuron*>::iterator neuron;
    unsigned int i = 0;
    for (neuron = this->neurons.begin(); neuron != this->neurons.end(); neuron++, i++) {
        switch (neuron_type) {
            case NON_SENSORY_NEURON:
                if ((*neuron)->type != SENSORY_NEURON) {
                    this->nonsensory_neurons.push_back((*neuron));
                }
                break;
            case NON_MOTOR_NEURON:
                if ((*neuron)->type != MOTOR_NEURON) {
                    this->nonmotor_neurons.push_back((*neuron));
                }
                break;
            case INTER_NEURON:
                if ((*neuron)->type == INTER_NEURON) {
                    this->interneurons.push_back((*neuron));
                }
                break;
            default:
                throw std::invalid_argument("Network::pick_neurons_by_type(int input_dim, NeuronType neuron_type) function only accepts NON_SENSORY_NEURON, NON_MOTOR_NEURON or INTER_NEURON as the neuron type!");
                break;
        }
        if (i == this->neurons.size()) {
            break;
        }
    }
}

int Network::get_connectivity()
{
    return this->connectivity;
}

int Network::get_connectivity_sqrt()
{
    return this->connectivity_sqrt;
}

int Network::get_decay_factor()
{
    return this->decay_factor;
}

void Network::increase_initiated_neurons()
{
    this->initiated_neurons += 1;
}

std::vector<double> Network::get_output()
{
    std::vector<double> output;
    for (auto& neuron: this->motor_neurons) {
        int decimals = pow(10, this->precision);
        output.push_back(roundf(neuron->potential * decimals) / decimals);
    }
    return output;
}

void Network::print_output()
{
    std::vector<double> output = this->get_output();
    std::cout << "\r";
    std::cout << "Output: ";
    for (const auto& i: output)
        std::cout << i << ' ';
}

void Network::load(std::vector<double> input_arr, std::vector<double> output_arr)
{
    std::vector<Neuron*>::iterator neuron;
    unsigned int i = 0;
    if (this->sensory_neurons.size() != input_arr.size()) {
        std::cout << "Size of the input array: " << input_arr.size() << '\n';
        std::cout << "Number of the sensory neurons: " << this->sensory_neurons.size() << '\n';
        std::cout << "Size of the input array and number of the sensory neurons are not matching! Please try again" << '\n';
    } else {
        int step = 0;
        for (neuron = this->sensory_neurons.begin(); neuron != this->sensory_neurons.end(); neuron++, i++) {
            (*neuron)->potential = input_arr[step];
            step++;
        }
    }
    if (output_arr.empty()) {
        int step = 0;
        this->freezer = true;
        for (neuron = this->nonsensory_neurons.begin(); neuron != this->nonsensory_neurons.end(); neuron++, i++) {
            (*neuron)->potential = NULL;
            step++;
        }
        this->freezer = false;
    } else {
        if (this->motor_neurons.size() != output_arr.size()) {
            std::cout << "Size of the output/target array: " << output_arr.size() << '\n';
            std::cout << "Number of the motor neurons: " << this->motor_neurons.size() << '\n';
            std::cout << "Size of the output/target array and number of the motor neurons are not matching! Please try again" << '\n';
        } else {
            int step = 0;
            for (neuron = this->motor_neurons.begin(); neuron != this->motor_neurons.end(); neuron++, i++) {
                (*neuron)->potential = output_arr[step];
                step++;
            }
        }
    }
}
