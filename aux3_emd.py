
import os
import sys

import pandas as pd
import scprep
import numpy as np

def print_data(marker_from, marker_to):
    print(f"From: {marker_from}")
    print(f"To: {marker_to}")

# Function to calculate EMD
#The function calculates the EMD between two distributions for each marker and stores the results in a DataFrame. The EMD measures the minimum amount of work required to transform one distribution into another, considering the distances between individual data points.
def calculate_emd(marker_list, emd_infodict, compare_from, compare_to,
                    emd_df):
    """
    Calculates Earth Mover's Distance (EMD) between two distributions for each marker in the given marker list.

    Args:
        marker_list (list): List of markers.
        emd_infodict (dict): EMD information dictionary.
        compare_from (DataFrame): Data for comparison from.
        compare_to (DataFrame): Data for comparison to.
        emd_df (DataFrame): DataFrame to store EMD results.

    Returns:
        DataFrame: Updated DataFrame with EMD results.
    """
    deprecated_string = "no_norm" #No normalisation implemented. Deprecate
    for marker in marker_list:
        emd_infodict["marker"] = marker
        emd_infodict[f"median_{deprecated_string}_arc_compare_from"
                        ] = compare_from[marker].median()
        emd_infodict[f"median_{deprecated_string}_arc_compare_to"
                        ] = compare_to[marker].median()
        emd_infodict[f"median_diff_{deprecated_string}_arc_compare_from_vs_to"
                        ] = compare_from[marker].median() - compare_to[
                                                            marker].median()

        if compare_from[marker].empty or compare_to[marker].empty:
            print(f"One of the arrays is empty for marker {marker}.")
            print_data(compare_from[marker], compare_to[marker])
            exit()
        # if len(compare_from[marker]) != len(compare_to[marker]):
        #     print(f"The arrays have different lengths for marker {marker}.")
        #     print_data(compare_from[marker], compare_to[marker])
        #     exit()
        if np.any(np.isnan(compare_from[marker])) or np.any(np.isnan(compare_to[marker])):
            print(f"One of the arrays contains NaN values for marker {marker}.")
            nan_rows_from = np.where(np.isnan(compare_from).any(axis=1))[0]
            print("Rows in FROM with NaN values:", nan_rows_from)
            nan_rows_to = np.where(np.isnan(compare_to).any(axis=1))[0]
            print("Rows in FROM with NaN values:", nan_rows_to)
            # print_data(compare_from[marker], compare_to[marker])
            exit()
        if np.any(np.isinf(compare_from[marker])) or np.any(np.isinf(compare_to[marker])):
            print(f"One of the arrays contains infinite values for marker {marker}.")
            print_data(compare_from[marker], compare_to[marker])
            exit()
        if not isinstance(compare_from[marker], (np.ndarray, list)) or not isinstance(compare_to[marker], (np.ndarray, list)):
            print(f"The arrays are not in a compatible formatfor marker {marker}.")
            print_data(compare_from[marker], compare_to[marker])
            exit()

        #As the distance calculated is a positve value, change to negative 
        # if input has smaller median than the denominator
        if (compare_from[marker].median() - compare_to[marker].median()) >= 0:
            emd_infodict[f"EMD_{deprecated_string}_arc"] = scprep.stats.EMD(
                                                        compare_from[marker],
                                                        compare_to[marker])
        else:
            emd_infodict[f"EMD_{deprecated_string}_arc"] = -scprep.stats.EMD(
                                                        compare_from[marker],
                                                        compare_to[marker])
        #Add EMD score to the output dataframe
        emd_df = pd.concat([emd_df, pd.DataFrame([emd_infodict])], ignore_index=True)
    
    return emd_df
