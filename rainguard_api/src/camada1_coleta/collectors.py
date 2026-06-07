import requests
import pandas as pd
from loguru import logger

def coletar_dados_inmet(estacao_id: str, data_inicio: str, data_fim: str) -> pd.DataFrame:
    """Coleta dados históricos de precipitação do INMET."""
    url = f"https://apitempo.inmet.gov.br/estacao/{data_inicio}/{data_fim}/{estacao_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        df = pd.DataFrame(dados)
        logger.info(f"Coletados {len(df)} registros da estação {estacao_id}")
        return df
    except Exception as e:
        logger.error(f"Erro ao coletar dados: {e}")
        return pd.DataFrame()

def carregar_dados_simulados() -> pd.DataFrame:
    """Gera dados simulados para desenvolvimento e testes."""
    import numpy as np
    np.random.seed(42)
    n = 500
    return pd.DataFrame({
        "regiao_id":    np.repeat(range(1, 11), 50),
        "precipitacao": np.random.exponential(scale=30, size=n),    # mm
        "umidade":      np.random.uniform(40, 100, n),              # %
        "nivel_rio":    np.random.uniform(0, 10, n),                # metros
        "temperatura":  np.random.uniform(15, 38, n),               # °C
        "latitude":     np.random.uniform(-23.5, -22.5, n),
        "longitude":    np.random.uniform(-47.5, -46.0, n),
    })