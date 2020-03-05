import tensorflow.keras as tk
from numpy import array

class AlphaNNet:

    def __init__(self, model = None, in_shape = None):
        if model:
            self.nnet = tk.models.load_model(model)
        else:
            self.nnet = tk.models.Sequential()
            self.nnet.add(tk.layers.Flatten(input_shape = in_shape))
            self.nnet.add(tk.layers.Dense(968, activation = 'relu'))
            self.nnet.add(tk.layers.Dense(968, activation = 'relu'))
            self.nnet.add(tk.layers.Dense(4, activation = 'softmax'))
            self.nnet.compile(optimizer = 'sgd', loss = 'categorical_crossentropy')
        
    def train(self, X, Y):
        self.nnet.fit(X, Y)
    
    def eval(self, X):
        return self.nnet.predict(array([X]))
    
    def copy(self):
        return tk.models.clone_model(self.nnet)
    
    def save(self, name):
        self.nnet.save(name + '.h5')
