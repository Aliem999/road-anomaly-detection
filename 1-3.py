import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Load the dataset 
file_path = 'sensor_data3.xlsx'
df = pd.read_excel(file_path)

# Fit ARIMA model and detect anomalies
def detect_anomalies_arima(df, p=5, d=1, q=5, threshold_factor=1.4):
    # Fit  model
    model = ARIMA(df['Intensity'], order=(p, d, q))
    model_fit = model.fit()
    
    # Get predicted values
    df['Predicted'] = model_fit.predict(start=0, end=len(df)-1, dynamic=False)
    
    # Calculate difference between actual and predicted values
    df['Residuals'] = df['Intensity'] - df['Predicted']
    
    # Use standard deviation of residuals as dynamic threshold
    std_residual = df['Residuals'].std()
    threshold = std_residual * threshold_factor
    
    # Identify anomalies based on dynamic threshold
    df['Anomaly'] = df['Residuals'].apply(lambda x: 1 if abs(x) > threshold else 0)
    
    
    anomalies = df[df['Anomaly'] == 1]
    
    return anomalies, df

# Detect anomalies
anomalies, df_with_predictions = detect_anomalies_arima(df)

# Display anomalies
#print("Detected Anomalies:")
#print(anomalies)

# Create subplots to display original data, predicted data, and anomalies
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

# Plot the original data
axes[0].plot(df['Time (s)'], df['Intensity'], label="Original Data", color='blue')
axes[0].set_title('\nOriginal Data')
axes[0].set_xlabel('Time (s)\n\n\n')
axes[0].set_ylabel('Intensity')
axes[0].legend()

# Plot the predicted data
axes[1].plot(df['Time (s)'], df['Predicted'], label="Predicted Data", color='green', linestyle='--')
axes[1].set_title('\nPredicted Data (ARIMA)')
axes[1].set_xlabel('Time (s)\n\n')
axes[1].set_ylabel('Predicted Intensity')
axes[1].legend()

# Plot anomalies
axes[2].plot(df['Time (s)'], df['Intensity'], label="Original Data", color='blue', alpha=0.7)
axes[2].scatter(anomalies['Time (s)'], anomalies['Intensity'], color='red', label="Anomalies", zorder=5)
axes[2].set_title('\nAnomalies Detected')
axes[2].set_xlabel('Time (s)\n\n')
axes[2].set_ylabel('Intensity')
axes[2].legend()

# Show the plot
plt.tight_layout()
plt.show()

# Save anomalies 
anomalies.to_excel('detected_anomalies_1-3.xlsx', index=False)
print(f"Anomalies detected and saved to 'detected_anomalies1-3.xlsx'")
