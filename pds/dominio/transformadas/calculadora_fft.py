"""
Implementação manual da Transformada Rápida de Fourier (FFT).

Utiliza o algoritmo Cooley-Tukey com decimação no tempo (DIT),
que decompõe recursivamente a DFT de tamanho N em duas DFTs
de tamanho N/2 através da relação butterfly:

    X[k]       = X_par[k] + W_N^k · X_impar[k]
    X[k + N/2] = X_par[k] - W_N^k · X_impar[k]

onde W_N^k = e^(-j·2π·k/N) é o fator twiddle.

Requisito: N deve ser potência de 2.

Complexidade: O(N·log₂N)
    - (N/2)·log₂N multiplicações complexas (operações butterfly)
    - N·log₂N somas complexas (adições e subtrações butterfly)
"""

import cmath
import math
import time

from .protocolo_transformada import ProtocoloTransformada
from .resultado_transformada import ResultadoTransformada


class CalculadoraFFT(ProtocoloTransformada):
    """
    Calcula a FFT pelo algoritmo Cooley-Tukey (Decimação no Tempo).

    Apenas calcula e contabiliza operações.
    A explicação passo a passo do algoritmo fica em DecomposicaoButterfly.
    """

    NOME_ALGORITMO = "FFT (Cooley-Tukey)"

    def __init__(self) -> None:
        # Contadores de operações são atributos privados reiniciados
        # a cada chamada de `calcular`, evitando estado compartilhado
        # entre chamadas sucessivas.
        self._total_multiplicacoes = 0
        self._total_somas = 0

    @staticmethod
    def e_potencia_de_dois(numero: int) -> bool:
        """Retorna True se número for potência de 2 (e positivo)."""
        return numero > 0 and (numero & (numero - 1)) == 0

    def _calcular_recursivamente(self, sequencia: list[complex]) -> list[complex]:
        """
        Implementação recursiva do algoritmo Cooley-Tukey.

        Caso base: sequência de tamanho 1 — a DFT de um único elemento
        é o próprio elemento (sem nenhuma operação aritmética).

        Caso recursivo: divide em amostras de índice par e ímpar,
        calcula a FFT de cada metade recursivamente e combina os
        resultados usando operações butterfly.
        """
        tamanho = len(sequencia)

        # Caso base: DFT de tamanho 1
        if tamanho == 1:
            return [sequencia[0]]

        # Separar amostras pelos índices pares e ímpares
        amostras_pares = [sequencia[n] for n in range(0, tamanho, 2)]
        amostras_impares = [sequencia[n] for n in range(1, tamanho, 2)]

        # Calcular FFT de cada metade recursivamente
        espectro_par = self._calcular_recursivamente(amostras_pares)
        espectro_impar = self._calcular_recursivamente(amostras_impares)

        # Combinar resultados — operação butterfly
        coeficientes = [complex(0, 0)] * tamanho
        metade = tamanho // 2

        for k in range(metade):
            # Fator twiddle: W_N^k = e^(-j·2π·k/N)
            angulo = -2 * cmath.pi * k / tamanho
            fator_twiddle = cmath.exp(complex(0, angulo))

            # Butterfly: uma multiplicação e duas somas (adição + subtração)
            produto = fator_twiddle * espectro_impar[k]
            self._total_multiplicacoes += 1

            coeficientes[k] = espectro_par[k] + produto
            coeficientes[k + metade] = espectro_par[k] - produto
            self._total_somas += 2

        return coeficientes

    def calcular(self, sequencia: list[float | int]) -> ResultadoTransformada:
        """
        Calcula a FFT de uma sequência real.

        Args:
            sequencia: Sequência de entrada x[n].
                       O comprimento DEVE ser potência de 2.

        Returns:
            ResultadoTransformada com coeficientes, magnitudes, fases
            e contadores de operações.

        Raises:
            ValueError: Se o comprimento da sequência não for potência de 2.
        """
        tamanho = len(sequencia)

        if not self.e_potencia_de_dois(tamanho):
            potencia_abaixo = 2 ** math.floor(math.log2(tamanho))
            potencia_acima = 2 ** math.ceil(math.log2(tamanho))
            raise ValueError(
                f"O tamanho da sequência N={tamanho} não é potência de 2. "
                f"O algoritmo Cooley-Tukey exige N = 2^m. "
                f"Potências de 2 mais próximas: {potencia_abaixo} e {potencia_acima}."
            )

        # Reiniciar contadores para esta execução
        self._total_multiplicacoes = 0
        self._total_somas = 0

        sequencia_complexa = [complex(amostra) for amostra in sequencia]

        inicio = time.perf_counter()
        coeficientes = self._calcular_recursivamente(sequencia_complexa)
        tempo_segundos = time.perf_counter() - inicio

        return ResultadoTransformada(
            nome_algoritmo=self.NOME_ALGORITMO,
            tamanho=tamanho,
            coeficientes=coeficientes,
            magnitudes=[abs(c) for c in coeficientes],
            fases=[cmath.phase(c) for c in coeficientes],
            multiplicacoes=self._total_multiplicacoes,
            somas=self._total_somas,
            tempo_segundos=tempo_segundos,
        )
