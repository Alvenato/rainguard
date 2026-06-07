from src.camada1_coleta.collectors import carregar_dados_simulados
from src.camada2_processamento.preprocessing import limpar_dados, engenharia_atributos
from src.camada3_ia.kmeans_clustering import agrupar_regioes
from src.camada3_ia.fuzzy_logic import criar_sistema_fuzzy, calcular_risco_fuzzy
from src.camada3_ia.decision_tree import treinar_arvore, classificar_alerta
from src.camada3_ia.cbr import SistemaCBR
from src.camada4_alertas.alert_system import emitir_alerta

def main():
    # Camada 1
    df = carregar_dados_simulados()

    # Camada 2
    df = limpar_dados(df)
    df = engenharia_atributos(df)

    # Camada 3 — K-Means
    df = agrupar_regioes(df)

    # Camada 3 — Árvore de Decisão
    modelo_arvore = treinar_arvore(df)

    # Camada 3 — Fuzzy
    sim_fuzzy = criar_sistema_fuzzy()

    # Camada 3 — CBR (popula com histórico sintético)
    cbr = SistemaCBR()
    for _, row in df.head(50).iterrows():
        cbr.adicionar_caso(row.to_dict())

    # Camada 4 — Teste com um ponto novo
    ponto_novo = {"precipitacao": 150.0, "umidade": 90.0, "nivel_rio": 7.5, "temperatura": 24.0}
    alerta = classificar_alerta(modelo_arvore, ponto_novo)
    risco_fuzzy = calcular_risco_fuzzy(sim_fuzzy, ponto_novo["precipitacao"], ponto_novo["nivel_rio"])
    similares = cbr.recuperar_casos_similares(ponto_novo)

    print(f"\nÁrvore de Decisão → Nível: {alerta}")
    print(f"Lógica Fuzzy     → Risco: {risco_fuzzy}/100")
    print(f"CBR              → {len(similares)} casos similares encontrados")
    emitir_alerta("SP-001", alerta, ponto_novo)

if __name__ == "__main__":
    main()