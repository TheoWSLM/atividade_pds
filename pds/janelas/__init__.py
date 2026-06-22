"""
Subpacote para manipulação, análise e visualização de janelas temporais.
"""

from .dominio import (
    ProtocoloJanela,
    JanelaRetangular,
    JanelaTriangular,
    JanelaHann,
    JanelaHamming,
    JanelaBlackman,
    GeradorSinais,
)
from .analise import AnalisadorJanelas
from .visualizacao import GeradorGraficosJanelas

__all__ = [
    "ProtocoloJanela",
    "JanelaRetangular",
    "JanelaTriangular",
    "JanelaHann",
    "JanelaHamming",
    "JanelaBlackman",
    "GeradorSinais",
    "AnalisadorJanelas",
    "GeradorGraficosJanelas",
]
