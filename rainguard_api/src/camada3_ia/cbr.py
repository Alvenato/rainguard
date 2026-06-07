import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

class SistemaCBR:
    """Busca eventos históricos similares para apoiar decisões."""

    def __init__(self):
        self.base_de_casos = pd.DataFrame()

    def adicionar_caso(self, caso: dict):
        self.base_de_casos = pd.concat(
            [self.base_de_casos, pd.DataFrame([caso])],
            ignore_index=True
        )

    def calcular_similaridade(self, caso_novo: dict, caso_base: pd.Series) -> float:
        features = ["precipitacao", "umidade", "nivel_rio"]
        v1 = np.array([caso_novo[f] for f in features])
        v2 = np.array([caso_base[f] for f in features])
        d_max = np.sqrt(len(features)) * 100  # distância máxima normalizada
        return 1 - (euclidean(v1, v2) / d_max)

    def recuperar_casos_similares(self, caso_novo: dict, top_k: int = 3) -> pd.DataFrame:
        if self.base_de_casos.empty:
            return pd.DataFrame()
        self.base_de_casos["similaridade"] = self.base_de_casos.apply(
            lambda row: self.calcular_similaridade(caso_novo, row), axis=1
        )
        return self.base_de_casos.nlargest(top_k, "similaridade")