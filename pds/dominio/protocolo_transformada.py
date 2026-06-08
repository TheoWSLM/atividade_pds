"""
Protocolo (contrato) que todas as transformadas espectrais devem seguir.

Novos algoritmos (DCT, WHT, STFT) podem ser adicionados
implementando este protocolo.
"""

from abc import ABC, abstractmethod

from .resultado_transformada import ResultadoTransformada


class ProtocoloTransformada(ABC):
    """
    Contrato mínimo que toda calculadora de transformada espectral deve cumprir.

    Expõe apenas o método público necessário:
    o consumidor não precisa conhecer detalhes internos do algoritmo.
    """

    @abstractmethod
    def calcular(self, sequencia: list[float | int]) -> ResultadoTransformada:
        """
        Calcula a transformada espectral de uma sequência discreta.

        Args:
            sequencia: Sequência de entrada x[n] com valores reais.

        Returns:
            ResultadoTransformada contendo coeficientes, magnitudes,
            fases e métricas de desempenho.
        """
        ...
