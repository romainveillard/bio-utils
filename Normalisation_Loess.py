import os
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Specify the folder containing the CSV files and the output file name
folder_path = '/Users/romain/Documents/Perso/aure/samples'

#This is a single file containing all conditions. Files have been downloaded from Cytobank as txt files, then concatenated together using R.
normalisation_channel = '165Ho_AlexaFluor488'

columns_to_ignore = ['Cell_Index', normalisation_channel]

def normalise_file(filename):
    file_path = os.path.join(folder_path, filename)

    # Read the file
    events = pd.read_csv(file_path, delimiter='\t')

    # Separate the columns to normalize and the columns to leave as-is
    columns_to_normalize = events.columns.difference(columns_to_ignore).tolist()

    # Apply Loess correction to each marker column
    for marker in columns_to_normalize:
        # cytof_data[f'Corrected_{marker}'] = apply_loess_correction(cytof_data[marker], cytof_data['WGA'])
        events[marker] = apply_loess_correction(events[marker], events[normalisation_channel])

    # # Perform the normalization only on the selected columns
    # # The ‘normalisation’ step is just dividing each marker by the x-normalised channel.
    # normalized_data = events[columns_to_normalize].div(events[normalisation_channel], axis=0)

    # # Combine normalized and unnormalized columns, preserving original order
    # data_normed = pd.concat([events[columns_to_ignore], normalized_data], axis=1)[events.columns]

    # Filter to keep only rows with all finite values
    data_normed = events[np.isfinite(events).all(axis=1)]

    # Write the normalised data to a file in the dedicated folder
    data_normed.to_csv(normalised_folder_path + "/normalised_" + filename, index=False, sep='\t')

    print(f"Normalised file: {file_path}")


# Advantages of Loess-Based Correction
#
# ✅ Handles Non-Linearity: No assumption about the functional form of the relationship.
# ✅ Data-Driven Approach: Adapts to trends within the dataset.
# ✅ Preserves Biological Signal: Corrects only for size effects without distorting underlying biological differences.
#
# Challenges & Considerations
#
# ⚠ Computational Cost: Loess smoothing can be slow for large datasets.
# ⚠ Choosing the Smoothing Parameter (span or frac): Needs tuning to avoid overfitting or underfitting.
# ⚠ Boundary Effects: Can be unstable at extreme values of WGA.
def apply_loess_correction(maker_data, wga_data):
    # Fit Loess model
    lowess_fit = sm.nonparametric.lowess(maker_data, wga_data, frac=0.5)

    # Interpolating fitted values
    # - Column 0 (lowess_fit[:, 0]): The independent variable values (e.g., WGA, the size marker). | WGA values (sorted).
	# - Column 1 (lowess_fit[:, 1]): The corresponding smoothed (Loess-fitted) dependent variable values (e.g., marker intensity). | Loess-smoothed marker intensity values.
    fitted_values = np.interp(wga_data, lowess_fit[:, 0], lowess_fit[:, 1])

    # Return the corrected data
    return maker_data / fitted_values

# Create the normalised folder
normalised_folder_path = os.path.join(folder_path, "normalised")
if not os.path.exists(normalised_folder_path):
    os.makedirs(normalised_folder_path)


# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Normalise the file
        normalise_file(filename)


def apply_loess_correction(maker_data, wga_data):
    lowess_fit = sm.nonparametric.lowess(maker_data, wga_data, frac=0.5)
    fitted_values = np.interp(wga_data, lowess_fit[:, 0], lowess_fit[:, 1])
    return maker_data / fitted_values