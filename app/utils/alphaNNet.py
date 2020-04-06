from tensorflow import keras as ks
from numpy import array
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

models_fp = 'app/models/'


class AlphaNNet:
    
    def __init__(self, 
        model='default',
        loss='categorical_crossentropy',
        in_shape=None,
        **config): 

        self.sess = tf.Session()
        self.graph = tf.get_default_graph()
        set_session(self.sess)
    #def __init__(self, model=None, in_shape=None):
        try:
            self.nnet = ks.models.load_model(models_fp + model)
            #self.graph = tf.get_default_graph()
            self.nnet._make_predict_function()
        except IOError: #file not found
            print('no model found')
            self.nnet = ks.Sequential([
                ks.layers.Conv2D(12, (3, 3), activation = 'relu', input_shape = in_shape),
                ks.layers.Flatten(),
                ks.layers.Dense(4, activation = 'softmax')
            ])
            self.nnet.compile(
                optimizer = ks.optimizers.Adam(lr = 0.0005), # lr < 0.001
                loss = loss 
            )
    
    def train(self, X, Y, ep = None, bs = None):
        self.nnet.fit(X, Y, epochs = ep, batch_size = bs)
    
    def pi(self, X):
        return self.nnet.predict(X)
    
    def copy(self):
        nnet_copy = AlphaNNet()
        nnet_copy.nnet = ks.models.clone_model(self.nnet)
        nnet_copy.nnet.build(self.nnet.layers[0].input_shape)
        nnet_copy.nnet.compile(
            optimizer = ks.optimizers.Adam(lr = 0.0005), # lr < 0.001
            loss = "categorical_crossentropy"
        )
        nnet_copy.nnet.set_weights(self.nnet.get_weights())
        return nnet_copy

    def save(self, name):
        self.nnet.save(models_fp + name + '.h5')
