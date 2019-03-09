#include <Python.h>
#include <iostream>
#include <cstdlib>
#include <unordered_map>
#include <tuple>
#include <math.h>

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

Network::Network(int size, int input_dim = 0, int output_dim = 0, double connectivity = 0.01, int precision = 2, bool randomly_fire = false, bool dynamic_output = false, bool visualization = false, double decay_factor = 1.0)
{
    this->precision = precision;
    std::cout << "\nPrecision of the network will be " << 1.0 / pow(10, precision) << '\n';
    this->connectivity = size * connectivity;
    this->connectivity_sqrt = sqrt(connectivity);
    std::cout << "Each individual non-sensory neuron will subscribe to " << this->connectivity << " different neurons" << '\n';

    this->neurons.reserve(size);
    for (int i = 0; i < size; i++) {
        Neuron* neuron = new Neuron(*this);
    }
    std::cout << size << " neurons created" << '\n';

    this->input_dim = input_dim;
    this->sensory_neurons.reserve(this->input_dim);
    this->pick_sensory_neurons(this->input_dim);

    this->output_dim = output_dim;
    this->motor_neurons.reserve(this->output_dim);
    this->pick_motor_neurons(this->output_dim);

    this->randomly_fire = randomly_fire;

    this->dynamic_output = dynamic_output;

    this->decay_factor = decay_factor;

    this->initiated_neurons = 0;

    this->fire_counter = 0;
    this->output.reserve(this->output_dim);
    this->wave_counter = 0;

    this->freezer = false;
    this->thread_kill_signal = false;
}

void Network::pick_sensory_neurons(int input_dim)
{
    std::vector<Neuron*> available_neurons;
    std::vector<Neuron*>::iterator neuron;
    int i = 0;
    for (neuron = this->neurons.begin(); neuron != this->neurons.end(); neuron++, i++) {
        if ((*neuron)->type == 0) {
            available_neurons.push_back((*neuron));
        }
        if (i == this->neurons.size()) {
            break;
        }
    }
    for (int j = 0; j < input_dim; j++) {
        available_neurons[j]->type = 1;
        this->sensory_neurons.push_back(available_neurons[j]);
    }
    std::cout << input_dim << " neuron picked as sensory neuron" << '\n';
}

void Network::pick_motor_neurons(int input_dim)
{
    std::vector<Neuron*> available_neurons;
    std::vector<Neuron*>::iterator neuron;
    int i = 0;
    for (neuron = this->neurons.begin(); neuron != this->neurons.end(); neuron++, i++) {
        if ((*neuron)->type == 0) {
            available_neurons.push_back((*neuron));
        }
        if (i == this->neurons.size()) {
            break;
        }
    }
    for (int j = 0; j < input_dim; j++) {
        available_neurons[j]->type = 2;
        this->motor_neurons.push_back(available_neurons[j]);
    }
    std::cout << input_dim << " neuron picked as motor neuron" << '\n';
}

static PyObject* test(PyObject* self)
{
    Network* network = new Network(14, 4, 2);

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
