from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

def agrupar_regioes(df: pd.DataFrame, k: int = 4) -> pd.DataFrame:
    """Agrupa regiões por perfil de risco ambiental."""
    features = ["precipitacao", "umidade", "nivel_rio", "temperatura"]
    X = df[features].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster"] = modelo.fit_predict(X_scaled)

    # Rotula clusters do mais ao menos arriscado
    medias = df.groupby("cluster")["indice_risco_bruto"].mean().sort_values(ascending=False)
    labels = {cluster: f"Risco {['Crítico','Alto','Médio','Baixo'][i]}" for i, cluster in enumerate(medias.index)}
    df["cluster_label"] = df["cluster"].map(labels)
    return df