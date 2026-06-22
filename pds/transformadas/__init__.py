"""
Subpacote de transformadas espectrais (DFT e FFT).
"""

from .calculadoras import (
    ProtocoloTransformada,
    ResultadoTransformada,
    CalculadoraDFT,
    CalculadoraFFT,
)
from .decomposicao import DecomposicaoButterfly
from .analise import (
    ResultadoComparacao,
    ComparadorAlgoritmos,
    GeradorRelatorio,
)
from .visualizacao import (
    GeradorGraficos,
    ValidadorNumerico,
)

__all__ = [
    "ProtocoloTransformada",
    "ResultadoTransformada",
    "CalculadoraDFT",
    "CalculadoraFFT",
    "DecomposicaoButterfly",
    "ResultadoComparacao",
    "ComparadorAlgoritmos",
    "GeradorRelatorio",
    "GeradorGraficos",
    "ValidadorNumerico",
]
