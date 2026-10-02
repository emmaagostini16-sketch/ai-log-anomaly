import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# Cantidad de registros
NORMAL_RECORDS = 10000
ANOMALOUS_RECORDS = 500

# Rutas habituales
NORMAL_PATHS = [
    "/",
    "/home",
    "/products",
    "/product/1",
    "/product/2",
    "/login",
    "/cart",
    "/checkout",
    "/contact"
]

# Métodos habituales
NORMAL_METHODS = ["GET", "GET", "GET", "GET", "POST"]

# Códigos HTTP habituales
NORMAL_STATUS_CODES = [200, 200, 200, 200, 201, 204]

# Rutas asociadas a comportamiento sospechoso
ANOMALOUS_PATHS = [
    "/admin",
    "/wp-admin",
    "/etc/passwd",
    "/.env",
    "/config.php"
]


def generate_normal_record(timestamp):
    """Genera un registro de acceso normal."""

    ip = f"192.168.1.{random.randint(10, 50)}"
    method = random.choice(NORMAL_METHODS)
    path = random.choice(NORMAL_PATHS)
    status = random.choice(NORMAL_STATUS_CODES)

    # Tiempo de respuesta normal: 50-300 ms
    response_time = random.randint(50, 300)

    return [
        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        ip,
        method,
        path,
        status,
        response_time,
        0
    ]


def generate_anomalous_record(timestamp):
    """Genera un registro con comportamiento anómalo."""

    ip = f"10.0.0.{random.randint(100, 120)}"

    # Una anomalía puede utilizar diferentes métodos
    method = random.choice(["GET", "POST", "PUT", "DELETE"])

    path = random.choice(ANOMALOUS_PATHS)

    # Errores frecuentes en comportamiento sospechoso
    status = random.choice([401, 403, 404, 500])

    # Tiempo de respuesta artificialmente elevado
    response_time = random.randint(700, 3000)

    return [
        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        ip,
        method,
        path,
        status,
        response_time,
        1
    ]


def main():
    """Genera el dataset completo."""

    # Directorio raíz del proyecto
    project_root = Path(__file__).resolve().parent.parent

    # Directorio donde guardaremos el dataset
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    output_file = data_dir / "access_logs.csv"

    start_time = datetime(2026, 10, 1, 8, 0, 0)

    records = []

    # Generar registros normales
    current_time = start_time

    for _ in range(NORMAL_RECORDS):
        records.append(generate_normal_record(current_time))
        current_time += timedelta(seconds=random.randint(1, 30))

    # Generar registros anómalos
    for _ in range(ANOMALOUS_RECORDS):
        records.append(generate_anomalous_record(current_time))
        current_time += timedelta(seconds=random.randint(1, 10))

    # Mezclar registros para que las anomalías no estén todas juntas
    random.shuffle(records)

    # Escribir CSV
    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "timestamp",
            "ip",
            "method",
            "path",
            "status",
            "response_time",
            "label"
        ])

        writer.writerows(records)

    print(f"Dataset generado correctamente.")
    print(f"Archivo: {output_file}")
    print(f"Registros normales: {NORMAL_RECORDS}")
    print(f"Registros anómalos: {ANOMALOUS_RECORDS}")
    print(f"Total de registros: {len(records)}")


if __name__ == "__main__":
    main()