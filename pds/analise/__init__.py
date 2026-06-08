"""
Pacote de análise — comparação e geração de relatórios.
"""

from .comparador_algoritmos import ComparadorAlgoritmos
from .resultado_comparacao import ResultadoComparacao
from .gerador_relatorio import GeradorRelatorio

__all__ = [
    "ComparadorAlgoritmos",
    "ResultadoComparacao",
    "GeradorRelatorio",
]
