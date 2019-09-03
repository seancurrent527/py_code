'''
Gradient descent implementation for neural networks.
'''

import numpy as np
from dual_numbers import DualNumber

def back_propgation(net, cost):
    pass

def mean_square_error(array, target):
    return sum((array - target)**2)

def net_error(array, target, net, error = mean_square_error):
    return error(net.traverse(array), target)

#dC/dw = dC/dN1 * (dN1/dw + dN1/dN2)
#X is constant! w is changing for grad calc

#grad(C) = [dC/dw1, dC/dw2,... dC/db, sum[dC/d_w1, dC/d_w2,... dC/d_b, sum[...]] ]
#First grad = [dC/d__w1, dC/d__w2,... dC/d__b]

def partial_traversal(X, y, net, cost, layer_num, unit_num, param_num):
    net[layer_num, unit_num].params[param_num] = DualNumber(net[layer_num, unit_num].params[param_num])
    y_out 


