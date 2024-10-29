import os
import pandas as pd
import numpy as np

# Specify the folder containing the CSV files and the output file name
folder_path = '/Users/romain/Documents/Perso/aure/processed'

#This is a single file containing all conditions. Files have been downloaded from Cytobank as txt files, then concatenated together using R.
normalisation_channel = '165Ho_AlexaFluor488'

columns_to_ignore = ['Cell_Index', normalisation_channel]

def normalise_file(filename):
    file_path = os.path.join(folder_path, filename)

    # Read the file
    events = pd.read_csv(file_path, delimiter='\t')

    # X-Normalise the channel (Min-max normalization)
    data_min = events[normalisation_channel].min()
    data_max = events[normalisation_channel].max()
    events[normalisation_channel] = events[normalisation_channel].map(lambda x: (x - data_min) / (data_max - data_min))

    # Separate the columns to normalize and the columns to leave as-is
    columns_to_normalize = events.columns.difference(columns_to_ignore)

    # Perform the normalization only on the selected columns
    # The ‘normalisation’ step is just dividing each marker by the x-normalised channel.
    normalized_data = events[columns_to_normalize].div(events[normalisation_channel], axis=0)

    # Combine normalized and unnormalized columns, preserving original order
    data_normed = pd.concat([events[columns_to_ignore], normalized_data], axis=1)[events.columns]

    # Filter to keep only rows with all finite values
    data_normed = data_normed[np.isfinite(data_normed).all(axis=1)]

    # Write the normalised data to a file in the dedicated folder
    data_normed.to_csv(normalised_folder_path + "/normalised_" + filename, index=False, sep='\t')

    print(f"Normalised file: {file_path}")


# Create the normalised folder
normalised_folder_path = os.path.join(folder_path, "normalised")
if not os.path.exists(normalised_folder_path):
    os.makedirs(normalised_folder_path)

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Normalise the file
        normalise_file(filename)
        