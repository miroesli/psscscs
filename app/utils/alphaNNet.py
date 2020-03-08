from tensorflow import keras as ks
from numpy import array

class AlphaNNet:

    def __init__(self, model=None, in_shape=None):
        if model:
            self.nnet = ks.models.load_model(model)
        elif in_shape:
            self.in_shape = in_shape
            self.nnet = ks.Sequential([
                ks.layers.Flatten(input_shape = in_shape),
                ks.layers.Dense(169, activation = 'relu'),
                ks.layers.Dense(81, activation = 'relu'),
                ks.layers.Dense(81, activation = 'relu'),
                ks.layers.Dense(81, activation = 'relu'),
                ks.layers.Dense(4, activation = 'softmax')
            ])
            self.nnet.compile(
                optimizer = ks.optimizers.SGD(lr = 0.005),
                loss = "categorical_crossentropy"
            )
    
    def train(self, X, Y, epochs = 10):
        self.nnet.fit(X, Y, epochs = epochs)
    
    def pi(self, X):
        return self.nnet.predict(array(X))
    
    def copy(self):
        nnet_copy = AlphaNNet()
        nnet_copy.nnet = ks.models.clone_model(self.nnet)
        nnet_copy.nnet.build(self.nnet.layers[0].input_shape)
        nnet_copy.nnet.compile(
            optimizer = ks.optimizers.SGD(lr = 0.005),
            loss = "categorical_crossentropy"
        )
        nnet_copy.nnet.set_weights(self.nnet.get_weights())
        return nnet_copy
    
    def save(self, name):
        self.nnet.save(name + '.h5')
