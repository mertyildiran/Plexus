#include <Python.h>

#include "neuron.hpp"
#include "network.hpp"

int glob_argc;
char **glob_argv;


static PyObject* test(PyObject* self)
{
    //Network* network = new Network(14, 4, 2);
    //network->nonsensory_neurons[0]->calculate_potential();

    Py_RETURN_NONE;
}

static PyObject* hello_world(PyObject* self)
{
    std::cout << "Hello World!" << std::endl;

    Py_RETURN_NONE;
}

typedef struct {
    PyObject_HEAD
    Network * ptrObj;
} PyNetwork;

static int PyNetwork_init(PyNetwork *self, PyObject *args, PyObject *kwargs)
// initialize PyNetwork Object
{
    int size;
    int input_dim = 0;
    int output_dim = 0;
    double connectivity = 0.01;
    int precision = 2;
    bool randomly_fire = false;
    bool dynamic_output = false;
    bool visualization = false;
    double decay_factor =  1.0;

    static char *kwlist[] = {"size", "input_dim", "output_dim", "connectivity", "precision", "randomly_fire", "dynamic_output", "visualization", "decay_factor", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwargs, "i|iidipppd", kwlist, &size, &input_dim, &output_dim, &connectivity, &precision, &randomly_fire, &dynamic_output, &visualization, &decay_factor))
        return -1;

    self->ptrObj = new Network(size, input_dim, output_dim, connectivity, precision, randomly_fire, dynamic_output, visualization, decay_factor);

    return 0;
}

static void PyNetwork_dealloc(PyNetwork * self)
// destruct the object
{
    delete self->ptrObj;
    Py_TYPE(self)->tp_free(self);
}

static PyObject * PyNetwork_initiate_subscriptions(PyNetwork* self, PyObject* args)
{
    //(self->ptrObj)->initiate_subscriptions();

    return 0;
}

static PyMethodDef PyNetwork_methods[] = {
    { "initiate_subscriptions", (PyCFunction)PyNetwork_initiate_subscriptions,    METH_VARARGS,       "initiate_subscriptions the mem network" },
    {NULL}  /* Sentinel */
};

static PyTypeObject PyNetworkType = { PyVarObject_HEAD_INIT(NULL, 0)
    "plexus.Network"   /* tp_name */
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
    //~ PyNetworkType.tp_members=Noddy_members;
    PyNetworkType.tp_init=(initproc)PyNetwork_init;

    if (PyType_Ready(&PyNetworkType) < 0)
        return NULL;

    m = PyModule_Create(&moduledef);
    if (m == NULL)
        return NULL;

    Py_INCREF(&PyNetworkType);
    PyModule_AddObject(m, "Network", (PyObject *)&PyNetworkType); // Add Network object to the module
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
