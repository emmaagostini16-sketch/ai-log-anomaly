import pandas as pd


class LogIngestionAgent:
    """
    Agente responsable de recibir, validar y normalizar
    los registros antes de enviarlos al modelo.
    """

    REQUIRED_FIELDS = [
        "method",
        "path",
        "status",
        "response_time"
    ]

    def process(self, logs):
        if not logs:
            raise ValueError(
                "El lote de registros no puede estar vacío."
            )

        normalized_logs = []

        for index, log in enumerate(logs):

            # Validar campos obligatorios
            missing_fields = [
                field
                for field in self.REQUIRED_FIELDS
                if field not in log
            ]

            if missing_fields:
                raise ValueError(
                    f"Registro {index}: faltan campos obligatorios: "
                    f"{', '.join(missing_fields)}"
                )

            # Normalizar datos
            normalized_log = {
                "method": str(log["method"]).upper(),
                "path": str(log["path"]),
                "status": int(log["status"]),
                "response_time": float(log["response_time"])
            }

            # Validaciones básicas
            if not normalized_log["path"].startswith("/"):
                raise ValueError(
                    f"Registro {index}: path inválido."
                )

            if not 100 <= normalized_log["status"] <= 599:
                raise ValueError(
                    f"Registro {index}: status HTTP inválido."
                )

            if normalized_log["response_time"] < 0:
                raise ValueError(
                    f"Registro {index}: response_time no puede ser negativo."
                )

            normalized_logs.append(normalized_log)

        return pd.DataFrame(normalized_logs)