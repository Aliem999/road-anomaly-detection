import cv2 
import numpy as np
import os
import pandas as pd

def calculate_mean_color(image):
    return np.mean(image, axis=(0, 1))  # Mean color (BGR) for each part

def analyze_color_by_parts(image, num_parts=40):
    h, w, _ = image.shape
    section_height = h // 8  # Dividing into 8 rows
    section_width = w // 5   # Dividing into 5 columns
    color_means = []

    for i in range(8):
        for j in range(5):
            section = image[i * section_height:(i + 1) * section_height, j * section_width:(j + 1) * section_width]
            color_means.append(calculate_mean_color(section))

    color_means = np.array(color_means)
    std_color_values = np.std(color_means, axis=0)  # Standard deviation of mean colors
    return np.any(std_color_values > 15), color_means  # Flag image if variation is high

def calculate_texture_score(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=5)
    grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=5)
    grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    return np.std(grad_magnitude)  # Standard deviation of gradients

def detect_abnormal_regions(image):
    mean_brightness = np.mean(image)
    dark_threshold = mean_brightness * 0.5
    bright_threshold = mean_brightness * 1.5
    abnormal_ratio = (np.sum(image < dark_threshold) + np.sum(image > bright_threshold)) / image.size
    return abnormal_ratio

def analyze_road_surface(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None, None, None

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    texture_score = calculate_texture_score(gray_image)
    abnormal_ratio = detect_abnormal_regions(gray_image)
    color_variation, _ = analyze_color_by_parts(image)

    return texture_score, abnormal_ratio, color_variation

def process_images(image_folder, texture_threshold=400, abnormal_ratio_threshold=0.05):
    all_data = []
    special_data = []
    color_data = []
    
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, filename)
            texture_score, abnormal_ratio, color_variation = analyze_road_surface(image_path)
            
            name, _ = os.path.splitext(filename)  # Remove file extension
            try:
                name = float(name)  # Convert filename to float
            except ValueError:
                continue  # Skip files that can't be converted to float
            
            if texture_score is not None:
                all_data.append([name, texture_score, abnormal_ratio])
            
            if texture_score is not None and texture_score > texture_threshold and abnormal_ratio > abnormal_ratio_threshold:
                special_data.append([name, texture_score, abnormal_ratio])
            
            if color_variation:
                color_data.append([name])
    
    return all_data, special_data, color_data

def save_results(all_data, special_data, color_data, output_all, output_special, output_color):
    if all_data:
        pd.DataFrame(all_data, columns=["Time (s)", "Texture Score", "Abnormal Ratio"]).to_excel(output_all, index=False)
        print(f"All images' results saved in {output_all}.")
    
    if special_data:
        pd.DataFrame(special_data, columns=["Time (s)", "Texture Score", "Abnormal Ratio"]).to_excel(output_special, index=False)
        print(f"Special images' results saved in {output_special}.")
    else:
        print("No special images met the criteria.")
    
    if color_data:
        pd.DataFrame(color_data, columns=["Time (s)"]).to_excel(output_color, index=False)
        print(f"Color analysis results saved in {output_color}.")
    else:
        print("No images with significant color variation found.")

def merge_files(file1, file2, output_file="merged.xlsx"):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    merged_df = pd.merge(df1, df2, on="Time (s)", how="inner")
    merged_df.to_excel(output_file, index=False)
    print(f"Merged file saved as '{output_file}' with {len(merged_df)} matching records.")

# Example usage:
image_folder = "road_images"
output_excel_all = "all_images1-4.xlsx"
output_excel_special = "special_images_analysis1-4.xlsx"
output_excel_color = "color_analysis1-4.xlsx"

all_data, special_data, color_data = process_images(image_folder)
save_results(all_data, special_data, color_data, output_excel_all, output_excel_special, output_excel_color)

# Merge special and color analysis files
merge_files(output_excel_special, output_excel_color, "merged_analysis1-4.xlsx")
