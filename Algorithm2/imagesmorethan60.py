# Import the pandas library for data manipulation and analysis
import pandas as pd
# Import the os module to interact with the operating system
import os
# Import the shutil module for file operations like copying
import shutil

# Load the CSV file containing data
csv_file_path = r'C:\Users\suyas\OneDrive-stevens.edu\Desktop\Applied Machine Learning\Final_Project\dataset\filtered_people.csv'  # Path to your CSV file
data = pd.read_csv(csv_file_path)  # Read the CSV file into a DataFrame

# Convert the 'images' column in the DataFrame from possibly non-integer types to integer
# Fill missing values with 0 before conversion
data['images'] = data['images'].fillna(0).astype(int)

# Filter the DataFrame to include only rows where the 'images' column has a value greater than 60
people_with_more_than_60_images = data[data['images'] > 60]

# Define the source and destination directories for file operations
source_dir = r'C:\Users\suyas\OneDrive-stevens.edu\Desktop\Applied Machine Learning\Final_Project\dataset\lfw-deepfunneled\lfw-deepfunneled'
dest_dir = r'C:\Users\suyas\OneDrive-stevens.edu\Desktop\Applied Machine Learning\Final_Project\dataset\copied2'

# Check if the destination directory exists; if not, create it
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Iterate over each person's name in the filtered DataFrame
for person in people_with_more_than_60_images['name']:
    # Construct the path to the person's folder in the source directory
    person_folder = os.path.join(source_dir, person)

    # Check if the person's folder exists in the source directory
    if os.path.exists(person_folder):
        # Construct the path to the person's folder in the destination directory
        person_dest_folder = os.path.join(dest_dir, person)
        # If the person's folder does not exist in the destination directory, create it
        if not os.path.exists(person_dest_folder):
            os.makedirs(person_dest_folder)

        # Initialize a counter to keep track of the number of images copied
        image_counter = 0

        # Copy images from the source to the destination folder
        for image in os.listdir(person_folder):
            # Copy up to 120 images .
            if image_counter < 120:
                shutil.copy(os.path.join(person_folder, image), os.path.join(person_dest_folder, image))
                image_counter += 1  # Increment the counter
            else:
                # Stop copying if 120 images have been copied
                break
