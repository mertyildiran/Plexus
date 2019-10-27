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
        Py_XINCREF(next);

        if (!PyFloat_Check(next)) {
            PyErr_SetString(
                PyExc_TypeError,
                "One of the arguments contains an illegal "
                "value (other than float)"
            );
        }

        double val = PyFloat_AsDouble(next);
        Py_XDECREF(next);
        arr.push_back(val);
    }
}

static PyTypeObject PyNetworkType = { PyVarObject_HEAD_INIT(NULL, 0)
    "plexus.Network"   /* tp_name */
};

static PyTypeObject PyNeuronType = { PyVarObject_HEAD_INIT(NULL, 0)
    "plexus.Neuron"   /* tp_name */
};

typedef struct {
    PyObject_HEAD
    Network * ptrObj;
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

    static char *kwlist[] = {
        "size",
        "input_dim",
        "output_dim",
        "connectivity",
        "precision",
        "randomly_fire",
        "dynamic_output",
        "visualization",
        "decay_factor",
        NULL
    };

    if (! PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        "i|iidipppd",
        kwlist,
        &size,
        &input_dim,
        &output_dim,
        &connectivity,
        &precision,
        &randomly_fire,
        &dynamic_output,
        &visualization,
        &decay_factor
    ))
        return -1;

    self->ptrObj = new Network(
        size,
        input_dim,
        output_dim,
        connectivity,
        precision,
        randomly_fire,
        dynamic_output,
        visualization,
        decay_factor
    );

    return 0;
}

static int PyNeuron_init(PyNeuron *self, PyObject *args)
{
    PyNetwork * network;

    if (! PyArg_ParseTuple(args, "O", &network))
        return -1;

    Py_XINCREF(network);

    self->ptrObj = new Neuron(*network->ptrObj);

    return 0;
}

static void PyNetwork_dealloc(PyNetwork * self)
{
    PyObject_GC_UnTrack(self);
    delete self->ptrObj;
    Py_TYPE(self)->tp_free(self);
}

static void PyNeuron_dealloc(PyNeuron * self)
{
    PyObject_GC_UnTrack(self);
    delete self->ptrObj;
    Py_TYPE(self)->tp_free(self);
}

static PyObject * PyNetwork_load(
    PyNetwork* self,
    PyObject* args,
    PyObject *kwargs
)
{
    std::vector<double> input_arr;
    std::vector<double> output_arr;
    PyObject *input_obj;
    PyObject *output_obj = Py_None;

    static char *kwlist[] = {"input_obj", "output_obj", NULL};

    if (! PyArg_ParseTupleAndKeywords(
        args,
        kwargs,
        "O|O",
        kwlist,
        &input_obj,
        &output_obj
    ))
        PyErr_SetString(PyExc_TypeError, "Wrong type of argument");

    Py_XINCREF(input_obj);
    Py_XINCREF(output_obj);

    PyObject *input_iter = PyObject_GetIter(input_obj);
    if (!input_iter) {
        PyErr_SetString(PyExc_TypeError, "Input argument is not iterable");
    }
    parse_iterable(input_arr, input_iter);

    if (output_obj != Py_None) {
        PyObject *output_iter = PyObject_GetIter(output_obj);
        if (!output_iter) {
            PyErr_SetString(
                PyExc_TypeError,
                "Output argument is not iterable"
            );
        }
        parse_iterable(output_arr, output_iter);
    }

    Py_XDECREF(input_obj);
    Py_XDECREF(output_obj);

    (self->ptrObj)->load(input_arr, output_arr);

    return Py_BuildValue("");
}

static PyObject * PyNetwork_freeze(PyNetwork* self)
{
    (self->ptrObj)->freeze();

    return Py_BuildValue("");
}

static PyObject * PyNetwork_get_precision(PyNetwork *self, void *closure)
{
    return Py_BuildValue("i", self->ptrObj->precision);
}

static PyObject * PyNetwork_get_connectivity(PyNetwork *self, void *closure)
{
    return Py_BuildValue("i", self->ptrObj->connectivity);
}

static PyObject * PyNetwork_get_connectivity_sqrt(
    PyNetwork *self,
    void *closure
)
{
    return Py_BuildValue("i", self->ptrObj->connectivity_sqrt);
}

static PyObject * PyNetwork_get_input_dim(PyNetwork *self, void *closure)
{
    return Py_BuildValue("i", self->ptrObj->input_dim);
}

static PyObject * PyNetwork_get_output_dim(PyNetwork *self, void *closure)
{
    return Py_BuildValue("i", self->ptrObj->output_dim);
}

