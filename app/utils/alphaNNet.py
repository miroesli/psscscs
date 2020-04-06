from tensorflow import keras as ks
from numpy import array

models_fp = 'models/'


class AlphaNNet:
    
    def __init__(self, model=None, in_shape=None):
        if model:
            self.nnet = ks.models.load_model(model)
        elif in_shape:
            self.nnet = ks.Sequential([
                ks.layers.Conv2D(32, (5, 5), use_bias=False, input_shape=ins),
                ks.layers.BatchNormalization(axis=3),
                ks.layers.Activation('selu'),
                ks.layers.Conv2D(32, (3, 3), use_bias=False),
                ks.layers.BatchNormalization(axis=3),
                ks.layers.Activation('selu'),
                ks.layers.Conv2D(64, (3, 3), use_bias=False),
                ks.layers.BatchNormalization(axis=3),
                ks.layers.Activation('selu'),
                ks.layers.Conv2D(64, (3, 3), use_bias=False),
                ks.layers.BatchNormalization(axis=3),
                ks.layers.Activation('selu'),
                ks.layers.Conv2D(128,(3, 3), use_bias=False),
                ks.layers.BatchNormalization(axis=3),
                ks.layers.Activation('selu'),
                ks.layers.Conv2D(128,(3, 3), use_bias=False),
                ks.layers.BatchNormalization(axis=3),
                ks.layers.Activation('selu'),
                ks.layers.Flatten(),
                ks.layers.Dense(3),
                ks.layers.Activation('sigmoid')
            ])
            self.nnet.compile(
                optimizer = ks.optimizers.Adam(lr = 0.0005), # lr < 0.001
                loss = "categorical_crossentropy"
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
