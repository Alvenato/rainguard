import pandas as pd
import numpy as np
from loguru import logger

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicatas, trata nulos e garante tipos corretos."""
    df = df.drop_duplicates()
    df["precipitacao"] = pd.to_numeric(df["precipitacao"], errors="coerce")
    df["nivel_rio"]    = pd.to_numeric(df["nivel_rio"],    errors="coerce")
    df["umidade"]      = pd.to_numeric(df["umidade"],      errors="coerce")
    # Preenche nulos com a mediana da coluna
    for col in ["precipitacao", "nivel_rio", "umidade", "temperatura"]:
        df[col] = df[col].fillna(df[col].median())
    logger.info(f"Dataset limpo: {len(df)} registros, {df.isnull().sum().sum()} nulos")
    return df

def engenharia_atributos(df: pd.DataFrame) -> pd.DataFrame:
    """Cria novas variáveis úteis para os modelos."""
    df["indice_risco_bruto"] = (
        df["precipitacao"] * 0.5 +
        df["nivel_rio"]    * 0.3 +
        df["umidade"]      * 0.2
    )
    df["precipitacao_norm"] = (df["precipitacao"] - df["precipitacao"].min()) / (df["precipitacao"].max() - df["precipitacao"].min())
    df["nivel_rio_norm"]    = (df["nivel_rio"]    - df["nivel_rio"].min())    / (df["nivel_rio"].max()    - df["nivel_rio"].min())
    return df