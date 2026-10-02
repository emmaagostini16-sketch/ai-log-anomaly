from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from app.anomaly_model import AnomalyDetectionModel


def main():
    project_root = Path(__file__).resolve().parent.parent

    dataset_path = project_root / "data" / "access_logs.csv"

    model_dir = project_root / "model"
    model_dir.mkdir(exist_ok=True)

    model_path = model_dir / "anomaly_model.pkl"
    test_path = model_dir / "test_data.csv"

    print("Cargando dataset...")

    df = pd.read_csv(dataset_path)

    print(f"Registros cargados: {len(df)}")

    # Separación 80% entrenamiento / 20% evaluación.
    #
    # label se utiliza solamente para mantener la proporción
    # de normales/anómalos en ambos conjuntos.
    # NO se utiliza como feature durante el entrenamiento.
    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["label"]
    )

    print()
    print("Separación del dataset")
    print("----------------------")
    print(f"Entrenamiento: {len(train_df)} registros")
    print(f"Evaluación:    {len(test_df)} registros")

    print()
    print(
        f"Anomalías en entrenamiento: "
        f"{int(train_df['label'].sum())}"
    )
    print(
        f"Anomalías en evaluación: "
        f"{int(test_df['label'].sum())}"
    )

    detector = AnomalyDetectionModel()

    print()
    print("Entrenando Isolation Forest...")

    # El modelo no recibe label como feature.
    detector.train(train_df)

    joblib.dump(detector, model_path)

    # Guardamos aparte los registros que el modelo nunca vio.
    test_df.to_csv(
        test_path,
        index=False
    )

    print()
    print(f"Modelo guardado en: {model_path}")
    print(f"Datos de evaluación guardados en: {test_path}")


if __name__ == "__main__":
    main()