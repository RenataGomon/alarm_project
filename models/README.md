This repository contains the files necessary to train a `RandomForestClassifier` model:

- **`scaler.pkl`** – allows reproducing the exact scaling conditions required for consistent data processing in forecasting or analysis.  
- **`vectorizer.pkl`** – a serialized `TfidfVectorizer` object that was trained on a corpus of news articles about the conflict in Ukraine.  
- **`RandomForestClassifier_training.ipynb`** – performs data preparation, training of the Random Forest model for airborne alarm prediction, and visualization of the results and feature importance.  

If you want to just use our model, it's pickle file can be found and downloaded from link below:
https://drive.google.com/file/d/19APUVwHT6njwNdxKrglWWlcubNnPaPl0/view?usp=share_link
Make sure it is located in folder models and is named "RandomForest_model_1.pkl" in order for it to work correctly.

If you want to train your own model, follow this steps:
1) Make sure all required dependencies are satisfied:
  pip install -r requirements.txt
2) Make sure "merged_with_isw.csv" (available by this link https://drive.google.com/drive/folders/168yeNIt2Shsg_E7qsC8Wjd_IeLWJVNOn) is present in the directory
3) Launch Jupyter Notebook:
  jupyter notebook
4) Open the .ipynb file and run all cells.

