from tensorflow import keras as ks
from numpy import array

class AlphaNNet:

    def __init__(self, model = None, in_shape = None):
        if model:
            self.nnet = ks.models.load_model(model)
        else:
            self.nnet = ks.Sequential([
                ks.layers.Flatten(input_shape = in_shape),
                ks.layers.Dense(968, activation = 'relu'),
                ks.layers.Dense(968, activation = 'relu'),
                ks.layers.Dense(4, activation = 'softmax')
            ])
            self.nnet.compile(
                optimizer = 'sgd',
                loss = ks.losses.CategoricalCrossentropy()
            )
        
    def train(self, X, Y):
        self.nnet.fit(X, Y)
    
    def eval(self, X):
        return self.nnet.predict(array([X]))
    
    def copy(self):
        return ks.models.clone_model(self.nnet)
    
    def save(self, name):
        self.nnet.save(name + '.h5')
