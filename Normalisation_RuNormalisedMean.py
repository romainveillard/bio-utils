import os
import pandas as pd

# Specify the folder containing the CSV files and the output file name
folder_path = '/Users/romain/Documents/Perso/aure/processed'

#This is a single file containing all conditions. Files have been downloaded from Cytobank as txt files, then concatenated together using R.
Ru_channels = ['96Ru_96Ru',
'98Ru_98Ru',
'99Ru_99Ru',
'100Ru_100Ru',
'101Ru_101Ru',
'102Ru_102Ru',
'104Ru_104Ru']

# columns_to_ignore = ['Cell_Index', 'Ru_mean'] + Ru_channels
columns_to_ignore = ['Cell_Index', 'Ru_mean']

# Function to normalise the RU channels first
def normalise_ru_channels(events):
    ru_means = events[Ru_channels].mean()
    events[Ru_channels] = events[Ru_channels].div(ru_means)


# Function to correct all the values by the mean of the normalised Ru Channels
def correct_values_by_mean(events):
    #Insert a column into the table the the mean Ruthenium). Note that Lucy says whilst you’re supposed to use all 7 channels, she only uses Ru100 and 101 - I think these are the most abundant naturally occuring isotopes.
    events.insert(9, 'Ru_mean', events[Ru_channels].mean(axis = 1))
    
    # Print how many rows will be filtered out along with their respective Ru_mean value
    print(len(events[events['Ru_mean'] <= 0.01]))
    print(events[events['Ru_mean'] <= 0.01])

    #Filter out any 0 values and any really tiny values otherwise this will distort the data.
    events = events[events['Ru_mean'] > 0.01]

    # Separate the columns to normalize and the columns to leave as-is
    columns_to_normalize = events.columns.difference(columns_to_ignore)

    # Perform the normalization only on the selected columns
    # The ‘normalisation’ step is just dividing each marker by the mean of the ruthenium channels.
    normalized_data = events[columns_to_normalize].div(events['Ru_mean'], axis=0)

    # Combine normalized and unnormalized columns, preserving original order
    events = pd.concat([events[columns_to_ignore], normalized_data], axis=1)[events.columns]


# Function to normalise a single file using the RU channels
def normalise_file(filename):
    file_path = os.path.join(folder_path, filename)

    # Join the cleaned lines and pass them to read_csv via StringIO
    events = pd.read_csv(file_path, delimiter='\t')

    # Normalise the Ru channels
    normalise_ru_channels(events)

    # Correct values by the Ru_mean
    correct_values_by_mean(events)

    # Write the normalised data to a file in the dedicated folder
    events.to_csv(normalised_folder_path + "/normalised_" + filename, index=False, sep='\t')

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
        