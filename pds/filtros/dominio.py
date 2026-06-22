"""
Domínio de Filtros FIR: Projeto de filtros via método de janelamento e análise de resposta ao impulso.
"""

import math
from pds.janelas.dominio import ProtocoloJanela
from pds.transformadas.calculadoras import CalculadoraFFT


class FiltroFIR:
    """
    Representa um Filtro Digital FIR (Finite Impulse Response).
    """

    def __init__(self, coeficientes: list[float], janela: ProtocoloJanela, fs: float) -> None:
        """
        Args:
            coeficientes: Coeficientes h[n] do filtro.
            janela:       Janela (implementando ProtocoloJanela) usada no projeto.
            fs:           Taxa de amostragem em Hz.
        """
        self.coeficientes = coeficientes
        self.janela = janela
        self.nome_janela = janela.nome
        self.fs = fs
        self.ordem = len(coeficientes) - 1

    def resposta_frequencia(self, n_fft: int = 2048) -> tuple[list[float], list[complex]]:
        """
        Calcula a resposta em frequência H(e^jω) usando FFT (zero-padding).

        Args:
            n_fft: Comprimento da FFT (deve ser potência de 2).

        Returns:
            Tupla (frequencias_hz, h_complexo) para frequências de 0 a fs/2 (Nyquist).
        """
        # Validar potência de 2
        if not (n_fft > 0 and (n_fft & (n_fft - 1)) == 0):
            n_fft = 2048

        # Preencher com zeros até o tamanho da FFT (zero-padding defensivo)
        pad = [0.0] * n_fft
        limite = min(len(self.coeficientes), n_fft)
        for i in range(limite):
            pad[i] = self.coeficientes[i]

        # Calcular FFT
        calculadora = CalculadoraFFT()
        resultado = calculadora.calcular(pad)

        # Pegar apenas a metade positiva do espectro (0 até Nyquist)
        metade = n_fft // 2 + 1
        h_complexo = resultado.coeficientes[:metade]
        frequencias_hz = [k * self.fs / n_fft for k in range(metade)]

        return frequencias_hz, h_complexo


class ProjetistaFiltroFIR:
    """
    Projeta filtros FIR Passa-Baixas usando o método do janelamento.
    """

    def __init__(self, fs: float, fc: float, ordem: int) -> None:
        """
        Args:
            fs:    Taxa de amostragem em Hz.
            fc:    Frequência de corte em Hz.
            ordem: M — ordem do filtro (número de coeficientes é M + 1).
        """
        self.fs = fs
        self.fc = fc
        self.ordem = ordem
        self.wc = 2 * math.pi * (fc / fs)  # Frequência de corte normalizada (rad/amostra)

    def projetar_ideal(self) -> list[float]:
        """
        Gera a resposta ao impulso ideal h_ideal[n] (causal, centrada em M/2).
        h_ideal[n] = sin(wc * (n - M/2)) / (pi * (n - M/2))
        """
        M = self.ordem
        metade = M / 2.0
        h_ideal = [0.0] * (M + 1)

        for n in range(M + 1):
            n_centralizado = n - metade
            if abs(n_centralizado) < 1e-9:
                # Tratamento do ponto de indefinição pelo limite L'Hopital
                h_ideal[n] = self.wc / math.pi
            else:
                h_ideal[n] = math.sin(self.wc * n_centralizado) / (math.pi * n_centralizado)

        return h_ideal

    def projetar_janelado(self, janela: ProtocoloJanela) -> FiltroFIR:
        """
        Projeta o filtro FIR truncando a resposta ideal com a janela especificada.
        h[n] = h_ideal[n] * w[n]
        """
        h_ideal = self.projetar_ideal()
        # A janela tem comprimento igual ao número de coeficientes (M + 1)
        w = janela.gerar(self.ordem + 1)
        h_janelado = [h_id * w_n for h_id, w_n in zip(h_ideal, w)]

        return FiltroFIR(
            coeficientes=h_janelado,
            janela=janela,
            fs=self.fs,
        )
