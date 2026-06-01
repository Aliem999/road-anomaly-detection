import pandas as pd
import matplotlib.pyplot as plt


def detect_and_save_special_records(file_path):
    # Load the Excel 
    df = pd.read_excel(file_path)

    # Check if the required columns ('Time (s)' and 'Distance(cm)') exist
    if 'Time (s)' in df.columns and 'Distance(cm)' in df.columns:
        # List to store special records
        special_records = []
        
       # Sample 10% of the data
        sampled_df1 = df.sample(frac=0.1, random_state=42)  # random_state ensures reproducibility

       # Sort the sampled data by 'Time (s)' for better visualization
        sampled_df1 = sampled_df1.sort_values(by='Time (s)')

        # Plot the sampled data
        plt.figure(figsize=(10, 6))
        plt.plot(sampled_df1['Time (s)'], sampled_df1['Distance(cm)'], marker='o', linestyle='-', color='b')
        plt.title('Time vs Distance (10% of Data)')
        plt.xlabel('Time (s)')
        plt.ylabel('Distance (cm)')
        plt.grid(True)
        plt.show()
    
        # Iterate through the DataFrame 
        i = 2
        while i < len(df) - 2:
            curr_distance = df.loc[i, 'Distance(cm)']
            prev_distance_1 = df.loc[i - 1, 'Distance(cm)']
            prev_distance_2 = df.loc[i - 2, 'Distance(cm)']
            next_distance_1 = df.loc[i + 1, 'Distance(cm)']
            next_distance_2 = df.loc[i + 2, 'Distance(cm)']
            
            if (abs(curr_distance - prev_distance_1) >= 1 or
                abs(curr_distance - prev_distance_2) >= 1 or
                abs(curr_distance - next_distance_1) >= 1 or
                abs(curr_distance - next_distance_2) >= 1):
                special_records.append(df.loc[i])
                i += 5#if we found an hole skip two next record 
                continue
            i += 1

        # Create a new DataFrame with the special records
        special_df = pd.DataFrame(special_records, columns=['Time (s)', 'Distance(cm)'])

        # Save the special records
        special_output_file = 'special_records_1-1.xlsx'
        special_df.to_excel(special_output_file, index=False)
        print(f"Special records have been saved to the file '{special_output_file}'.")

        #Plot the special records
        plt.figure(figsize=(10, 6))
        plt.plot(special_df['Time (s)'], special_df['Distance(cm)'], marker='o', linestyle='-', color='r')
        plt.title('Special Records: Distance Differing by 1 or More Units from 1 or 2 Previous or 1 or 2 Next Records')
        plt.xlabel('Time (s)')
        plt.ylabel('Distance (cm)')
        plt.grid(True)
        plt.show()
    else:
        print("Error: The Excel file must contain 'Time (s)' and 'Distance(cm)' columns.")

file_path = 'sensor_data1.xlsx'  
detect_and_save_special_records(file_path)