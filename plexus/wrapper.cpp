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
    int test;
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
    self->test = 5;

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

static int PyNetwork_get_test(PyNetwork *self, void *closure)
{
    std::cout << "Test get" << '\n';
    Py_INCREF(self->test);
    return self->test;
}

static int PyNetwork_set_test(PyNetwork *self, int value, void *closure)
{
    std::cout << "Test set" << '\n';
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the test attribute");
        return -1;
    }

    Py_DECREF(self->test);
    Py_INCREF(value);
    self->test = value;

    return 0;
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
    {NULL}  /* Sentinel */
};

static PyMemberDef PyNeuron_members[] = {
    {NULL}  /* Sentinel */
};

static PyGetSetDef PyNetwork_getseters[] = {
    {"test", (getter)PyNetwork_get_test, (setter)PyNetwork_set_test, "Precision of the network", NULL},
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
    PyNetworkType.tp_getset=PyNetwork_getseters;
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
