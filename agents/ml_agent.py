import joblib
import pandas as pd


FEATURES = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS",
]


class MLAgent:

    def __init__(self):
        self.model = joblib.load(
            "models/phishing_url_model.pkl"
        )

    def predict(self, features):

        # Keep exactly the features used during training
        data = {
            feature: features.get(feature, 0)
            for feature in FEATURES
        }

        df = pd.DataFrame(
            [data],
            columns=FEATURES
        )

        prediction = int(
            self.model.predict(df)[0]
        )

        probabilities = self.model.predict_proba(df)[0]

        # Find the probability belonging to class 1
        class_probabilities = dict(
            zip(
                self.model.classes_,
                probabilities
            )
        )

        phishing_probability = float(
            class_probabilities.get(1, 0.0)
        )

        return {
            "prediction": prediction,
            "phishing_probability": round(
                phishing_probability * 100,
                2
            )
        }