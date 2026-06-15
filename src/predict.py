import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model


def predict_future(state, values, time_step=5, future_years=5):

    # Clean state name
    state = state.strip().replace("'", "")

    # Load model
    model_path = os.path.join("saved_models", f"{state}_lstm.h5")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found for {state}")

    model = load_model(model_path)

    # Load scaler
    scaler_path = os.path.join("saved_scalers", f"{state}_scaler.pkl")
    scaler = joblib.load(scaler_path)

    values = np.array(values).reshape(-1, 1)
    scaled_values = scaler.transform(values)

    input_seq = scaled_values[-time_step:]
    predictions = []

    for _ in range(future_years):
        input_reshaped = input_seq.reshape(1, time_step, 1)
        pred = model.predict(input_reshaped, verbose=0)
        predictions.append(pred[0][0])

        input_seq = np.append(input_seq[1:], pred)

    predictions = np.array(predictions).reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions)

    return predictions.flatten()