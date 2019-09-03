#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    PyObject * datum;
    PyObject * left;
    PyObject * right;
    PyObject * parent;
} Node;

static void Node_dealloc(Node * self)
{
    Py_XDECREF(self->datum);
    Py_XDECREF(self->left);
    Py_XDECREF(self->right);
    Py_XDECREF(self->parent);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject * Node_new(PyTypeObject * type, PyObject * args, PyObject * kwds)
{
    Node * self;
    self = (Node *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->datum = Py_None;
        if (self->datum == NULL){
            Py_DECREF(self);
            return NULL;
        }
        self->left = Py_None;
        self->right = Py_None;
        self->parent = Py_None;
    }
    return (PyObject *) self;
}

static int Node_init(Node * self, PyObject * args, PyObject * kwds)
{
    static char *kwlist[] = {"datum", NULL};
    PyObject *datum = NULL, *tmp;

    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &datum))
        return -1;
    
    if(datum){
        tmp = self->datum;
        Py_INCREF(datum);
        self->datum = datum;
        Py_XDECREF(tmp);
    }
    return 0;
}

static PyMemberDef Node_members[] = {
    {"datum", T_OBJECT_EX, offsetof(Node, datum), 0, "datum of the node"},
    {"left", T_OBJECT_EX, offsetof(Node, left), 0, "left child"},
    {"right", T_OBJECT_EX, offsetof(Node, right), 0, "right child"},
    {"parent", T_OBJECT_EX, offsetof(Node, parent), 0, "parent node"},
    {NULL}
};

static PyObject * is_leaf(Node * self)
{
    if (self->left == Py_None && self->right == Py_None) {
        return Py_True;
    }
    return Py_False;
}