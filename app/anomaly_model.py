import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


class AnomalyDetectionModel:

    def __init__(self):
        self.pipeline = None

    def build_pipeline(self):
        categorical_features = [
            "method",
            "path"
        ]

        numeric_features = [
            "status",
            "response_time",
            "is_error",
            "is_sensitive_path"
        ]

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore"),
                    categorical_features
                ),
                (
                    "numeric",
                    "passthrough",
                    numeric_features
                )
            ]
        )

        model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

        self.pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model)
            ]
        )

    def prepare_features(self, df):
        data = df.copy()

        sensitive_paths = [
            "/admin",
            "/wp-admin",
            "/etc/passwd",
            "/.env",
            "/config.php"
        ]

        data["is_error"] = (
            data["status"] >= 400
        ).astype(int)

        data["is_sensitive_path"] = (
            data["path"].isin(sensitive_paths)
        ).astype(int)

        return data[
            [
                "method",
                "path",
                "status",
                "response_time",
                "is_error",
                "is_sensitive_path"
            ]
        ]

    def train(self, df):
        self.build_pipeline()

        features = self.prepare_features(df)

        self.pipeline.fit(features)

        return self

    def predict(self, df):
        if self.pipeline is None:
            raise RuntimeError(
                "El modelo no ha sido entrenado."
            )

        features = self.prepare_features(df)

        return self.pipeline.predict(features)