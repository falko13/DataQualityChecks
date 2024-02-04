import pandas as pd
from sklearn.ensemble import IsolationForest
import os

# Strategy interface for anomaly detection to allow flexibility in the implementation of various algorithms.
class AnomalyDetectionStrategy:
    def fit(self, X):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

# Specific implementation of the Isolation Forest algorithm as a strategy.
# Allows configuring the number of estimators and contamination factor, suitable for different datasets.
class IsolationForestStrategy(AnomalyDetectionStrategy):
    def __init__(self, n_estimators=100, contamination='auto'):
        # Initialize Isolation Forest with provided parameters for flexibility.
        self.model = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=42)

    def fit(self, X):
        # Fit the model to the data. Essential for anomaly detection.
        self.model.fit(X)

    def predict(self, X):
        # Predict anomalies based on the Isolation Forest model. Uses a standard threshold to classify anomalies.
        scores = self.model.score_samples(X)
        return scores < -0.85  # Using a threshold to determine anomalies.

# AnomalyDetector class designed to work with any strategy that follows the AnomalyDetectionStrategy interface.
# This design allows adding new anomaly detection methods without changing the detector's core functionality.
class AnomalyDetector:
    def __init__(self, strategies):
        # Accepts multiple strategies for anomaly detection, enhancing modularity.
        self.strategies = strategies if isinstance(strategies, list) else [strategies]

    def process_column(self, df, column_name):
        # Processes each column with the provided strategies, enabling multiple anomaly detection approaches.
        data = df[[column_name]].dropna()
        summary_data = []

        for strategy in self.strategies:
            strategy.fit(data)
            anomaly_flags = strategy.predict(data)
            num_anomalies = anomaly_flags.sum()

            # Include strategy name in the column name for clarity on the method used.
            strategy_name = strategy.__class__.__name__
            anomaly_flag_column = f"{column_name}_anomaly_flag_{strategy_name}"

            # Mark detected anomalies in the DataFrame.
            df[anomaly_flag_column] = 0
            df.loc[data.index, anomaly_flag_column] = anomaly_flags.astype(int)

            # Compile summary data for each strategy.
            summary_data.append({
                'Column': column_name,
                'Method': strategy_name,
                'Num_Anomalies': num_anomalies
            })

        return summary_data

    def create_summary(self, df, column_names):
        # Generate a comprehensive summary across all specified columns and strategies.
        all_summary_data = []
        for column in column_names:
            column_summary = self.process_column(df, column)
            all_summary_data.extend(column_summary)
        return pd.DataFrame(all_summary_data)

    def save_results(self, df, original_csv_path, suffix="_anomaly"):
        # Save the modified DataFrame with anomaly flags to a new file, keeping the original data intact.
        file_name, file_extension = os.path.splitext(original_csv_path)
        new_csv_file_path = f"{file_name}{suffix}{file_extension}"
        df.to_csv(new_csv_file_path, index=False)

# Main function orchestrates the anomaly detection process using the specified strategies.
# Demonstrates the use of the AnomalyDetector with Isolation Forest strategy.
def main():
    csv_file_path = 'loan_data.csv'
    df = pd.read_csv(csv_file_path)
    column_names = ['CoapplicantIncome', 'LoanAmount']

    strategies = [IsolationForestStrategy(n_estimators=100, contamination='auto')]
    detector = AnomalyDetector(strategies)
    summary_table = detector.create_summary(df, column_names)
    print(summary_table)

    # Output the DataFrame with new anomaly flags, enabling further analysis.
    new_file_path = detector.save_results(df, csv_file_path)
    print(f"Updated DataFrame saved to: {new_file_path}")

if __name__ == '__main__':
    main()