static PyObject * PyNetwork_get_randomly_fire(PyNetwork *self, void *closure)
{
    return Py_BuildValue("b", self->ptrObj->randomly_fire);
}

static PyObject * PyNetwork_get_motor_randomly_fire_rate(
    PyNetwork *self,
    void *closure
)
{
    return Py_BuildValue("i", self->ptrObj->motor_randomly_fire_rate);
}

static PyObject * PyNetwork_get_dynamic_output(PyNetwork *self, void *closure)
{
    return Py_BuildValue("b", self->ptrObj->dynamic_output);
}

static PyObject * PyNetwork_get_decay_factor(PyNetwork *self, void *closure)
{
    return Py_BuildValue("d", self->ptrObj->decay_factor);
}

static PyObject * PyNetwork_get_initiated_neurons(
    PyNetwork *self,
    void *closure
)
{
    return Py_BuildValue("i", self->ptrObj->initiated_neurons);
}

static PyObject * PyNetwork_get_freezer(PyNetwork *self, void *closure)
{
    return Py_BuildValue("b", self->ptrObj->freezer);
}

static PyObject * PyNetwork_get_thread_kill_signal(
    PyNetwork *self,
    void *closure
)
{
    return Py_BuildValue("b", self->ptrObj->thread_kill_signal);
}

static PyObject * PyNetwork_get_wave_counter(PyNetwork *self, void *closure)
{
    return Py_BuildValue("l", self->ptrObj->wave_counter);
}

static PyObject * PyNetwork_get_fire_counter(PyNetwork *self, void *closure)
{
    return Py_BuildValue("l", self->ptrObj->fire_counter);
}

static PyObject * PyNeuron_get_desired_potential(PyNeuron *self, void *closure)
{
    return Py_BuildValue("d", self->ptrObj->desired_potential);
}

static PyObject * PyNeuron_get_loss(PyNeuron *self, void *closure)
{
    return Py_BuildValue("d", self->ptrObj->loss);
}

static PyObject * PyNeuron_get_fire_counter(PyNeuron *self, void *closure)
{
    return Py_BuildValue("i", self->ptrObj->fire_counter);
}

static PyObject * PyNeuron_get_index(PyNeuron *self, void *closure)
{
    return Py_BuildValue("I", self->ptrObj->index);
}

static int PyNeuron_set_index(PyNeuron *self, PyObject *value, void *closue)
{
    if (value == NULL) {
        PyErr_SetString(
            PyExc_TypeError,
            "Cannot delete the position attribute"
        );
        return -1;
    }

    if (! PyLong_Check(value)) {
        PyErr_SetString(
            PyExc_TypeError,
            "The position attribute value must be an integer"
        );
        return -1;
    }

    self->ptrObj->index = PyLong_AsLong(value);

    return 0;
}

static PyObject * PyNeuron_get_potential(PyNeuron *self, void *closure)
{
    return Py_BuildValue("d", self->ptrObj->potential);
}

static PyObject * PyNeuron_get_type(PyNeuron *self, void *closure)
{
    return Py_BuildValue("i", self->ptrObj->type);
}

static PyObject * PyNeuron_get_ban_counter(PyNeuron *self, void *closure)
{
    return Py_BuildValue("i", self->ptrObj->ban_counter);
}

static PyObject * PyNeuron_get_position(PyNeuron *self, void *closure)
{
    PyObject *PList = PyList_New(0);
    Py_XINCREF(PList);
    PyList_Append(
        PList,
        Py_BuildValue(
            "i",
            std::get<0>(self->ptrObj->position)
        )
    );
    PyList_Append(
        PList,
        Py_BuildValue(
            "i",
            std::get<1>(self->ptrObj->position)
        )
    );
    return PyList_AsTuple(PList);
}

static int PyNeuron_set_position(PyNeuron *self, PyObject *value, void *closue)
{
    if (value == NULL) {
        PyErr_SetString(
            PyExc_TypeError,
            "Cannot delete the position attribute"
        );
        return -1;
    }

    if (! PyTuple_Check(value)) {
        PyErr_SetString(
            PyExc_TypeError,
            "The position attribute value must be a tuple"
        );
        return -1;
    }

    PyObject *x = PyTuple_GetItem(value, 0);
    PyObject *y = PyTuple_GetItem(value, 1);

    if (! PyFloat_Check(x) || ! PyFloat_Check(y)) {
        PyErr_SetString(
            PyExc_TypeError,
            "The elements of position attribute must be float"
        );
        return -1;
    }

    std::get<0>(self->ptrObj->position) = PyFloat_AsDouble(x);
    std::get<1>(self->ptrObj->position) = PyFloat_AsDouble(y);

    return 0;
}

