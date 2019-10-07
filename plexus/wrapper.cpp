#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"
#include <stdexcept>

#include "neuron.hpp"
#include "network.hpp"

int glob_argc;
char **glob_argv;


void parse_iterable(std::vector<double> &arr, PyObject *iter)
{
    while (true) {
        PyObject *next = PyIter_Next(iter);
        if (!next) {
            // nothing left in the iterator
            break;
        }

        if (!PyFloat_Check(next)) {
            throw std::invalid_argument("One of the arguments contains an illegal value (other than float)");
        }

        double val = PyFloat_AsDouble(next);
        arr.push_back(val);
    }
}

typedef struct {
    PyObject_HEAD
    Network * ptrObj;
    int& precision;
    int& connectivity;
    int& connectivity_sqrt;
    int& input_dim;
    int& output_dim;
    bool& randomly_fire;
    int& motor_randomly_fire_rate;
    bool& dynamic_output;
    double& decay_factor;
    int& initiated_neurons;
    bool& freezer;
    bool& thread_kill_signal;
    unsigned long long int& wave_counter;
    unsigned long long int& fire_counter;
} PyNetwork;

typedef struct {
    PyObject_HEAD
    Neuron * ptrObj;
} PyNeuron;

static int PyNetwork_init(PyNetwork *self, PyObject *args, PyObject *kwargs)
{
    int size;
    int input_dim = 0;
    int output_dim = 0;
    double connectivity = 0.01;
    int precision = 2;
    int randomly_fire = false;
    int dynamic_output = false;
    int visualization = false;
    double decay_factor =  1.0;

    static char *kwlist[] = {"size", "input_dim", "output_dim", "connectivity", "precision", "randomly_fire", "dynamic_output", "visualization", "decay_factor", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwargs, "i|iidipppd", kwlist, &size, &input_dim, &output_dim, &connectivity, &precision, &randomly_fire, &dynamic_output, &visualization, &decay_factor))
        return -1;

    self->ptrObj = new Network(size, input_dim, output_dim, connectivity, precision, randomly_fire, dynamic_output, visualization, decay_factor);

    self->precision = self->ptrObj->precision;
    self->connectivity = self->ptrObj->connectivity;
    self->connectivity_sqrt = self->ptrObj->connectivity_sqrt;
    self->input_dim = self->ptrObj->input_dim;
    self->output_dim = self->ptrObj->output_dim;
    self->randomly_fire = self->ptrObj->randomly_fire;
    self->motor_randomly_fire_rate = self->ptrObj->motor_randomly_fire_rate;
    self->dynamic_output = self->ptrObj->dynamic_output;
    self->decay_factor = self->ptrObj->decay_factor;
    self->initiated_neurons = self->ptrObj->initiated_neurons;
    self->freezer = self->ptrObj->freezer;
    self->thread_kill_signal = self->ptrObj->thread_kill_signal;
    self->wave_counter = self->ptrObj->wave_counter;
    self->fire_counter = self->ptrObj->fire_counter;

    std::cout << self->input_dim << '\n';
    std::cout << self->output_dim << '\n';
    std::cout << self->connectivity << '\n';
    std::cout << self->precision << '\n';
    std::cout << self->randomly_fire << '\n';
    std::cout << self->dynamic_output << '\n';
    std::cout << self->decay_factor << '\n';

    std::cout << self->ptrObj->input_dim << '\n';
    std::cout << self->ptrObj->output_dim << '\n';
    std::cout << self->ptrObj->connectivity << '\n';
    std::cout << self->ptrObj->precision << '\n';
    std::cout << self->ptrObj->randomly_fire << '\n';
    std::cout << self->ptrObj->dynamic_output << '\n';
    std::cout << self->ptrObj->decay_factor << '\n';

    return 0;
}

static int PyNeuron_init(PyNeuron *self, PyObject *args)
{
    PyNetwork network;

    if (! PyArg_ParseTuple(args, "O", &network))
        return -1;

    self->ptrObj = new Neuron(*network.ptrObj);

    return 0;
}

static void PyNetwork_dealloc(PyNetwork * self)
{
    delete self->ptrObj;
    Py_TYPE(self)->tp_free(self);
}

static void PyNeuron_dealloc(PyNeuron * self)
{
    delete self->ptrObj;
    Py_TYPE(self)->tp_free(self);
}

