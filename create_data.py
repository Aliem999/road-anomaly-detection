import random
import pandas as pd

# Generate data
data = []
start_time = 0  # Start time (in milliseconds)
time_interval = .1  # Time interval between data points (in milliseconds)
distance=0
distance1=0
distance2=0
distance3=0
distance4=0


for i in range(10000): 
  
    distance4=distance3
    distance3=distance2
    distance2=distance1
    distance1=distance
    distance = random.uniform(0, 1000) # Random distance between 30 and 60
    distance=(distance+distance1+distance2+distance3+distance4)/5
    data.append((start_time, distance))
    start_time += time_interval  # Increment time by 500 milliseconds

# Create a DataFrame to display the data
df = pd.DataFrame(data, columns=['Time (s)', 'Intensity'])


# Save the data to an Excel file
output_file = 'sensor_data3.xlsx'#sensor_data2 sensor_data1
df.to_excel(output_file, index=False)

print(f"Data has been saved to the file '{output_file}'.")





