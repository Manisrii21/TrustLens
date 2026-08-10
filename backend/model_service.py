import joblib
import os


class ModelService:
    def __init__(self):
        model_path = os.path.join("models", "phishing_model.pkl")
        self.model = joblib.load(model_path)

    def predict(self, features):
        prediction = self.model.predict(features)
        probability = self.model.predict_proba(features)

        return prediction, probability


# Singleton instance
model_service = ModelService()