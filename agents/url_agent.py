from agents.url_features import extract_features
from agents.feature_extractor import extract_features as extract_ml_features
from agents.ml_agent import MLAgent


class URLAgent:

    def __init__(self):
        self.ml_agent = MLAgent()

    def analyze(self, url):

        # -----------------------------------------
        # Existing rule-based URL analysis
        # -----------------------------------------

        features = extract_features(url)

        score = 100
        reasons = []

        if not features["uses_https"]:
            score -= 30
            reasons.append(
                "Website is not using HTTPS."
            )

        if features["has_ip"]:
            score -= 25
            reasons.append(
                "IP address used instead of a domain."
            )

        if features["has_at_symbol"]:
            score -= 20
            reasons.append(
                "URL contains '@' symbol."
            )

        if features["url_length"] > 75:
            score -= 10
            reasons.append(
                "URL is unusually long."
            )

        if features["num_hyphens"] > 2:
            score -= 10
            reasons.append(
                "Too many hyphens in the domain."
            )

        # -----------------------------------------
        # ML analysis
        # -----------------------------------------

        ml_features = extract_ml_features(url)

        ml_result = self.ml_agent.predict(
            ml_features
        )

        prediction = ml_result["prediction"]
        phishing_probability = ml_result[
            "phishing_probability"
        ]

        # -----------------------------------------
        # Combine ML + security rules
        # -----------------------------------------

        if prediction == 1:

            # ML says phishing.
            # Reduce trust according to confidence.

            if phishing_probability >= 80:
                score -= 35
                reasons.append(
                    "Machine learning model detected "
                    "strong phishing indicators."
                )

            elif phishing_probability >= 50:
                score -= 20
                reasons.append(
                    "Machine learning model detected "
                    "possible phishing indicators."
                )

        # Never allow the score to go outside 0-100
        score = max(0, min(score, 100))

        # -----------------------------------------
        # Risk classification
        # -----------------------------------------

        if score >= 80:
            risk = "Low"

        elif score >= 50:
            risk = "Medium"

        else:
            risk = "High"

        # -----------------------------------------
        # Final response
        # -----------------------------------------

        return {
            "url": url,
            "risk": risk,
            "trust_score": score,
            "ml_prediction": (
                "Phishing"
                if prediction == 1
                else "Legitimate"
            ),
            "ml_phishing_probability":
                phishing_probability,
            "reasons": reasons
        }