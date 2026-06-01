import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore

# Load Excel
def load_data(file_path):
    return pd.read_excel(file_path)

def plot_data(df, anomalies):
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["Time (s)"], df["Vibration"], label="Vibration Data", color='blue')
    plt.axhline(df["Vibration"].mean(), color='red', linestyle='dashed', label="Mean Vibration")  # Mean Line
    plt.scatter(anomalies["Time (s)"], anomalies["Vibration"], color='red', label="Anomalies", zorder=3)  # Anomaly points
    plt.xlabel("Time (s)")
    plt.ylabel("Vibration")
    plt.title("Vibration Over Time (Anomaly Detection)")
    plt.legend()
    plt.show()

def plot_anomalies(anomalies):
    
    plt.figure(figsize=(10, 5))
    plt.scatter(anomalies["Time (s)"], anomalies["Vibration"], color='red', label="Anomalies", zorder=3)
    plt.axhline(anomalies["Vibration"].mean(), color='black', linestyle='dashed', label="Anomaly Mean")
    plt.xlabel("Time (s)")
    plt.ylabel("Vibration")
    plt.title("Detected Anomalies Over Time")
    plt.legend()
    plt.show()

def detect_anomalies(df, threshold=2.0):
    
    df["Z-Score"] = zscore(df["Vibration"])  # Compute Z-score
    mean_value = df["Vibration"].mean()  # Compute mean
    return df[(df["Z-Score"] > threshold) & (df["Vibration"] > mean_value)]  # Filter anomalies above mean

def save_anomalies(anomalies, output_file="anomalies_1-2.xlsx"):
    
    #Save detected anomalies
  
    anomalies.to_excel(output_file, index=False)
    print(f"Anomaly records saved to '{output_file}'. Total anomalies: {len(anomalies)}")


if __name__ == "__main__":
    file_path = "sensor_data2.xlsx" 
    df = load_data(file_path)
    anomalies = detect_anomalies(df, threshold=1) 
    
    plot_data(df, anomalies)  # Plot full dataset 
    plot_anomalies(anomalies)  # Plot anomalies 
    
    save_anomalies(anomalies)
