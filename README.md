
# Normalisation scripts

## Table of Contents
1. [Normalization of RU Channels Data](#normalization-of-RU-Channels-Data)

## Normalization of RU Channels Data

### Description

This script processes and normalizes data for specific channels (RU channels) from CSV files in a specified folder. It calculates a normalized mean for these channels, organizing the data for further analysis or visualization.

The method implemented in this script follows the approach described in the ["Nature Communications: Analytical Strategies"](https://www.nature.com/articles/s41467-018-03005-5#Sec15) by Burnum-Johnson et al., which introduces a robust approach for data normalization and processing in high-throughput experiments. The script leverages this method to ensure consistent normalization of RU channel data across samples.

### Prerequisites

- **Python 3.x**
- **Pandas** library

Install the required packages by running:
```bash
pip install pandas
```

### Usage

1. **Specify Folder Path**: Ensure the `folder_path` variable points to the directory containing your CSV files.
   
   ```python
   folder_path = '/path/to/your/csv/files'
   ```

2. **Define RU Channels**: The variable `Ru_channels` should list the names of the columns representing the RU channels you wish to process.

3. **Run the Script**: Execute the script by running:
   ```bash
   python Normalisation_RuNormalisedMean.py
   ```

### Output

The script processes each CSV file in the specified folder, applies normalization to the specified channels following the method referenced above, and outputs the results to the console or saves them in a specified format.

### Reference

For more details on the normalization approach, please refer to:
- Burnum-Johnson, K. E., et al. "Nature Communications: Analytical Strategies," *Nature Communications* 9, Article number: 3005 (2018). DOI: [10.1038/s41467-018-03005-5](https://www.nature.com/articles/s41467-018-03005-5#Sec15).
