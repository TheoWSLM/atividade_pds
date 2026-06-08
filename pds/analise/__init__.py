"""
Pacote de análise — comparação e geração de relatórios.
"""

from .transformadas.resultado_comparacao import ResultadoComparacao
from .transformadas.comparador_algoritmos import ComparadorAlgoritmos
from .transformadas.gerador_relatorio import GeradorRelatorio

__all__ = [
    "ComparadorAlgoritmos",
    "ResultadoComparacao",
    "GeradorRelatorio",
]
