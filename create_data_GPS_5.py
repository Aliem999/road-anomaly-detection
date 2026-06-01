import random
import pandas as pd

# Generate NMEA GPGGA Sentence
def generate_gpgga_sentence(time, lat, lon, altitude, satellites):
    
    
    #Parameters:
    #    time (float): Time in seconds.
    #    lat (float): Latitude in decimal degrees.
    #    lon (float): Longitude in decimal degrees.
    #    altitude (float): Altitude in meters.
    #    satellites (int): Number of satellites used.
    
    #Returns:
    #    str: A formatted NMEA GPGGA sentence.
  
    time_str = f"{int(time // 3600):02}{int((time % 3600) // 60):02}{int(time % 60):02}.{int((time * 10) % 10)}"
    lat_deg = int(abs(lat))
    lat_min = (abs(lat) - lat_deg) * 60
    lat_dir = "N" if lat >= 0 else "S"
    lon_deg = int(abs(lon))
    lon_min = (abs(lon) - lon_deg) * 60
    lon_dir = "E" if lon >= 0 else "W"
    hdop = round(random.uniform(0.5, 2.0), 1)
    geoid_sep = round(random.uniform(20, 50), 1)
    return f"$GPGGA,{time_str},{lat_deg}{lat_min:.3f},{lat_dir},{lon_deg}{lon_min:.3f},{lon_dir},1,{satellites},{hdop},{altitude},M,{geoid_sep},M,,*"

# Generate data
data = []
start_time = 0  # Start time in seconds
time_interval = 0.1  # Time interval between records

for i in range(10000):
    latitude = round(random.uniform(-90, 90), 6)
    longitude = round(random.uniform(-180, 180), 6)
    altitude = round(random.uniform(0, 1000), 2)
    satellites = random.randint(4, 12)  # Number of satellites (4 to 12 typical for GPS)
    gpgga_sentence = generate_gpgga_sentence(start_time, latitude, longitude, altitude, satellites)
    
    data.append((start_time, latitude, longitude, altitude, satellites, gpgga_sentence))
    start_time += time_interval  # Increment time

# Create DataFrame
df = pd.DataFrame(data, columns=['Time (s)', 'Latitude', 'Longitude', 'Altitude (m)', 'Satellites', 'NMEA Sentence'])

# Save to Excel
output_file = 'gps_gpgga_data5.xlsx'
df.to_excel(output_file, index=False)

print(f"Data has been saved to '{output_file}' with 10,000 sequential time records.")