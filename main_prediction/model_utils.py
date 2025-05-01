import datetime as dt


class TrainedModel:
    def __init__(self, model):
        self.model = model
        self.trained_at = dt.datetime.now()
        self.last_predicted_at = None

    def predict(self, X):
        self.last_predicted_at = dt.datetime.now()
        proba = self.model.predict_proba(X)[:, 1]

        preds = (proba > 0.78).astype(int)

        return preds

    def get_metadata(self):
        pred_time = self.last_predicted_at

        if pred_time:
            pred_time = self.last_predicted_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            pred_time = "no previous prediction"
        return {
            "last_model_train_time": self.trained_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "last_prediction_time": pred_time
        }