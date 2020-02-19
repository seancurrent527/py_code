import tensorflow as tf
import numpy as np

class ConCurrent(tf.keras.layers.Layer):
    def __init__(self, units, repeats,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(ConCurrent, self).__init__(**kwargs)
        assert type(units) in (int, list), "units must be a list or integer"
        if type(units) is int:
            assert repeats is not None, "if units is an integer, repeats must be specified"
            self.units = [units for _ in range(repeats)]
        else:
            self.units = units
        self.repeats = len(self.units)
        self.activation = tf.keras.activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        self.bias_initializer = tf.keras.initializers.get(bias_initializer)
        self.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        self.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        self.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)
        self.kernel_constraint = tf.keras.constraints.get(kernel_constraint)
        self.bias_constraint = tf.keras.constraints.get(bias_constraint)

    def build(self, input_shape):
        assert len(input_shape) >= 2
        self.kernels = []
        self.biases = []
        in_units = input_shape[-1]
        for i, out_units in enumerate(self.units):
            self.kernels.append(self.add_weight(name = 'kernel_' + str(i),
                                    shape = (in_units, out_units),
                                    initializer = self.kernel_initializer,
                                    regularizer = self.kernel_regularizer,
                                    constraint = self.kernel_constraint,
                                    trainable = True))
            if self.use_bias:
                self.biases.append(self.add_weight(name = 'bias_' + str(i),
                                    shape = (out_units,),
                                    initializer = self.bias_initializer,
                                    regularizer = self.bias_regularizer,
                                    constraint = self.bias_constraint,
                                    trainable = True))
            in_units = in_units + out_units
        super(ConCurrent, self).build(input_shape)

    def call(self, inputs):
        for i, kernel in enumerate(self.kernels):
            output = tf.keras.backend.dot(inputs, kernel)
            if self.use_bias:
                output = tf.keras.backend.bias_add(output, self.biases[i], data_format='channels_last')
            if self.activation is not None:
                output = self.activation(output)
            inputs = tf.keras.backend.concatenate([inputs, output])
        return inputs

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = sum(self.units) + input_shape[-1]
        return tuple(output_shape)

class Transformer(tf.keras.layers.Layer):
    def __init__(self, units, heads=1,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(Transformer, self).__init__(**kwargs)
        self.units = units
        self.heads = heads
        self.activation = tf.keras.activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = tf.keras.initializers.get(kernel_initializer)
        self.bias_initializer = tf.keras.initializers.get(bias_initializer)
        self.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)
        self.bias_regularizer = tf.keras.regularizers.get(bias_regularizer)
        self.activity_regularizer = tf.keras.regularizers.get(activity_regularizer)
        self.kernel_constraint = tf.keras.constraints.get(kernel_constraint)
        self.bias_constraint = tf.keras.constraints.get(bias_constraint)

    def build(self, input_shape):
        # (batch, timesteps, features)
        assert len(input_shape) == 3
        self.query_kernel = self.add_weight(name = 'query_kernel',
                                            shape = (input_shape[-1], self.units),
                                            initializer = self.kernel_initializer,
                                            regularizer = self.kernel_regularizer,
                                            constraint = self.kernel_constraint,
                                            trainable = True)
        self.value_kernel = self.add_weight(name = 'value_kernel',
                                            shape = (input_shape[-1], self.units),
                                            initializer = self.kernel_initializer,
                                            regularizer = self.kernel_regularizer,
                                            constraint = self.kernel_constraint,
                                            trainable = True)
        self.query_bias = self.add_weight(name = 'query_bias',
                                            shape = (self.units,),
                                            initializer = self.bias_initializer,
                                            regularizer = self.bias_regularizer,
                                            constraint = self.bias_constraint,
                                            trainable = True)
        self.value_bias = self.add_weight(name = 'value_bias',
                                            shape = (self.units,),
                                            initializer = self.bias_initializer,
                                            regularizer = self.bias_regularizer,
                                            constraint = self.bias_constraint,
                                            trainable = True)
        self.key_kernels = []
        self.key_biases = []
        for i in range(self.heads):
            self.key_kernels.append(self.add_weight(name = 'key_kernel' + str(i),
                                            shape = (input_shape[-1], self.units),
                                            initializer = self.kernel_initializer,
                                            regularizer = self.kernel_regularizer,
                                            constraint = self.kernel_constraint,
                                            trainable = True))
            self.key_biases.append(self.add_weight(name = 'key_bias' + str(i),
                                            shape = (self.units,),
                                            initializer = self.bias_initializer,
                                            regularizer = self.bias_regularizer,
                                            constraint = self.bias_constraint,
                                            trainable = True))
        self.key_converter = self.add_weight(name = 'key_converter',
                                            shape = (self.heads * self.units, self.units,),
                                            initializer = self.bias_initializer,
                                            regularizer = self.bias_regularizer,
                                            constraint = self.bias_constraint,
                                            trainable = True)

        super(Transformer, self).build(input_shape)

    def call(self, inputs):
        queries = tf.keras.backend.dot(inputs, self.query_kernel) + (self.query_bias if self.use_bias else 0)
        #Fix keys
        keys = tf.keras.backend.dot(inputs, self.key_kernel) + (self.key_bias if self.use_bias else 0)
        values = tf.keras.backend.dot(inputs, self.value_kernel) + (self.value_bias if self.use_bias else 0)
        sims = tf.keras.backend.dot(queries, tf.keras.permute_dimensions(keys, (0, 2, 1))) / np.sqrt(self.units)
        attentions = tf.keras.backend.softmax(sims, axis = -1)
        outputs = tf.keras.backend.dot(attentions, values)
        return self.activation(outputs)

    def compute_output_shape(self, input_shape):
        return input_shape[:-1] + (self.units,)