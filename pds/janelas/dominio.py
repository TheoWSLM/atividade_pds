"""
Domínio de Janelamento: Protocolos, implementações de janelas e geradores de sinais.
"""

from abc import ABC, abstractmethod
import math


class ProtocoloJanela(ABC):
    """
    Contrato abstrato que define uma janela temporal.
    """

    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome legível da janela."""
        ...

    @property
    @abstractmethod
    def largura_lobulo_principal_bins(self) -> str:
        """Largura aproximada do lóbulo principal em número de bins."""
        ...

    @property
    @abstractmethod
    def atenuacao_sidelobe_db(self) -> float:
        """Atenuação do primeiro lóbulo lateral em dB."""
        ...

    @property
    @abstractmethod
    def taxa_decaimento_db_oitava(self) -> float:
        """Taxa de decaimento dos lóbulos laterais em dB/oitava."""
        ...

    @property
    @abstractmethod
    def fator_transicao_fir(self) -> float:
        """Fator C usado no cálculo da banda de transição de filtros FIR (e.g. C * fs / M)."""
        ...

    @property
    @abstractmethod
    def atenuacao_stopband_fir_db(self) -> float:
        """Atenuação teórica mínima na banda de rejeição do filtro FIR em dB."""
        ...

    @abstractmethod
    def gerar(self, tamanho: int) -> list[float]:
        """
        Gera os coeficientes w[n] da janela para um dado tamanho N.

        Args:
            tamanho: N — número de amostras da janela.

        Returns:
            Lista com os coeficientes da janela.
        """
        ...

    def aplicar(self, sinal: list[float]) -> list[float]:
        """
        Aplica a janela sobre um sinal (multiplicação termo a termo).

        Args:
            sinal: Sinal original x[n].

        Returns:
            Sinal janelado x_w[n] = x[n] * w[n].
        """
        tamanho = len(sinal)
        w = self.gerar(tamanho)
        return [x_n * w_n for x_n, w_n in zip(sinal, w)]


class JanelaRetangular(ProtocoloJanela):
    """
    Janela Retangular (ou Dirichlet).
    w[n] = 1.0 para 0 <= n < N.
    """

    @property
    def nome(self) -> str:
        return "Retangular"

    @property
    def largura_lobulo_principal_bins(self) -> str:
        return "2.0 (4π/N)"

    @property
    def atenuacao_sidelobe_db(self) -> float:
        return -13.0

    @property
    def taxa_decaimento_db_oitava(self) -> float:
        return -6.0

    @property
    def fator_transicao_fir(self) -> float:
        return 0.9

    @property
    def atenuacao_stopband_fir_db(self) -> float:
        return -21.0

    def gerar(self, tamanho: int) -> list[float]:
        if tamanho <= 0:
            return []
        return [1.0] * tamanho


class JanelaTriangular(ProtocoloJanela):
    """
    Janela Triangular (ou Bartlett).
    w[n] = 1.0 - |(n - (N-1)/2) / ((N-1)/2)| para 0 <= n < N.
    """

    @property
    def nome(self) -> str:
        return "Triangular"

    @property
    def largura_lobulo_principal_bins(self) -> str:
        return "4.0 (8π/N)"

    @property
    def atenuacao_sidelobe_db(self) -> float:
        return -26.0

    @property
    def taxa_decaimento_db_oitava(self) -> float:
        return -12.0

    @property
    def fator_transicao_fir(self) -> float:
        return 2.2

    @property
    def atenuacao_stopband_fir_db(self) -> float:
        return -25.0

    def gerar(self, tamanho: int) -> list[float]:
        if tamanho <= 0:
            return []
        if tamanho == 1:
            return [1.0]

        metade_comprimento = (tamanho - 1) / 2.0
        return [
            1.0 - abs((n - metade_comprimento) / metade_comprimento)
            for n in range(tamanho)
        ]


class JanelaHann(ProtocoloJanela):
    """
    Janela de Hann (ou Hanning).
    w[n] = 0.5 - 0.5 * cos(2*pi*n / (N-1)) para 0 <= n < N.
    """

    @property
    def nome(self) -> str:
        return "Hann"

    @property
    def largura_lobulo_principal_bins(self) -> str:
        return "4.0 (8π/N)"

    @property
    def atenuacao_sidelobe_db(self) -> float:
        return -32.0

    @property
    def taxa_decaimento_db_oitava(self) -> float:
        return -18.0

    @property
    def fator_transicao_fir(self) -> float:
        return 3.1

    @property
    def atenuacao_stopband_fir_db(self) -> float:
        return -44.0

    def gerar(self, tamanho: int) -> list[float]:
        if tamanho <= 0:
            return []
        if tamanho == 1:
            return [1.0]

        denominador = tamanho - 1
        return [
            0.5 - 0.5 * math.cos(2 * math.pi * n / denominador)
            for n in range(tamanho)
        ]


class JanelaHamming(ProtocoloJanela):
    """
    Janela de Hamming.
    w[n] = 0.54 - 0.46 * cos(2*pi*n / (N-1)) para 0 <= n < N.
    """

    @property
    def nome(self) -> str:
        return "Hamming"

    @property
    def largura_lobulo_principal_bins(self) -> str:
        return "4.0 (8π/N)"

    @property
    def atenuacao_sidelobe_db(self) -> float:
        return -43.0

    @property
    def taxa_decaimento_db_oitava(self) -> float:
        return -6.0

    @property
    def fator_transicao_fir(self) -> float:
        return 3.3

    @property
    def atenuacao_stopband_fir_db(self) -> float:
        return -53.0

    def gerar(self, tamanho: int) -> list[float]:
        if tamanho <= 0:
            return []
        if tamanho == 1:
            return [1.0]

        denominador = tamanho - 1
        return [
            0.54 - 0.46 * math.cos(2 * math.pi * n / denominador)
            for n in range(tamanho)
        ]


class JanelaBlackman(ProtocoloJanela):
    """
    Janela de Blackman.
    w[n] = 0.42 - 0.5 * cos(2*pi*n / (N-1)) + 0.08 * cos(4*pi*n / (N-1)) para 0 <= n < N.
    """

    @property
    def nome(self) -> str:
        return "Blackman"

    @property
    def largura_lobulo_principal_bins(self) -> str:
        return "6.0 (12π/N)"

    @property
    def atenuacao_sidelobe_db(self) -> float:
        return -58.0

    @property
    def taxa_decaimento_db_oitava(self) -> float:
        return -18.0

    @property
    def fator_transicao_fir(self) -> float:
        return 5.5

    @property
    def atenuacao_stopband_fir_db(self) -> float:
        return -74.0

    def gerar(self, tamanho: int) -> list[float]:
        if tamanho <= 0:
            return []
        if tamanho == 1:
            return [1.0]

        denominador = tamanho - 1
        return [
            0.42
            - 0.5 * math.cos(2 * math.pi * n / denominador)
            + 0.08 * math.cos(4 * math.pi * n / denominador)
            for n in range(tamanho)
        ]


class GeradorSinais:
    """
    Utilitário para geração de sinais de teste discretos no tempo.
    """

    @staticmethod
    def gerar_cossenos_soma(
        fs: float,
        componentes: list[tuple[float, float]],
        tamanho: int,
    ) -> list[float]:
        """
        Gera um sinal discreto soma de cossenos.

        Args:
            fs:           Frequência de amostragem em Hz.
            componentes:  Lista de tuplas (amplitude, frequencia_hz).
            tamanho:      N — número total de amostras a gerar.

        Returns:
            Lista com as amostras do sinal x[n].
        """
        sinal = [0.0] * tamanho
        for n in range(tamanho):
            tempo = n / fs
            for amp, freq in componentes:
                sinal[n] += amp * math.cos(2 * math.pi * freq * tempo)
        return sinal
