"""
Calculadoras de Transformadas Espectrais (DFT e FFT).

Este módulo agrupa os contratos, estruturas de dados e implementações
para cálculo de transformadas discretas de Fourier.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import cmath
import math
import time


@dataclass
class ResultadoTransformada:
    """
    Resultado genérico de uma transformada espectral discreta.

    Atributos:
        nome_algoritmo:      Identificador legível (ex: "DFT", "FFT Cooley-Tukey").
        tamanho:             N — comprimento da sequência de entrada.
        coeficientes:        X[k] para k = 0, ..., N-1 (números complexos).
        magnitudes:          |X[k]| — espectro de amplitude.
        fases:               ∠X[k] em radianos — espectro de fase.
        multiplicacoes:      Quantidade de multiplicações complexas realizadas.
        somas:               Quantidade de somas complexas realizadas.
        tempo_segundos:      Tempo de execução do cálculo em segundos.
    """

    nome_algoritmo: str
    tamanho: int
    coeficientes: list[complex]
    magnitudes: list[float]
    fases: list[float]
    multiplicacoes: int
    somas: int
    tempo_segundos: float

    @property
    def total_operacoes(self) -> int:
        """Soma de multiplicações e somas complexas."""
        return self.multiplicacoes + self.somas

    @property
    def tempo_microssegundos(self) -> float:
        """Tempo de execução convertido para microssegundos."""
        return self.tempo_segundos * 1_000_000

    def formatar_coeficiente(self, indice: int) -> str:
        """Retorna X[k] formatado como string para exibição."""
        coef = self.coeficientes[indice]
        mag = self.magnitudes[indice]
        fase = self.fases[indice]
        return (
            f"X[{indice}] = {coef.real:+8.4f} {coef.imag:+8.4f}j  "
            f"|X[{indice}]| = {mag:8.4f}  "
            f"∠X[{indice}] = {fase:+8.4f} rad"
        )

    def __str__(self) -> str:
        separador = "=" * 60
        linhas = [
            separador,
            f"  RESULTADO {self.nome_algoritmo} (N = {self.tamanho})",
            separador,
        ]
        for indice in range(self.tamanho):
            linhas.append(f"  {self.formatar_coeficiente(indice)}")
        linhas.extend([
            "─" * 60,
            f"  Multiplicações complexas: {self.multiplicacoes}",
            f"  Somas complexas:          {self.somas}",
            f"  Total de operações:       {self.total_operacoes}",
            f"  Tempo de execução:        {self.tempo_microssegundos:.2f} µs",
            separador,
        ])
        return "\n".join(linhas)


class ProtocoloTransformada(ABC):
    """
    Contrato mínimo que toda calculadora de transformada espectral deve cumprir.
    """

    @abstractmethod
    def calcular(self, sequencia: list[float | int]) -> ResultadoTransformada:
        """
        Calcula a transformada espectral de uma sequência discreta.

        Args:
            sequencia: Sequência de entrada x[n] com valores reais.

        Returns:
            ResultadoTransformada contendo os coeficientes complexos e métricas.
        """
        ...


class CalculadoraDFT(ProtocoloTransformada):
    """
    Calcula a DFT pela fórmula direta, sem otimizações.
    Complexidade: O(N²)
    """

    NOME_ALGORITMO = "DFT (Fórmula Direta)"

    def calcular(self, sequencia: list[float | int]) -> ResultadoTransformada:
        """
        Calcula a DFT de uma sequência real.
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


class CalculadoraFFT(ProtocoloTransformada):
    """
    Calcula a FFT pelo algoritmo Cooley-Tukey (Decimação no Tempo).
    Complexidade: O(N·log₂N)
    """

    NOME_ALGORITMO = "FFT (Cooley-Tukey)"

    @staticmethod
    def e_potencia_de_dois(numero: int) -> bool:
        """Retorna True se número for potência de 2 (e positivo)."""
        return numero > 0 and (numero & (numero - 1)) == 0

    def _calcular_recursivamente(self, sequencia: list[complex]) -> tuple[list[complex], int, int]:
        """
        Implementação recursiva do algoritmo Cooley-Tukey DIT.

        Returns:
            Tupla contendo (coeficientes_calculados, total_multiplicacoes, total_somas).
        """
        tamanho = len(sequencia)

        if tamanho == 1:
            return [sequencia[0]], 0, 0

        # Separar amostras pelos índices pares e ímpares
        amostras_pares = [sequencia[n] for n in range(0, tamanho, 2)]
        amostras_impares = [sequencia[n] for n in range(1, tamanho, 2)]

        # Calcular FFT de cada metade recursivamente
        espectro_par, mults_par, somas_par = self._calcular_recursivamente(amostras_pares)
        espectro_impar, mults_impar, somas_impar = self._calcular_recursivamente(amostras_impares)

        # Combinar resultados — operação butterfly
        coeficientes = [complex(0, 0)] * tamanho
        metade = tamanho // 2

        mults_comb = 0
        somas_comb = 0

        for k in range(metade):
            # Fator twiddle: W_N^k = e^(-j·2π·k/N)
            angulo = -2 * cmath.pi * k / tamanho
            fator_twiddle = cmath.exp(complex(0, angulo))

            # Butterfly: uma multiplicação e duas somas (adição + subtração)
            produto = fator_twiddle * espectro_impar[k]
            mults_comb += 1

            coeficientes[k] = espectro_par[k] + produto
            coeficientes[k + metade] = espectro_par[k] - produto
            somas_comb += 2

        total_mults = mults_par + mults_impar + mults_comb
        total_somas = somas_par + somas_impar + somas_comb

        return coeficientes, total_mults, total_somas

    def calcular(self, sequencia: list[float | int]) -> ResultadoTransformada:
        """
        Calcula a FFT de uma sequência real.
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

        sequencia_complexa = [complex(amostra) for amostra in sequencia]

        inicio = time.perf_counter()
        coeficientes, total_mults, total_somas = self._calcular_recursivamente(sequencia_complexa)
        tempo_segundos = time.perf_counter() - inicio

        return ResultadoTransformada(
            nome_algoritmo=self.NOME_ALGORITMO,
            tamanho=tamanho,
            coeficientes=coeficientes,
            magnitudes=[abs(c) for c in coeficientes],
            fases=[cmath.phase(c) for c in coeficientes],
            multiplicacoes=total_mults,
            somas=total_somas,
            tempo_segundos=tempo_segundos,
        )
