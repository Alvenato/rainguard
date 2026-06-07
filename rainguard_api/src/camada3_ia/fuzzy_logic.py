import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def criar_sistema_fuzzy():
    """Cria sistema de inferência fuzzy para classificar risco de enchente."""
    # Variáveis de entrada
    precipitacao = ctrl.Antecedent(np.arange(0, 201, 1), "precipitacao")
    nivel_rio    = ctrl.Antecedent(np.arange(0, 11, 0.1), "nivel_rio")
    # Variável de saída
    risco        = ctrl.Consequent(np.arange(0, 101, 1), "risco")

    # Funções de pertinência — precipitação
    precipitacao["baixa"]  = fuzz.trimf(precipitacao.universe, [0, 0, 50])
    precipitacao["media"]  = fuzz.trimf(precipitacao.universe, [30, 80, 130])
    precipitacao["alta"]   = fuzz.trimf(precipitacao.universe, [100, 200, 200])

    # Funções de pertinência — nível do rio
    nivel_rio["baixo"]  = fuzz.trimf(nivel_rio.universe, [0, 0, 4])
    nivel_rio["medio"]  = fuzz.trimf(nivel_rio.universe, [3, 5, 7])
    nivel_rio["alto"]   = fuzz.trimf(nivel_rio.universe, [6, 10, 10])

    # Funções de pertinência — risco de saída
    risco["baixo"]  = fuzz.trimf(risco.universe, [0, 0, 40])
    risco["medio"]  = fuzz.trimf(risco.universe, [25, 50, 75])
    risco["alto"]   = fuzz.trimf(risco.universe, [60, 100, 100])

    # Regras fuzzy
    regras = [
        ctrl.Rule(precipitacao["alta"]  & nivel_rio["alto"],  risco["alto"]),
        ctrl.Rule(precipitacao["alta"]  & nivel_rio["medio"], risco["alto"]),
        ctrl.Rule(precipitacao["media"] & nivel_rio["alto"],  risco["alto"]),
        ctrl.Rule(precipitacao["media"] & nivel_rio["medio"], risco["medio"]),
        ctrl.Rule(precipitacao["baixa"] | nivel_rio["baixo"], risco["baixo"]),
    ]

    sistema = ctrl.ControlSystem(regras)
    return ctrl.ControlSystemSimulation(sistema)

def calcular_risco_fuzzy(sim, precipitacao: float, nivel: float) -> float:
    sim.input["precipitacao"] = precipitacao
    sim.input["nivel_rio"]    = nivel
    sim.compute()
    return round(sim.output["risco"], 2)