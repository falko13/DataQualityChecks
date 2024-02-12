import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import os
import numpy as np


# Strategy interface for anomaly detection to allow flexibility in the implementation of various algorithms.
class AnomalyDetectionStrategy:
    def fit(self, X):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def score(self, X):
        # Method to get anomaly scores, should be implemented by each strategy.
        raise NotImplementedError


# Specific implementation of the Isolation Forest algorithm as a strategy.
class IsolationForestStrategy(AnomalyDetectionStrategy):
    def __init__(self, n_estimators=100, contamination='auto'):
        self.model = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=42)

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X):
        scores = self.model.score_samples(X)
        return scores < -0.82  # Using a threshold to determine anomalies.

    def score(self, X):
        # Return the anomaly scores directly from the model.
        return self.model.score_samples(X)


# Implementation of Local Outlier Factor (LOF) Strategy
class LocalOutlierFactorStrategy(AnomalyDetectionStrategy):
    def __init__(self, n_neighbors=20, contamination='auto'):
        self.model = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination, novelty=True)

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X):
        # Calculate the LOF scores using the negative_outlier_factor_ attribute.
        # Note: The negative_outlier_factor_ values are negative; more negative means more outlier-like.
        # We negate these values to make them positive, where higher values indicate more outlier-like.
        lof_scores = -self.model.negative_outlier_factor_  # Inverting the sign for consistency

        # Apply the threshold to determine anomalies.
        # An anomaly flag is set to 1 if the LOF score is greater than 15.
        anomaly_flags = lof_scores > 15

        return anomaly_flags

    def score(self, X):
        # Call fit again before accessing negative_outlier_factor_ as it's required for obtaining the scores.
        # This might not be the most efficient way if called after predict in a row, consider refactoring.
        self.model.fit(X)
        return -self.model.negative_outlier_factor_  # Returning the scores for use elsewhere


# Implementation of Z-Score Strategy
class ZScoreStrategy(AnomalyDetectionStrategy):
    def __init__(self, threshold=3):
        self.threshold = threshold

    def fit(self, X):
        # Z-Score fitting isn't required as it's a stateless operation, but we calculate mean and std here for efficiency.
        self.mean = np.mean(X)
        self.std = np.std(X)

    def predict(self, X):
        # Calculate Z-Scores for each data point
        z_scores = (X - self.mean) / self.std
        # Flag as anomaly if Z-Score is greater than the threshold
        anomaly_flags = np.abs(z_scores) > self.threshold
        return anomaly_flags.squeeze()  # Ensure it returns an array matching the number of rows in X

    def score(self, X):
        # Calculate and return the absolute Z-Scores as the "anomaly score"
        return np.abs((X - self.mean) / self.std).squeeze()


# AnomalyDetector class designed to work with any strategy that follows the AnomalyDetectionStrategy interface.
class AnomalyDetector:
    def __init__(self, strategies):
        self.strategies = strategies if isinstance(strategies, list) else [strategies]

    def process_column(self, df, column_name):
        # Exclude records where the column value is 0 in addition to dropping NA values.
        data = df[df[column_name] != 0][[column_name]].dropna()
        summary_data = []

        for strategy in self.strategies:
            strategy.fit(data)
            anomaly_flags = strategy.predict(data)
            anomaly_scores = strategy.score(data)  # Get anomaly scores for each data point

            num_anomalies = anomaly_flags.sum()
            strategy_name = strategy.__class__.__name__
            anomaly_flag_column = f"{column_name}_anomaly_flag_{strategy_name}"
            anomaly_score_column = f"{column_name}_anomaly_score_{strategy_name}"  # Column for anomaly scores

            df[anomaly_flag_column] = 0
            df.loc[data.index, anomaly_flag_column] = anomaly_flags.astype(int)
            df[anomaly_score_column] = 0.0  # Initialize score column
            df.loc[data.index, anomaly_score_column] = anomaly_scores  # Assign scores

            summary_data.append({
                'Column': column_name,
                'Method': strategy_name,
                'Num_Anomalies': num_anomalies
            })

        return summary_data

    def create_summary(self, df, column_names):
        all_summary_data = []
        for column in column_names:
            column_summary = self.process_column(df, column)
            all_summary_data.extend(column_summary)
        return pd.DataFrame(all_summary_data)

    def save_results(self, df, original_csv_path, suffix="_anomaly"):
        file_name, file_extension = os.path.splitext(original_csv_path)
        new_csv_file_path = f"{file_name}{suffix}{file_extension}"
        df.to_csv(new_csv_file_path, index=False)


def main():
    csv_file_path = 'loan_data.csv'
    df = pd.read_csv(csv_file_path)
    column_names = ['CoapplicantIncome', 'LoanAmount']

    # Initialize strategies
    local_outlier_factor_strategy = LocalOutlierFactorStrategy(n_neighbors=20, contamination='auto')
    isolation_forest_strategy = IsolationForestStrategy(n_estimators=100, contamination='auto')
    z_score_strategy = ZScoreStrategy(threshold=3)  # Add the ZScoreStrategy with a threshold of 3

    # Add the new ZScoreStrategy to the strategies list
    strategies = [local_outlier_factor_strategy, isolation_forest_strategy, z_score_strategy]

    detector = AnomalyDetector(strategies)
    summary_table = detector.create_summary(df, column_names)
    print(summary_table)

    new_file_path = detector.save_results(df, csv_file_path)
    print(f"Updated DataFrame saved to: {new_file_path}")


if __name__ == '__main__':
    main()
