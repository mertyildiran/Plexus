#include <Python.h>
#include <iostream>

int glob_argc;
char **glob_argv;

static PyObject* hello_world(PyObject* self)
{
    std::cout << "Hello World!" << std::endl;

    Py_RETURN_NONE;
}

static PyMethodDef cplexus_funcs[] = {
    {"hello_world", (PyCFunction)hello_world, METH_VARARGS, NULL},
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
