from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np

def treinar_arvore(df: pd.DataFrame) -> DecisionTreeClassifier:
    """Treina a árvore de decisão para classificar o nível de alerta."""
    # Cria rótulo a partir do índice de risco
    df["nivel_alerta"] = pd.cut(
        df["indice_risco_bruto"],
        bins=[0, 15, 30, 50, np.inf],
        labels=["Verde", "Amarelo", "Laranja", "Vermelho"]
    )
    features = ["precipitacao", "umidade", "nivel_rio", "temperatura"]
    X = df[features]
    y = df["nivel_alerta"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = DecisionTreeClassifier(max_depth=5, random_state=42)
    modelo.fit(X_train, y_train)

    print(classification_report(y_test, modelo.predict(X_test)))
    print(export_text(modelo, feature_names=features))
    return modelo

def classificar_alerta(modelo: DecisionTreeClassifier, dados: dict) -> str:
    entrada = pd.DataFrame([dados])
    return modelo.predict(entrada)[0]