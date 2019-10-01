#include <Python.h>
#include <stdexcept>

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
} PyNetwork;

static int PyNetwork_init(PyNetwork *self, PyObject *args, PyObject *kwargs)
// initialize PyNetwork Object
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

    if (! PyArg_ParseTupleAndKeywords(args, kwargs, "i|iiidipppd", kwlist, &size, &input_dim, &output_dim, &connectivity, &precision, &randomly_fire, &dynamic_output, &visualization, &decay_factor))
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

static PyObject * PyNetwork_load(PyNetwork* self, PyObject* args, PyObject *kwargs)
{
    std::vector<double> input_arr;
    std::vector<double> output_arr;
    PyObject *input_obj;
    PyObject *output_obj;

    if (! PyArg_ParseTuple(args, "OO", &input_obj, &output_obj))
        throw std::invalid_argument("Wrong type of argument");

    PyObject *input_iter = PyObject_GetIter(input_obj);
    PyObject *output_iter = PyObject_GetIter(output_obj);
    if (!input_iter || !output_iter) {
        throw std::invalid_argument("One of the arguments is not iterable");
    }

    parse_iterable(input_arr, input_iter);
    parse_iterable(output_arr, output_iter);

    (self->ptrObj)->load(input_arr, output_arr);
    return Py_BuildValue("");
}

static PyMethodDef PyNetwork_methods[] = {
    {"load", (PyCFunction)PyNetwork_load, METH_VARARGS, "Load input and ouput the neural network" },
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