static PyObject * PyNeuron_connections_PyDict_build(
    std::unordered_map<Neuron*,
    double> connections
)
{
    PyObject *PDict = PyDict_New();
    Py_XINCREF(PDict);

    for (auto& it: connections) {
        PyNeuron * neuron = PyObject_New(PyNeuron, &PyNeuronType);
        neuron->ptrObj = it.first;
        PyDict_SetItem(
            PDict,
            Py_BuildValue("O", neuron),
            Py_BuildValue("d", it.second)
        );
    }
    return PDict;
}

static PyObject * PyNeuron_get_subscriptions(PyNeuron *self, void *closure)
{
    std::unordered_map<Neuron*, double> connections
        = (self->ptrObj)->subscriptions;
    return PyNeuron_connections_PyDict_build(connections);
}

static PyObject * PyNeuron_get_publications(PyNeuron *self, void *closure)
{
    std::unordered_map<Neuron*, double> connections
        = (self->ptrObj)->publications;
    return PyNeuron_connections_PyDict_build(connections);
}


static PyObject * PyNetwork_get_output(PyNetwork *self, void *closure)
{
    std::vector<double> output;

    output = (self->ptrObj)->get_output();

    PyObject *PList = PyList_New(0);
    Py_XINCREF(PList);

    for (const auto& i: output)
        PyList_Append(PList, Py_BuildValue("d", i));

    return PList;
}

static PyObject * PyNetwork_neuron_PyList_builder(std::vector<Neuron*> neurons)
{
    PyObject *PList = PyList_New(0);
    Py_XINCREF(PList);

    for (Neuron* i: neurons) {
        PyNeuron * neuron = PyObject_New(PyNeuron, &PyNeuronType);
        neuron->ptrObj = i;
        PyList_Append(PList, Py_BuildValue("O", neuron));
    }
    return PList;
}

static PyObject * PyNetwork_get_neurons(PyNetwork *self, void *closure)
{
    std::vector<Neuron*> neurons = (self->ptrObj)->neurons;
    return PyNetwork_neuron_PyList_builder(neurons);
}

static PyObject * PyNetwork_get_sensory_neurons(PyNetwork *self, void *closure)
{
    std::vector<Neuron*> neurons = (self->ptrObj)->sensory_neurons;
    return PyNetwork_neuron_PyList_builder(neurons);
}

static PyObject * PyNetwork_get_motor_neurons(PyNetwork *self, void *closure)
{
    std::vector<Neuron*> neurons = (self->ptrObj)->motor_neurons;
    return PyNetwork_neuron_PyList_builder(neurons);
}

static PyObject * PyNetwork_get_interneurons(PyNetwork *self, void *closure)
{
    std::vector<Neuron*> neurons = (self->ptrObj)->interneurons;
    return PyNetwork_neuron_PyList_builder(neurons);
}

static PyObject * PyNetwork_get_nonsensory_neurons(
    PyNetwork *self,
    void *closure
)
{
    std::vector<Neuron*> neurons = (self->ptrObj)->nonsensory_neurons;
    return PyNetwork_neuron_PyList_builder(neurons);
}

static PyObject * PyNetwork_get_nonmotor_neurons(
    PyNetwork *self,
    void *closure
)
{
    std::vector<Neuron*> neurons = (self->ptrObj)->nonmotor_neurons;
    return PyNetwork_neuron_PyList_builder(neurons);
}

