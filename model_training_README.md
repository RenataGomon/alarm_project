data_preparation_and_model_training.ipynb is our main notebook for second stage of this project, where we:
  - Cleaned and prepared data
  - Merged all datasets: weather, air alarms, and ISW reports (TF-IDF + PCA)
  - Performed feature engineering 
  - Scaled needed data for machine learning appropriate format
  - Used TimeSeriesSplit to split data for train/test to ensure chronological consistency.
  - Trained and evaluated:
    - Linear Regression (for continuous prediction).
    - Logistic Regression (for binary classification).
  - Visualized confusion matrices, prediction distributions, feature importances.


