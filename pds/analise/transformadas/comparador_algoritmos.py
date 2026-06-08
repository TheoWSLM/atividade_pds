"""
Comparador de dois algoritmos de transformada espectral.

Orquestra a execução de duas transformadas e verifica a corretude
numérica entre elas.
"""

from pds.dominio.transformadas.protocolo_transformada import ProtocoloTransformada
from .resultado_comparacao import ResultadoComparacao


class ComparadorAlgoritmos:
    """
    Executa dois algoritmos sobre a mesma entrada e mede suas diferenças.

    Uso:
        comparador = ComparadorAlgoritmos(
            algoritmo_a=CalculadoraDFT(),
            algoritmo_b=CalculadoraFFT(),
        )
        resultado = comparador.comparar([0, 1, 2, 3])
    """

    TOLERANCIA_PADRAO = 1e-10

    def __init__(
        self,
        algoritmo_a: ProtocoloTransformada,
        algoritmo_b: ProtocoloTransformada,
        tolerancia: float = TOLERANCIA_PADRAO,
    ) -> None:
        """
        Args:
            algoritmo_a:  Primeiro algoritmo (ex: CalculadoraDFT).
            algoritmo_b:  Segundo algoritmo (ex: CalculadoraFFT).
            tolerancia:   Tolerância de ponto flutuante para verificação de corretude.
        """
        self._algoritmo_a = algoritmo_a
        self._algoritmo_b = algoritmo_b
        self._tolerancia = tolerancia

    def _coeficientes_coincidem(self, coefs_a: list[complex], coefs_b: list[complex]) -> bool:
        """
        Verifica se dois conjuntos de coeficientes são numericamente equivalentes.

        Usa comparação ponto a ponto com tolerância absoluta para
        lidar com erros de arredondamento em ponto flutuante.
        """
        if len(coefs_a) != len(coefs_b):
            return False

        return all(
            abs(coef_a - coef_b) <= self._tolerancia
            for coef_a, coef_b in zip(coefs_a, coefs_b)
        )

    def comparar(self, sequencia: list[float | int]) -> ResultadoComparacao:
        """
        Executa ambos os algoritmos e retorna as métricas comparativas.

        Args:
            sequencia: Sequência de entrada x[n].

        Returns:
            ResultadoComparacao com os resultados de ambos os algoritmos
            e a verificação de corretude.
        """
        resultado_a = self._algoritmo_a.calcular(sequencia)
        resultado_b = self._algoritmo_b.calcular(sequencia)

        coincide = self._coeficientes_coincidem(
            resultado_a.coeficientes,
            resultado_b.coeficientes,
        )

        return ResultadoComparacao(
            resultado_a=resultado_a,
            resultado_b=resultado_b,
            sequencia_original=tuple(sequencia),
            resultados_identicos=coincide,
            tolerancia_usada=self._tolerancia,
        )
