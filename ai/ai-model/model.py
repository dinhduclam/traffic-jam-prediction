from keras import Input, Model
from keras.layers import LSTM, Dropout, Dense
from keras.optimizers.adam import Adam
from keras.regularizers import l1


# Live Data-Based Probability Estimation
class LDBPEModel(Model):
    def __init__(self, num_features, name='Live Data-Based Probability Estimation Model'):
        super.__init__(name=name)
        self.num_features = num_features

    def __call__(self, *args, **kwargs):
        inputs = Input(shape=(self.num_features,))
        x = LSTM(units=128, kernel_regularizer=l1(0.000001), return_sequences=True, recurrent_dropout=0.1)(inputs)
        x = Dropout(rate=0.2)(x)
        x = LSTM(units=128, kernel_regularizer=l1(0.000001), return_sequences=True, recurrent_dropout=0.1)(x)
        x = Dropout(rate=0.2)(x)
        x = LSTM(units=128, kernel_regularizer=l1(0.000001), recurrent_dropout=0.1)(x)
        x = Dropout(rate=0.2)(x)
        outputs = Dense(2, activation='relu')(x)

        _model = Model(inputs=inputs, outputs=outputs)
        _model.summary()

        adam = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

        _model.compile(
            optimizer=adam, loss='binary_crossentropy', metrics=['accuracy']
        )

        return _model


# Historical Data-Based Probability Estimation
class HDBPEModel(Model):
    def __init__(self, num_features, name='Historical Data-Based Probability Estimation Model'):
        super.__init__(name=name)
        self.num_features = num_features

    def __call__(self, *args, **kwargs):
        inputs = Input(shape=(self.num_features,))
        x = Dense(128, activation='relu', kernel_regularizer=l1(0.000001))(inputs)
        x = Dropout(rate=0.2)(x)
        x = Dense(64, activation='relu', kernel_regularizer=l1(0.000001))(x)
        x = Dropout(rate=0.2)(x)
        outputs = Dense(2, activation='relu')(x)

        _model = Model(inputs=inputs, outputs=outputs)
        _model.summary()

        adam = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

        _model.compile(
            optimizer=adam, loss='binary_crossentropy', metrics=['accuracy']
        )

        return _model
