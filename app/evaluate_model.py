from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)


def main():
    project_root = Path(__file__).resolve().parent.parent

    dataset_path = project_root / "model" / "test_data.csv"
    model_path = project_root / "model" / "anomaly_model.pkl"

    print("Cargando dataset y modelo...")

    df = pd.read_csv(dataset_path)
    model = joblib.load(model_path)

    # Etiquetas reales:
    # 0 = normal
    # 1 = anomalía
    y_true = df["label"]

    # Isolation Forest devuelve:
    #  1 = normal
    # -1 = anomalía
    raw_predictions = model.predict(df)

    # Convertimos al mismo formato de nuestras etiquetas:
    # 0 = normal
    # 1 = anomalía
    y_pred = (raw_predictions == -1).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1]
    ).ravel()

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print()
    print("Evaluación del modelo")
    print("---------------------")
    print(f"Total de registros: {len(df)}")
    print(f"Anomalías reales: {(y_true == 1).sum()}")
    print(f"Anomalías detectadas: {(y_pred == 1).sum()}")

    print()
    print("Matriz de confusión")
    print("-------------------")
    print(f"True Negatives  (TN): {tn}")
    print(f"False Positives (FP): {fp}")
    print(f"False Negatives (FN): {fn}")
    print(f"True Positives  (TP): {tp}")

    print()
    print("Métricas")
    print("--------")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")


if __name__ == "__main__":
    main()