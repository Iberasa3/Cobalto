# main.py
from ingestion import extract_and_save, TICKERS, DB_NAME


def run_pipeline():
    print("Iniciando el pipeline de datos del Nasdaq...")

    # 1. Fase de Ingesta
    print("\n--- FASE 1: INGESTA ---")
    extract_and_save(TICKERS, DB_NAME)

    # Aquí en el futuro pondremos:
    # 2. Fase de Feature Engineering
    # 3. Fase de Entrenamiento/Predicción


if __name__ == "__main__":
    run_pipeline()