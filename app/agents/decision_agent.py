class DecisionAgent:
    """
    Agente responsable de interpretar las predicciones
    del modelo y sugerir una acción.
    """

    def decide(self, predictions):

        total_logs = len(predictions)

        if total_logs == 0:
            return {
                "threat_detected": False,
                "anomalies": 0,
                "total_logs": 0,
                "anomaly_ratio": 0.0,
                "action": "allow",
                "reason": "No logs were provided for analysis."
            }

        anomalies = int(
            (predictions == -1).sum()
        )

        anomaly_ratio = anomalies / total_logs

        threat_detected = anomalies > 0

        # Política de decisión
        if anomaly_ratio >= 0.50:
            action = "block"
            reason = (
                f"High anomaly ratio detected: "
                f"{anomalies} of {total_logs} logs "
                f"were classified as anomalous."
            )

        elif anomaly_ratio > 0:
            action = "alert"
            reason = (
                f"Anomalous activity detected: "
                f"{anomalies} of {total_logs} logs "
                f"were classified as anomalous."
            )

        else:
            action = "allow"
            reason = (
                "No anomalous behavior was detected "
                "in the analyzed logs."
            )

        return {
            "threat_detected": threat_detected,
            "anomalies": anomalies,
            "total_logs": total_logs,
            "anomaly_ratio": round(anomaly_ratio, 4),
            "action": action,
            "reason": reason
        }