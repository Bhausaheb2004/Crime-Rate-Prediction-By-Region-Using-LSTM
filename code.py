# ============================================
# CRIME RATE PREDICTION BY REGION USING LSTM
# ============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# =========================
# 1️⃣ Load Dataset
# =========================

df = pd.read_csv("crime_data_india.csv")

print("Available Regions:")
print(df['STATE/UT'].unique())

# =========================
# 2️⃣ Select Region
# =========================

region = input("Enter State/UT Name: ").upper()

region_df = df[df['STATE/UT'] == region]

if region_df.empty:
    print("Region not found!")
    exit()

region_df = region_df.sort_values('YEAR')

# =========================
# 3️⃣ Create TOTAL_CRIME
# =========================

region_df['TOTAL_CRIME'] = region_df.iloc[:, 2:].sum(axis=1)
region_df = region_df[['YEAR', 'TOTAL_CRIME']]
region_df.reset_index(drop=True, inplace=True)

# =========================
# 4️⃣ Scaling
# =========================

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(region_df[['TOTAL_CRIME']])

# =========================
# 5️⃣ Train-Test Split
# =========================

train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size-3:]

# =========================
# 6️⃣ Create Sequences
# =========================

def create_sequences(data, window_size=3):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(X), np.array(y)

window_size = 3

X_train, y_train = create_sequences(train_data, window_size)
X_test, y_test = create_sequences(test_data, window_size)

X_train = X_train.reshape(X_train.shape[0], window_size, 1)
X_test = X_test.reshape(X_test.shape[0], window_size, 1)

# =========================
# 7️⃣ Build LSTM Model
# =========================

model = Sequential()

model.add(LSTM(64, return_sequences=True, input_shape=(window_size,1)))
model.add(Dropout(0.2))

model.add(LSTM(32))
model.add(Dropout(0.2))

model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

# =========================
# 8️⃣ Train Model
# =========================

model.fit(X_train, y_train, epochs=150, batch_size=4,
          validation_data=(X_test, y_test))

# =========================
# 9️⃣ Predictions
# =========================

test_pred = model.predict(X_test)

test_pred = scaler.inverse_transform(test_pred)
y_test_actual = scaler.inverse_transform(y_test)

# =========================
# 🔟 Evaluation
# =========================

rmse = math.sqrt(mean_squared_error(y_test_actual, test_pred))
mae = mean_absolute_error(y_test_actual, test_pred)

print("\nModel Performance:")
print("RMSE:", rmse)
print("MAE:", mae)

# =========================
# 1️⃣1️⃣ Plot Graph
# =========================

plt.figure(figsize=(10,6))
plt.plot(region_df['YEAR'], region_df['TOTAL_CRIME'], label="Actual Crime")

test_plot = np.empty((len(scaled_data), 1))
test_plot[:] = np.nan
test_plot[train_size:] = test_pred

plt.plot(region_df['YEAR'], test_plot, label="Predicted Crime")

plt.title("Crime Prediction - " + region)
plt.xlabel("Year")
plt.ylabel("Total Crime")
plt.legend()
plt.show()

# =========================
# 1️⃣2️⃣ Future Prediction
# =========================

last_3 = scaled_data[-window_size:]
last_3 = last_3.reshape(1, window_size, 1)

future = model.predict(last_3)
future = scaler.inverse_transform(future)

print("\nNext Year Predicted Crime:", future[0][0])