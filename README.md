# Anomaly Detection Framework

## Description

This Python script is designed for detecting data quality issues in datasets by identifying anomalies within specified columns. Initially configured to use the Isolation Forest algorithm, it now supports a flexible framework that allows for the integration of multiple anomaly detection strategies, including the Local Outlier Factor (LOF) with a specific scoring threshold. This adaptability makes it especially useful for datasets where data quality issues may not be immediately apparent, enabling analysts and data scientists to quickly flag, investigate potential outliers, and assess the degree of anomalousness via score metrics.

### Purpose

- **Data Quality Assurance**: Aids in ensuring the integrity and quality of data by detecting anomalies indicative of data quality issues, offering not just binary flags but also anomaly scores for a more nuanced analysis.
- **Automated Analysis**: Enables automated analysis of multiple columns within large datasets, streamlining efficiency in data quality assessments.
- **Flexible Strategy Integration**: Facilitates the use of various anomaly detection methods, enhancing the script's applicability to diverse data characteristics and requirements. Now includes the ability to ignore zero values and use score-based thresholds for the LOF strategy.

### Restrictions

- **Data Format**: Requires the input dataset in CSV format, with each column tested for anomalies being numeric due to the numerical nature of the included and potential anomaly detection algorithms.
- **Data Distribution and Scalability**: While designed for scalability and robust against diverse data distributions, performance may vary based on the dataset's characteristics and the computational resources available.

### Ideal Use Cases

Ideal for a preliminary step in the data cleaning and preprocessing pipeline across various applications where data quality is critical. Its flexible strategy approach allows for customized anomaly detection tailored to specific data characteristics, making it versatile for financial analysis, customer data management, and more.

## Features

- **Flexible Anomaly Detection Implementation**: Supports multiple anomaly detection strategies, including Isolation Forest, Local Outlier Factor (LOF), Z-Score, and now the Interquartile Range (IQR) strategy, each with configurable parameters for efficient anomaly detection. This variety allows for tailored anomaly detection approaches to fit different dataset characteristics and anomaly detection needs.

- **Z-Score Anomaly Detection Strategy**: The newly integrated Z-Score strategy enables anomaly detection based on standard deviation from the mean. This strategy is particularly effective for datasets that approximate a normal distribution, as it identifies outliers by how many standard deviations away from the mean they are.
    ### Assumptions for Using Z-Score:
    - **Normal Distribution**: The Z-Score method assumes the data follows a normal (Gaussian) distribution. For datasets that significantly deviate from this assumption, other strategies like LOF may be more appropriate.
    - **Outlier Threshold**: A common threshold is a Z-Score of 3 or -3, identifying data points that lie beyond three standard deviations from the mean as outliers. This threshold can be adjusted based on specific analysis needs or to accommodate different levels of outlier sensitivity.
    - **Impact of Sample Size**: While the Z-Score method can be applied to datasets of any size, its reliability is higher with larger datasets. Small sample sizes may result in a biased estimation of the mean and standard deviation, affecting the accuracy of outlier detection.
    - **Sensitivity to Skewness**: The method may not perform well with skewed distributions. For datasets with significant skewness, data transformation or alternative strategies might be necessary to accurately identify outliers.

- **IQR Anomaly Detection Strategy**: Adds the ability to detect anomalies using the Interquartile Range (IQR) method, which is effective for datasets with skewed distributions or outliers. The IQR method does not assume a normal distribution, making it versatile and robust across different data types.
    ### Configuration and Assumptions for Using IQR:
    - **Multiplier Adjustment to 3**: The IQR strategy has been configured with a multiplier of 3 for identifying outliers, offering a more conservative approach that focuses on the most extreme deviations. This adjustment helps in reducing false positives in anomaly detection.
    - **Non-Parametric Approach**: Suitable for datasets that do not follow a normal distribution, leveraging the quartiles to determine outliers. This method is particularly useful for data with asymmetrical distributions.
    - **Versatility across Distributions**: The IQR strategy's reliance on quartiles rather than mean and standard deviation makes it adept at handling outliers in various distribution types, including skewed distributions.

- **Score-Based Anomaly Detection**: Incorporates anomaly scores into the final output, enabling a quantitative measure of anomalousness for each detected outlier. This feature is now extended with the inclusion of Z-Score strategy and IQR method, providing a standard measure for the degree of deviation from the norm.

- **Configurable and Extensible**: Easily extendable to include new anomaly detection algorithms by implementing the AnomalyDetectionStrategy interface. The addition of the Z-Score and IQR strategies exemplifies the framework's flexibility and adaptability to different statistical approaches for anomaly detection.

- **Summary Generation and Results Saving**: Generates a detailed summary and outputs the dataset with anomaly flags and scores, facilitating in-depth analysis and review. This comprehensive approach aids in the thorough examination of potential data quality issues, leveraging multiple strategies for a nuanced analysis.

## Example Files

- `loan_data.csv`: An example input file containing loan data for anomaly detection.
- `loan_data_anomaly.csv`: An example output file generated by the script, showcasing the detected anomalies with flags and scores.

These files serve as a practical demonstration of how the script processes input data and produces output with anomalies flagged and scored, offering insights into the effectiveness of each strategy under different data conditions.

## Usage

1. **Prepare Your Dataset**: Ensure it is in CSV format with numeric columns suitable for anomaly testing.
2. **Configure Detection Strategies** (Optional): Define or adjust anomaly detection strategies as required, now including the option to set the IQR multiplier for more conservative or liberal outlier detection.
3. **Run the Script**: Execute the script to apply the configured anomaly detection strategies to your data.
4. **Review the Output**: Analyze the summary table and the new CSV file with appended anomaly flags and scores to identify and investigate potential data quality issues.