static PyObject * PyNetwork_load(PyNetwork* self, PyObject* args, PyObject *kwargs)
{
    std::vector<double> input_arr;
    std::vector<double> output_arr;
    PyObject *input_obj;
    PyObject *output_obj = Py_None;

    static char *kwlist[] = {"input_obj", "output_obj", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", kwlist, &input_obj, &output_obj))
        throw std::invalid_argument("Wrong type of argument");

    PyObject *input_iter = PyObject_GetIter(input_obj);
    if (!input_iter) {
        throw std::invalid_argument("Input argument is not iterable");
    }
    parse_iterable(input_arr, input_iter);

    if (output_obj != Py_None) {
        PyObject *output_iter = PyObject_GetIter(output_obj);
        if (!output_iter) {
            throw std::invalid_argument("Output argument is not iterable");
        }
        parse_iterable(output_arr, output_iter);
    }

    (self->ptrObj)->load(input_arr, output_arr);

    return Py_BuildValue("");
}

static PyObject * PyNetwork_output(PyNetwork* self)
{
    std::vector<double> output;

    output = (self->ptrObj)->get_output();

    PyObject *PList = PyList_New(0);
    std::vector<int>::const_iterator it;

    for (const auto& i: output)
        PyList_Append(PList, Py_BuildValue("d", i));

    return PList;
}

static PyObject * PyNetwork_freeze(PyNetwork* self)
{
    (self->ptrObj)->freeze();

    return Py_BuildValue("");
}

static PyMethodDef PyNetwork_methods[] = {
    {"load", (PyCFunction)PyNetwork_load, METH_VARARGS | METH_KEYWORDS, "Load input and output into the neural network" },
    {"output", (PyCFunction)PyNetwork_output, METH_NOARGS, "Returns the output of the neural network" },
    {"freeze", (PyCFunction)PyNetwork_freeze, METH_NOARGS, "Freeze the neural network" },
    {NULL}  /* Sentinel */
};

static PyMethodDef PyNeuron_methods[] = {
    {NULL}  /* Sentinel */
};

static PyMemberDef PyNetwork_members[] = {
    {"precision", T_INT, offsetof(PyNetwork, precision), READONLY, "Precision of the network"},
    {"connectivity", T_INT, offsetof(PyNetwork, connectivity), READONLY, "Connectivity of the network"},
    {"connectivity_sqrt", T_INT, offsetof(PyNetwork, connectivity_sqrt), READONLY, "Square root of the connectivity of the network"},
    {"input_dim", T_INT, offsetof(PyNetwork, input_dim), READONLY, "Input dimension of the network"},
    {"output_dim", T_INT, offsetof(PyNetwork, output_dim), READONLY, "Output dimension of the network"},
    {"randomly_fire", T_BOOL, offsetof(PyNetwork, randomly_fire), READONLY, "Is randomly fire enabled for the network?"},
    {"motor_randomly_fire_rate", T_INT, offsetof(PyNetwork, motor_randomly_fire_rate), READONLY, "Motor neurons' randomly fire rate"},
    {"dynamic_output", T_BOOL, offsetof(PyNetwork, dynamic_output), READONLY, "Is dynamic output enabled for the network?"},
    {"decay_factor", T_DOUBLE, offsetof(PyNetwork, decay_factor), READONLY, "Decay factor of the network"},
    {"initiated_neurons", T_INT, offsetof(PyNetwork, initiated_neurons), READONLY, "Initiated neuron count of the network"},
    {"freezer", T_BOOL, offsetof(PyNetwork, freezer), READONLY, "Is freezing enabled for the network?"},
    {"thread_kill_signal", T_BOOL, offsetof(PyNetwork, thread_kill_signal), READONLY, "Are threads signalled for kill?"},
    {"wave_counter", T_LONG, offsetof(PyNetwork, wave_counter), READONLY, "Holds the integer value of how many waves executed throughout the network"},
    {"fire_counter", T_LONG, offsetof(PyNetwork, fire_counter), READONLY, "Holds the integer value of how many neurons fired during the training"},
    {NULL}  /* Sentinel */
};

static PyMemberDef PyNeuron_members[] = {
    {NULL}  /* Sentinel */
};

static PyTypeObject PyNetworkType = { PyVarObject_HEAD_INIT(NULL, 0)
    "plexus.Network"   /* tp_name */
};

static PyTypeObject PyNeuronType = { PyVarObject_HEAD_INIT(NULL, 0)
    "plexus.Neuron"   /* tp_name */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "cplexus",          /* name of module */
    "",                 /* module documentation, may be NULL */
    -1,                 /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_cplexus(void)
// create the module
{
    PyObject* m;

    PyNetworkType.tp_new = PyType_GenericNew;
    PyNetworkType.tp_basicsize=sizeof(PyNetwork);
    PyNetworkType.tp_dealloc=(destructor) PyNetwork_dealloc;
    PyNetworkType.tp_flags=Py_TPFLAGS_DEFAULT;
    PyNetworkType.tp_doc="Network objects";
    PyNetworkType.tp_methods=PyNetwork_methods;
    PyNetworkType.tp_members=PyNetwork_members;
    PyNetworkType.tp_init=(initproc)PyNetwork_init;

    PyNeuronType.tp_new = PyType_GenericNew;
    PyNeuronType.tp_basicsize=sizeof(PyNeuron);
    PyNeuronType.tp_dealloc=(destructor) PyNeuron_dealloc;
    PyNeuronType.tp_flags=Py_TPFLAGS_DEFAULT;
    PyNeuronType.tp_doc="Neuron objects";
    PyNeuronType.tp_methods=PyNeuron_methods;
    PyNeuronType.tp_members=PyNeuron_members;
    PyNeuronType.tp_init=(initproc)PyNeuron_init;

    if (PyType_Ready(&PyNetworkType) < 0)
        return NULL;

    if (PyType_Ready(&PyNeuronType) < 0)
        return NULL;

    m = PyModule_Create(&moduledef);
    if (m == NULL)
        return NULL;

    Py_INCREF(&PyNetworkType);
    Py_INCREF(&PyNeuronType);
    PyModule_AddObject(m, "Network", (PyObject *)&PyNetworkType); // Add Network object to the module
    PyModule_AddObject(m, "Neuron", (PyObject *)&PyNeuronType); // Add Neuron object to the module
    return m;
}

void initcplexus(void)
{
    PyInit_cplexus();
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
