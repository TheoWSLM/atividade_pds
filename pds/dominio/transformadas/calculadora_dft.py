"""
Implementação manual da Transformada Discreta de Fourier (DFT).

A DFT é definida por:
    X[k] = Σ(n=0 até N-1) x[n] · e^(-j·2π·k·n/N)

onde:
    - x[n] é a sequência discreta de entrada
    - X[k] é o coeficiente espectral na frequência k
    - N é o comprimento da sequência
    - j é a unidade imaginária

Complexidade: O(N²)
    - N² multiplicações complexas
    - N·(N-1) somas complexas
"""

import cmath
import time

from .protocolo_transformada import ProtocoloTransformada
from .resultado_transformada import ResultadoTransformada


class CalculadoraDFT(ProtocoloTransformada):
    """
    Calcula a DFT pela fórmula direta, sem otimizações.

    Apenas calcula a DFT e contabiliza as operações realizadas.
    Formatação e visualização pertencem a outras camadas.
    """

    NOME_ALGORITMO = "DFT (Fórmula Direta)"

    def calcular(self, sequencia: list[float | int]) -> ResultadoTransformada:
        """
        Calcula a DFT de uma sequência real.

        Para cada frequência k, acumula a soma:
            X[k] = Σ x[n] · W_N^(k·n)
        onde W_N^(k·n) = e^(-j·2π·k·n/N) é o fator twiddle.

        Args:
            sequencia: Sequência de entrada x[n].

        Returns:
            ResultadoTransformada com coeficientes, magnitudes, fases
            e contadores de operações.
        """
        tamanho = len(sequencia)
        coeficientes: list[complex] = []
        total_multiplicacoes = 0
        total_somas = 0

        inicio = time.perf_counter()

        for k in range(tamanho):
            acumulador = complex(0, 0)

            for n in range(tamanho):
                # Fator twiddle: W_N^(k·n) = e^(-j·2π·k·n/N)
                angulo = -2 * cmath.pi * k * n / tamanho
                fator_twiddle = cmath.exp(complex(0, angulo))

                # Multiplicação: x[n] · W_N^(k·n)
                acumulador += sequencia[n] * fator_twiddle
                total_multiplicacoes += 1

                # A soma é contabilizada a partir da segunda amostra
                if n > 0:
                    total_somas += 1

            coeficientes.append(acumulador)

        tempo_segundos = time.perf_counter() - inicio

        return ResultadoTransformada(
            nome_algoritmo=self.NOME_ALGORITMO,
            tamanho=tamanho,
            coeficientes=coeficientes,
            magnitudes=[abs(c) for c in coeficientes],
            fases=[cmath.phase(c) for c in coeficientes],
            multiplicacoes=total_multiplicacoes,
            somas=total_somas,
            tempo_segundos=tempo_segundos,
        )
