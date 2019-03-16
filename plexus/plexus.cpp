#include <Python.h>
#include <iostream>
#include <cstdlib>
#include <unordered_map>
#include <tuple>
#include <math.h>
#include <utility>
#include <thread>

#include "random.hpp"
using Random = effolkronium::random_static;

#include "neuron.h"
#include "network.h"

int glob_argc;
char **glob_argv;


double Neuron::get_potential()
{
    return this->potential;
}

Neuron::Neuron(Network& network)
{
    this->network = &network;
    this->network->neurons.push_back(&(*this));
}

void Neuron::partially_subscribe()
{
    if (this->subscriptions.size() == 0) {
        unsigned int sample_length = Random::get(this->network->get_connectivity(), this->network->get_connectivity_sqrt());
        if (sample_length > this->network->nonmotor_neurons.size())
            sample_length = this->network->nonmotor_neurons.size();
        if (sample_length <= 0)
            sample_length = 0;
        this->subscriptions.reserve(sample_length);
        for (unsigned int i = 0; i < sample_length; i++) {
            Neuron* target_neuron = this->network->nonmotor_neurons[i];
            this->subscriptions.insert( std::pair<Neuron*, double>(target_neuron, Random::get(-1.0, 1.0)) );
            target_neuron->publications.insert( std::pair<Neuron*, double>(&(*this), 0.0) );
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
    return total;
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

Network::Network(int size, int input_dim = 0, int output_dim = 0, double connectivity = 0.01, int precision = 2, bool randomly_fire = false, bool dynamic_output = false, bool visualization = false, double decay_factor = 1.0)
{
    this->precision = precision;
    std::cout << "\nPrecision of the network will be " << 1.0 / pow(10, precision) << '\n';
    this->connectivity = std::ceil(size * connectivity);
    this->connectivity_sqrt = std::ceil(sqrt(connectivity));
    std::cout << "Each individual non-sensory neuron will subscribe to " << this->connectivity << " different neurons" << '\n';

    this->neurons.reserve(size);
    for (int i = 0; i < size; i++) {
        Neuron* neuron = new Neuron(*this);
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
    std::cout << "Inside _ignite" << '\n';
    int motor_fire_counter = 0;
    std::vector<Neuron> ban_list;
    while (network->freezer == false) {
        if (network->randomly_fire) {
            Neuron* neuron = random_unique(network->sensory_neurons.begin(), network->sensory_neurons.end(), 1)[0];
            if (neuron->type == 2) {
                if (1 != Random::get(1, network->motor_randomly_fire_rate))
                    continue;
                else
                    motor_fire_counter++;

                // TODO
            }
        } else {

        }
        break;
    }
}

void Network::ignite()
{
    this->freezer = false;
    this->thread1 = std::thread{&this->_ignite, this};
    //this->thread1.detach();
    this->thread1.join();
    std::cout << "Network has been ignited" << '\n';
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
        }
    }
    switch (neuron_type) {
        case SENSORY_NEURON:
            std::cout << input_dim << " neuron picked as sensory neuron" << '\n';
            break;
        case MOTOR_NEURON:
            std::cout << input_dim << " neuron picked as motor neuron" << '\n';
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

void Network::increase_initiated_neurons()
{
    this->initiated_neurons += 1;
}

static PyObject* test(PyObject* self)
{
    Network* network = new Network(14, 4, 2);
    //network->nonsensory_neurons[0]->calculate_potential();

    Py_RETURN_NONE;
}

static PyObject* hello_world(PyObject* self)
{
    std::cout << "Hello World!" << std::endl;

    Py_RETURN_NONE;
}

static PyMethodDef cplexus_funcs[] = {
    {"hello_world", (PyCFunction)hello_world, METH_VARARGS, NULL},
    {"test", (PyCFunction)test, METH_VARARGS, NULL},
    {NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "cplexus",          /* name of module */
    "",                 /* module documentation, may be NULL */
    -1,                 /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    cplexus_funcs
};

PyMODINIT_FUNC PyInit_cplexus(void) {
    return PyModule_Create(&moduledef);
}
#endif

void initcplexus(void)
{
    #if PY_MAJOR_VERSION >= 3
    PyInit_cplexus();
    #else
    Py_InitModule3("cplexus", cplexus_funcs,
                   "Extension module example!");
    #endif
}

int main(int argc, char *argv[])
{
    glob_argc = argc;
    glob_argv = argv;

    wchar_t *program = Py_DecodeLocale(argv[0], NULL);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initcplexus();
}
