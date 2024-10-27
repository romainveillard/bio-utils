import pandas as pd
from io import StringIO

# Read the original file and clean each line
with open("all_eventscropped.csv", "r") as file:
    cleaned_lines = [line.strip().strip('"') for line in file]

# Join the cleaned lines and pass them to read_csv via StringIO
all_events = pd.read_csv(StringIO("\n".join(cleaned_lines)), delimiter='\t')

#This is a single file containing all conditions. Files have been downloaded from Cytobank as txt files, then concatenated together using R.
Ru_channels = ['Ru96',
'Ru98',
'Ru99',
'Ru100',
'Ru101',
'Ru102',
'Ru104']

#Insert a column into the table the the mean Ruthenium). Note that Lucy says whilst you’re supposed to use all 7 channels, she only uses Ru100 and 101 - I think these are the most abundant naturally occuring isotopes.
all_events.insert(9, 'Ru_mean', all_events[Ru_channels].mean(axis = 1))
#Filter out any 0 values and any really tiny values otherwise this will distort the data.
ru_pos_events = all_events[all_events['Ru_mean'] > 0.01]

# Separate the columns to normalize and the columns to leave as-is
columns_to_leave_as_is = ['Cell_Index', 'file_identifier', 'file_origin', 'Sample_ID-Cell_Index'] + Ru_channels
columns_to_normalize = all_events.columns.difference(columns_to_leave_as_is)

# Perform the normalization only on the selected columns
# The ‘normalisation’ step is just dividing each marker by the mean of the ruthenium channels.
normalized_data = all_events[columns_to_normalize].div(ru_pos_events['Ru_mean'], axis=0)

# Combine normalized and unnormalized columns, preserving original order
data_normed = pd.concat([all_events[columns_to_leave_as_is], normalized_data], axis=1)[all_events.columns]

data_normed.to_csv("data_normed.csv", index=False, sep='\t')