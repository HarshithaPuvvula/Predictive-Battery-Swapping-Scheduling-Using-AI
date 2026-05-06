import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def prepare_sequences(data, window=5):
    X, y = [], []
    for i in range(len(data) - window):
        X.append(data[i:i+window])
        y.append(data[i+window])
    return np.array(X), np.array(y)

def train_lstm(arrivals):
    scaler = MinMaxScaler()
    arrivals_scaled = scaler.fit_transform(arrivals.reshape(-1, 1))

    X, y = prepare_sequences(arrivals_scaled)

    model = Sequential([
        LSTM(16, input_shape=(X.shape[1], 1)),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=10, verbose=0)

    return model, scaler

def predict_next(model, scaler, recent_arrivals):
    recent_scaled = scaler.transform(recent_arrivals.reshape(-1, 1))
    recent_scaled = recent_scaled.reshape(1, len(recent_scaled), 1)
    prediction = model.predict(recent_scaled, verbose=0)
    return int(scaler.inverse_transform(prediction)[0][0])
