# Anomaly Detection with Isolation Forest

## Description

This Python script is designed for detecting data quality issues in datasets by identifying anomalies within specified columns using the Isolation Forest algorithm. It's particularly useful for datasets where data quality issues may not be immediately apparent, allowing analysts and data scientists to quickly flag and investigate potential outliers.

### Purpose

- **Data Quality Assurance**: Helps in ensuring the integrity and quality of data by detecting anomalies that could indicate data quality issues.
- **Automated Analysis**: Facilitates automated analysis of multiple columns within large datasets, improving efficiency in data quality assessments.

### Restrictions

- **Data Format**: The script requires the input dataset to be in a CSV format. Each column tested for anomalies should be numeric, as the Isolation Forest algorithm works with numerical data.
- **Data Distribution**: While the Isolation Forest algorithm is robust and generally performs well on diverse data distributions, it is important to note that extreme data distributions or highly skewed datasets might affect the detection sensitivity and specificity. Its recommended to preprocess or transform data to mitigate extreme skewness or to carefully tune the algorithm's parameters (such as `contamination`) to better suit their specific dataset characteristics.
- **Scalability**: The script is designed to be scalable and can handle multiple columns within large datasets efficiently. However, the computational time and resources required will increase with the size of the dataset and the number of columns being analyzed.

### Ideal Use Cases

This script is ideally used as a preliminary step in the data cleaning and preprocessing pipeline, allowing data practitioners to identify and address data quality issues early in the data analysis workflow. It is suitable for a wide range of applications, from financial analysis and risk assessment to customer data management and beyond, wherever data quality is paramount.

## Features

- **Isolation Forest Implementation**: Utilizes the Isolation Forest algorithm for efficient anomaly detection in data.
- **Flexible Data Processing**: Allows for anomaly detection on multiple columns of a dataset.
- **Summary Generation**: Generates a summary table detailing the anomaly detection process and outcomes for each tested column.
- **Results Saving**: Outputs the modified dataset with anomaly flags to a new CSV file for further analysis.

## Requirements

To run this script, you need Python 3.x installed along with the following packages:
- pandas
- scikit-learn
- numpy

## Usage

1. **Prepare Your Dataset**: Ensure your dataset is in a CSV format with the columns you wish to test for anomalies.
2. **Modify the Script Parameters** (Optional): Adjust the parameters such as `n_estimators`, `contamination`, and `score_threshold` in the `AnomalyDetector` class instantiation as needed.
3. **Run the Script**: Execute the script by running the following command in your terminal:

python main.py

Replace `main.py` with the path to the script if necessary.

4. **Review the Output**: The script will print a summary table to the console and save a new CSV file with the anomaly flags for each tested column. The new file name will be the original file name appended with `_anomaly`.

## Contributing

Contributions to this repository are welcome. Please follow the standard fork-pull request workflow.

- Fork the repository
- Create your feature branch (`git checkout -b feature/AmazingFeature`)
- Commit your changes (`git commit -am 'Add some AmazingFeature'`)
- Push to the branch (`git push origin feature/AmazingFeature`)
- Open a pull request

## License

Distributed under the MIT License. 

