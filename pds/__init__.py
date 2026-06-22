"""
Pacote principal do projeto PDS (Processamento Digital de Sinais).

Expõe a API pública organizada por funcionalidades: transformadas, janelas e filtros.
"""

from .transformadas import (
    ProtocoloTransformada,
    ResultadoTransformada,
    CalculadoraDFT,
    CalculadoraFFT,
    DecomposicaoButterfly,
    ComparadorAlgoritmos,
    ResultadoComparacao,
    GeradorRelatorio,
    GeradorGraficos,
    ValidadorNumerico,
)
from .janelas import (
    ProtocoloJanela,
    JanelaRetangular,
    JanelaTriangular,
    JanelaHann,
    JanelaHamming,
    JanelaBlackman,
    GeradorSinais,
    AnalisadorJanelas,
    GeradorGraficosJanelas,
)
from .filtros import (
    FiltroFIR,
    ProjetistaFiltroFIR,
    AnalisadorFiltros,
    GeradorGraficosFiltros,
)

__all__ = [
    # Transformadas
    "ProtocoloTransformada",
    "ResultadoTransformada",
    "CalculadoraDFT",
    "CalculadoraFFT",
    "DecomposicaoButterfly",
    "ComparadorAlgoritmos",
    "ResultadoComparacao",
    "GeradorRelatorio",
    "GeradorGraficos",
    "ValidadorNumerico",
    # Janelas
    "ProtocoloJanela",
    "JanelaRetangular",
    "JanelaTriangular",
    "JanelaHann",
    "JanelaHamming",
    "JanelaBlackman",
    "GeradorSinais",
    "AnalisadorJanelas",
    "GeradorGraficosJanelas",
    # Filtros
    "FiltroFIR",
    "ProjetistaFiltroFIR",
    "AnalisadorFiltros",
    "GeradorGraficosFiltros",
]
