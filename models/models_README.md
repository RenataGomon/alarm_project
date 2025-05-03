Contains files necessary to train model RandomForestClassifier:
  -scaler.pkl : allows to reproduce the exact scaling conditions required for consistent data processing in forecasting or analysis.
  -vectorizer.pkl : a serialised TfidfVectorizer object that was trained on a corpus of news articles about the conflict in Ukraine.
  -RandomForestClassifier_training.ipynb : performs data preparation, training of the Random Forest model for airborne alarm prediction, and visualisation of the results and importance of the features.
  
 To run the RandomForestClassifier_training.ipynb code:
 1) Open Terminal
 2) Clone the repository:
  git clone https://github.com/yourusername/your-repo.git
 3) Navigate to the project directory:
  cd your-repo
 4) Install the required dependencies:
  pip install -r requirements.txt
 5) Make sure "merged_with_isw.csv" (available by this link https://drive.google.com/drive/folders/168yeNIt2Shsg_E7qsC8Wjd_IeLWJVNOn) is present in the directory
 6) Launch Jupyter Notebook:
  jupyter notebook
 7) Open the .ipynb file and run all cells.
