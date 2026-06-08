"""
Pacote principal do projeto PDS.

Expõe as classes públicas de todas as subcamadas.
"""

from .dominio import (
    ProtocoloTransformada,
    ResultadoTransformada,
    CalculadoraDFT,
    CalculadoraFFT,
    DecomposicaoButterfly,
)
from .analise import (
    ComparadorAlgoritmos,
    ResultadoComparacao,
    GeradorRelatorio,
)
from .visualizacao import (
    GeradorGraficos,
    ValidadorNumerico,
)

__all__ = [
    # Domínio
    "ProtocoloTransformada",
    "ResultadoTransformada",
    "CalculadoraDFT",
    "CalculadoraFFT",
    "DecomposicaoButterfly",
    # Análise
    "ComparadorAlgoritmos",
    "ResultadoComparacao",
    "GeradorRelatorio",
    # Visualização
    "GeradorGraficos",
    "ValidadorNumerico",
]
