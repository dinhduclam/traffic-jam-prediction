from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split

from model import LDBPEModel, HDBPEModel
from utils import read_data


def run(epochs=20, batch_size=128):
    X, y = read_data()
    num_features = X.shape[1]
    # split train test data
    X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.2, random_state=2023)

    # Create two models, namely, Live Data-Based Probability Estimation (LDBPE)
    # and Historical Data-Based Probability Estimation (HDBPE)
    live_model = LDBPEModel(num_features=num_features)
    historical_model = HDBPEModel(num_features=num_features)

    # Train Live Data-Based Probability Estimation model
    live_checkpoint_path = '../trained-model/best_live_model.model'
    live_callback = ModelCheckpoint(filepath=live_checkpoint_path,
                                    monitor='val_loss',
                                    mode='min',
                                    save_best_only=True)
    live_model.fit(X_train, y_train, epochs=epochs,
                   batch_size=batch_size, validation_split=0.1,
                   callbacks=[live_callback])

    # Historical Data-Based Probability Estimation model
    historical_checkpoint_path = '../trained-model/best_historical_model.model'
    historical_callback = ModelCheckpoint(filepath=historical_checkpoint_path,
                                          monitor='val_loss',
                                          mode='min',
                                          save_best_only=True)
    historical_model.fit(X_train, y_train, epochs=epochs,
                         batch_size=batch_size, validation_split=0.1,
                         callbacks=[historical_callback])

    # Test Model

