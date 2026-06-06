import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import sys
import os

if __name__ == "__main__":
    # 1. Tangkap parameter dinamis yang dikirim oleh file MLproject (sys.argv)
    n_estimators = int(sys.argv[1]) if len(sys.argv) > 1 else 505
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 35
    dataset_name = sys.argv[3] if len(sys.argv) > 3 else "train_pca.csv"

    # 2. Muat dataset berdasarkan parameter dinamis
    if os.path.exists(dataset_name):
        data = pd.read_csv(dataset_name)
    else:
        raise FileNotFoundError(f"File {dataset_name} tidak ditemukan!")

    X = data.drop("Credit_Score", axis=1)
    y = data["Credit_Score"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)
    input_example = X_train[0:5]

    # 3. JALANKAN TRICK UTAMA: Jangan panggil mlflow.start_run() lagi!
    # Karena 'mlflow run' sudah otomatis membuka run, kita langsung pakai fungsinya.
    mlflow.autolog()

    # Latiha model menggunakan parameter dinamis dari CLI
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    # Hitung akurasi
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    # Simpan model ke artifact
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        input_example=input_example
    )

    print(f"✅ Sukses melatih model! Estimators: {n_estimators}, Depth: {max_depth}, Accuracy: {accuracy:.4f}")