static PyMethodDef PyNetwork_methods[] = {
    {
        "load",
        (PyCFunction)PyNetwork_load,
        METH_VARARGS | METH_KEYWORDS,
        "Load input and output into the neural network"
    },
    {
        "freeze",
        (PyCFunction)PyNetwork_freeze,
        METH_NOARGS,
        "Freeze the neural network"
    },
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
    {
        "precision",
        (getter)PyNetwork_get_precision,
        NULL,
        "Precision of the network",
        NULL
    },
    {
        "connectivity",
        (getter)PyNetwork_get_connectivity,
        NULL,
        "Connectivity of the network",
        NULL
    },
    {
        "connectivity_sqrt",
        (getter)PyNetwork_get_connectivity_sqrt,
        NULL,
        "Square root of the connectivity of the network",
        NULL
    },
    {
        "input_dim",
        (getter)PyNetwork_get_input_dim,
        NULL,
        "Input dimension of the network",
        NULL
    },
    {
        "output_dim",
        (getter)PyNetwork_get_output_dim,
        NULL,
        "Output dimension of the network",
        NULL
    },
    {
        "randomly_fire",
        (getter)PyNetwork_get_randomly_fire,
        NULL,
        "Is randomly fire enabled for the network?",
        NULL
    },
    {
        "motor_randomly_fire_rate",
        (getter)PyNetwork_get_motor_randomly_fire_rate,
        NULL,
        "Motor neurons' randomly fire rate",
        NULL
    },
    {
        "dynamic_output",
        (getter)PyNetwork_get_dynamic_output,
        NULL,
        "Is dynamic output enabled for the network?",
        NULL
    },
    {
        "decay_factor",
        (getter)PyNetwork_get_decay_factor,
        NULL,
        "Decay factor of the network",
        NULL
    },
    {
        "initiated_neurons",
        (getter)PyNetwork_get_initiated_neurons,
        NULL,
        "Initiated neuron count of the network",
        NULL
    },
    {
        "freezer",
        (getter)PyNetwork_get_freezer,
        NULL,
        "Is freezing enabled for the network?",
        NULL
    },
    {
        "thread_kill_signal",
        (getter)PyNetwork_get_thread_kill_signal,
        NULL,
        "Are threads signalled for kill?",
        NULL
    },
    {
        "wave_counter",
        (getter)PyNetwork_get_wave_counter,
        NULL,
        "Holds the integer value of how many waves executed "
        "throughout the network",
        NULL
    },
    {
        "fire_counter",
        (getter)PyNetwork_get_fire_counter,
        NULL,
        "Holds the integer value of how many "
        "neurons fired during the training",
        NULL
    },
    {
        "output",
        (getter)PyNetwork_get_output,
        NULL,
        "Shows the output of the neural network",
        NULL
    },
    {
        "neurons",
        (getter)PyNetwork_get_neurons,
        NULL,
        "Holds the neurons of the neural network",
        NULL
    },
    {
        "sensory_neurons",
        (getter)PyNetwork_get_sensory_neurons,
        NULL,
        "Holds the sensory neurons of the neural network",
        NULL
    },
    {
        "motor_neurons",
        (getter)PyNetwork_get_motor_neurons,
        NULL,
        "Holds the motor neurons of the neural network",
        NULL
    },
    {
        "interneurons",
        (getter)PyNetwork_get_interneurons,
        NULL,
        "Holds the interneurons of the neural network",
        NULL
    },
    {
        "nonsensory_neurons",
        (getter)PyNetwork_get_nonsensory_neurons,
        NULL,
        "Holds the nonsensory neurons of the neural network",
        NULL
    },
    {
        "nonmotor_neurons",
        (getter)PyNetwork_get_nonmotor_neurons,
        NULL,
        "Holds the nonmotor neurons of the neural network",
        NULL
    },
    {NULL}  /* Sentinel */
};

static PyGetSetDef PyNeuron_getseters[] = {
    {
        "desired_potential",
        (getter)PyNeuron_get_desired_potential,
        NULL,
        "Desired potential of the neuron",
        NULL
    },
    {
        "loss",
        (getter)PyNeuron_get_loss,
        NULL,
        "Loss of the neuron",
        NULL
    },
    {
        "fire_counter",
        (getter)PyNeuron_get_fire_counter,
        NULL,
        "Fire counter of the neuron",
        NULL
    },
    {
        "index",
        (getter)PyNeuron_get_index,
        (setter)PyNeuron_set_index,
        "Index of the neuron inside the network",
        NULL
    },
    {
        "potential",
        (getter)PyNeuron_get_potential,
        NULL,
        "Potential of the neuron",
        NULL
    },
    {
        "type",
        (getter)PyNeuron_get_type,
        NULL,
        "Type of the neuron",
        NULL
    },
    {
        "ban_counter",
        (getter)PyNeuron_get_ban_counter,
        NULL,
        "Ban counter of the neuron",
        NULL
    },
    {
        "position",
        (getter)PyNeuron_get_position,
        (setter)PyNeuron_set_position,
        "Position(imaginary) of the neuron",
        NULL
    },
    {
        "subscriptions",
        (getter)PyNeuron_get_subscriptions,
        NULL,
        "Holds the subscriptions of the neuron",
        NULL
    },
    {
        "publications",
        (getter)PyNeuron_get_publications,
        NULL,
        "Holds the publications of the neuron",
        NULL
    },
    {NULL}  /* Sentinel */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "cplexus",          /* name of module */
    "",                 /* module documentation, may be NULL */
    -1,                 /* size of per-interpreter state of the module, or
                           -1 if the module keeps state in global variables. */
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_cplexus(void) /* create the module */
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
    PyNeuronType.tp_getset=PyNeuron_getseters;
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

    /* Add Network object to the module */
    PyModule_AddObject(m, "Network", (PyObject *)&PyNetworkType);
    /* Add Neuron object to the module */
    PyModule_AddObject(m, "Neuron", (PyObject *)&PyNeuronType);
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
