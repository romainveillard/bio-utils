import os
import pandas as pd

# Specify the folder containing the CSV files and the output file name
folder_path = '/Users/romain/Documents/Perso/aure/processed'

#This is a single file containing all conditions. Files have been downloaded from Cytobank as txt files, then concatenated together using R.
normalisation_channel = 'XXXXX'

columns_to_ignore = ['Cell_Index', normalisation_channel]

def normalise_file(filename):
    file_path = os.path.join(folder_path, filename)

    # Join the cleaned lines and pass them to read_csv via StringIO
    events = pd.read_csv(file_path, delimiter='\t')
    
    #Filter out any 0 values and any really tiny values otherwise this will distort the data.
    events = events[events[normalisation_channel] > 0.01]

    # Separate the columns to normalize and the columns to leave as-is
    columns_to_normalize = events.columns.difference(columns_to_ignore)

    # Perform the normalization only on the selected columns
    # The ‘normalisation’ step is just dividing each marker by the normalisation channel.
    normalized_data = events[columns_to_normalize].div(events[normalisation_channel], axis=0)

    # Combine normalized and unnormalized columns, preserving original order
    data_normed = pd.concat([events[columns_to_ignore], normalized_data], axis=1)[events.columns]

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
        