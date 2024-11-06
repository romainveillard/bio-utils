import os
import pandas as pd

#################################################
# Declaration of constants to use in the script #
#################################################

# Specify the folder containing the CSV files
folder_path = '/Users/romain/Documents/Perso/aure/processed'

# Name of the RU channels columns
Ru_channels = ['96Ru_96Ru_(Ru96Di)',
'98Ru_98Ru_(Ru98Di)',
'99Ru_99Ru_(Ru99Di)',
'100Ru_100Ru_(Ru_100Di)',
'101Ru_101Ru_(Ru_101Di)',
'102Ru_102Ru_(Ru_102Di)',
'104Ru_104Ru_(Ru_104Di)']

# Name of the column which contains the mean of RU channels for a single cell
single_cell_RU_mean_column = 'Ru_mean'

# Columms to ignore in the normalisation
# All the metadata columns, and the "horizontal mean" column
columns_to_ignore = ['Event #', 'Time', 'Event_length', 'Width', 'Residual', 'Residual', single_cell_RU_mean_column]

#################################################
# Function to normalise the RU channels first,  #
# using the mean values computed from all files #
#################################################
def normalise_ru_channels(events, ru_means):
    events[Ru_channels] = events[Ru_channels].div(ru_means)


##########################################
# Function to correct all the values by  #
# the mean of the normalised Ru Channels #
##########################################
def correct_values_by_mean(events):
    # Store the mean of all RU channels for each single cell ('axis=1') in a new column
    events.insert(9, single_cell_RU_mean_column, events[Ru_channels].mean(axis = 1))
    
    # DEBUG: Print how many rows will be filtered out along with their respective Ru_mean value
    print(len(events[events[single_cell_RU_mean_column] <= 0.01]))
    print(events[events[single_cell_RU_mean_column] <= 0.01])

    # Filter out any cell where the RU mean column is <= 0.01 to avoid distorting the data
    events = events[events[single_cell_RU_mean_column] > 0.01]

    # Separate the columns to normalize and the columns to leave as-is
    columns_to_normalize = events.columns.difference(columns_to_ignore)

    # Perform the normalization only on the selected columns
    # The ‘normalisation’ step is just dividing each marker by the mean of the Ruthenium channels.
    normalized_data = events[columns_to_normalize].div(events['Ru_mean'], axis=0)

    # Combine normalized and unnormalized columns, preserving original order
    return pd.concat([events[columns_to_ignore], normalized_data], axis=1)[events.columns]

##################################
# Function to normalise a single #
# file using the RU channels     #
##################################
def normalise_file(filename, ru_means):
    file_path = os.path.join(folder_path, filename)

    # Join the cleaned lines and pass them to read_csv via StringIO
    events = pd.read_csv(file_path, delimiter='\t')

    # Normalise the Ru channels
    normalise_ru_channels(events, ru_means)

    # Correct values by the Ru_mean
    events = correct_values_by_mean(events)

    # Write the normalised data to a file in the dedicated folder
    events.to_csv(normalised_folder_path + "/normalised_" + filename, index=False, sep='\t')

    print(f"Normalised file: {file_path}")


##########################################################
# Function to load all the file into a single DataFrame, #
# compute the mean for each RU channels and return them  #
##########################################################
def get_Ru_means():
    all_events = pd.DataFrame()

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            # Load the file
            events = pd.read_csv(file_path, delimiter='\t')
            # Add the data to the overall DataFrame
            all_events = pd.concat([all_events, events], ignore_index=True)
    
    # Return the mean for each RU channels
    return events[Ru_channels].mean()



############
### Main ###
############

# Create the normalised folder
normalised_folder_path = os.path.join(folder_path, "normalised")
if not os.path.exists(normalised_folder_path):
    os.makedirs(normalised_folder_path)

# Get the means to use for each file
ru_means = get_Ru_means()

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Normalise the file
        normalise_file(filename, ru_means)
        