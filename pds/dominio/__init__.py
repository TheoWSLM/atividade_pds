"""
Pacote de domínio — algoritmos e tipos puros do PDS.

Exporta apenas o necessário para as camadas superiores.
"""

from .protocolo_transformada import ProtocoloTransformada
from .resultado_transformada import ResultadoTransformada
from .calculadora_dft import CalculadoraDFT
from .calculadora_fft import CalculadoraFFT
from .decomposicao_butterfly import DecomposicaoButterfly

__all__ = [
    "ProtocoloTransformada",
    "ResultadoTransformada",
    "CalculadoraDFT",
    "CalculadoraFFT",
    "DecomposicaoButterfly",
]
