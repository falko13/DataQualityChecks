import pandas as pd
from sklearn.ensemble import IsolationForest
import os


class AnomalyDetector:
    """
    A class to encapsulate the anomaly detection process using the Isolation Forest algorithm.
    """

    def __init__(self, n_estimators=100, contamination='auto', score_threshold=-0.85):
        """
        Initializes the AnomalyDetector with the Isolation Forest parameters and threshold for anomaly detection.

        Parameters:
        - n_estimators: The number of base estimators in the ensemble.
        - contamination: The proportion of outliers in the data set, used to define the threshold on the scores of the samples.
        - score_threshold: The threshold for the raw scores below which a data point is considered an anomaly.
        """
        self.n_estimators = n_estimators
        self.contamination = contamination
        self.score_threshold = score_threshold
        self.models = {}  # To store the fitted models for each column.

    def fit(self, X, column_name):
        """
        Fits the Isolation Forest model for a specific column.

        Parameters:
        - X: The feature matrix.
        - column_name: The name of the column to fit the model on.
        """
        model = IsolationForest(n_estimators=self.n_estimators, contamination=self.contamination, random_state=42)
        model.fit(X)
        self.models[column_name] = model  # Store the fitted model.

    def detect_anomalies(self, X, column_name):
        """
        Detects anomalies in the data using the fitted Isolation Forest model.

        Parameters:
        - X: The feature matrix.
        - column_name: The name of the column to detect anomalies in.

        Returns:
        A boolean array where True indicates an anomaly.
        """
        model = self.models.get(column_name)
        scores = model.score_samples(X)
        return scores < self.score_threshold

    def process_column(self, df, column_name):
        """
        Processes a single column by fitting the model, detecting anomalies, and returning summary information.

        Parameters:
        - df: The DataFrame containing the data.
        - column_name: The name of the column to process.

        Returns:
        A dictionary with summary information about the anomaly detection for the column.
        """
        data = df[[column_name]].dropna()
        self.fit(data, column_name)
        anomaly_flags = self.detect_anomalies(data, column_name)
        num_anomalies = anomaly_flags.sum()

        # Update the DataFrame with anomaly flags.
        df[column_name + '_anomaly_flag'] = 0
        df.loc[data.index, column_name + '_anomaly_flag'] = anomaly_flags.astype(int)

        return {
            'Column': column_name,
            'Method': 'Isolation Forest',
            'n_estimators': self.n_estimators,
            'contamination': self.contamination,
            'Num_Anomalies': num_anomalies
        }

    def create_summary(self, df, column_names):
        """
        Creates a summary table for the anomaly detection across multiple columns.

        Parameters:
        - df: The DataFrame containing the data.
        - column_names: A list of column names to process.

        Returns:
        A DataFrame containing the summary information for each column.
        """
        summary_data = [self.process_column(df, column) for column in column_names]
        summary_df = pd.DataFrame(summary_data)
        return summary_df

    def save_results(self, df, original_csv_path, suffix="_anomaly"):
        """
        Saves the DataFrame with anomaly flags to a new CSV file.

        Parameters:
        - df: The DataFrame to save.
        - original_csv_path: The path to the original CSV file.
        - suffix: The suffix to add to the original filename for the new file.

        Returns:
        The path to the new CSV file.
        """
        file_name, file_extension = os.path.splitext(original_csv_path)
        new_csv_file_path = f"{file_name}{suffix}{file_extension}"
        df.to_csv(new_csv_file_path, index=False)  # Save DataFrame without the index.
        return new_csv_file_path


# Main function to execute the anomaly detection process.
def main():
    # Specify the path to the CSV file and the columns to be tested for anomalies.
    csv_file_path = 'loan_data.csv'
    df = pd.read_csv(csv_file_path)
    column_names = ['CoapplicantIncome', 'LoanAmount']

    # Initialize the AnomalyDetector, create a summary, and save the results.
    detector = AnomalyDetector()
    summary_table = detector.create_summary(df, column_names)
    print(summary_table)

    new_file_path = detector.save_results(df, csv_file_path)
    print(f"Updated DataFrame saved to: {new_file_path}")


if __name__ == '__main__':
    main()
