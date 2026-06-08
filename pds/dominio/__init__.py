"""
Pacote de domínio — algoritmos e tipos puros do PDS.

Exporta apenas o necessário para as camadas superiores.
"""

from .transformadas.protocolo_transformada import ProtocoloTransformada
from .transformadas.resultado_transformada import ResultadoTransformada
from .transformadas.calculadora_dft import CalculadoraDFT
from .transformadas.calculadora_fft import CalculadoraFFT
from .transformadas.decomposicao_butterfly import DecomposicaoButterfly

__all__ = [
    "ProtocoloTransformada",
    "ResultadoTransformada",
    "CalculadoraDFT",
    "CalculadoraFFT",
    "DecomposicaoButterfly",
]
