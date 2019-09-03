#include <Python.h>

double factorial_calc(long n){
    double total = 1;
    if(n==0)
        return total;

    for(n; n > 0; n--){
        total = total * n;
    };
    return total;
}

static PyObject* factorial(PyObject* self, PyObject* args){
    int n;
    
    if(!PyArg_ParseTuple(args, "l", &n))
        return NULL;

    return PyLong_FromDouble(factorial_calc(n));
}

static PyObject* choose(PyObject* self, PyObject* args){
    int n;
    int k;
    if(!PyArg_ParseTuple(args, "ll", &n, &k))
        return NULL;

    return PyLong_FromDouble(factorial_calc(n) / (factorial_calc(k) * factorial_calc(n - k)));
}

static PyMethodDef MathMethods[] = {
    {"factorial", factorial, METH_VARARGS, "Calculate a factorial."},
    {"choose", choose, METH_VARARGS, "Calculate a combination."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef mathspace = {
    PyModuleDef_HEAD_INIT,
    "mathspace",
    "Mathspace module to add mathematical data structures",
    -1,
    MathMethods
};

PyMODINIT_FUNC PyInit_mathspace(void){
    return PyModule_Create(&mathspace);
}