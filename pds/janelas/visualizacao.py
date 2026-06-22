"""
Visualização de Janelas: Plotagem de formas de onda, sinais janelados e espectros em dB.
"""

import os
import math
import matplotlib.pyplot as plt
from .dominio import ProtocoloJanela

class GeradorGraficosJanelas:
    """
    Gera as visualizações gráficas para a análise de janelas do Exercício 1.
    """

    PALETAS = {
        "Retangular": "#E91E63",  # Rosa/Red
        "Triangular": "#FF9800",  # Laranja
        "Hann": "#4CAF50",        # Verde
        "Hamming": "#2196F3",     # Azul
        "Blackman": "#9C27B0",    # Roxo
    }

    def plotar_comparativo_janelas(
        self,
        sinal_original: list[float],
        janelas: list[ProtocoloJanela],
        fs: float,
        diretorio_saida: str = "resultados",
        nome_arquivo: str = "ex1_janelas_e_espectros",
    ) -> str:
        """
        Gera uma visualização composta para comparar as 5 janelas:
        1. Formato temporal de cada janela w[n].
        2. Sinal janelado x_w[n].
        3. Comparação de espectro de magnitude (em dB, normalizado).
        """
        os.makedirs(diretorio_saida, exist_ok=True)
        N = len(sinal_original)
        frequencias = [k * fs / N for k in range(N // 2 + 1)]  # Apenas até Nyquist

        # Configurar figura com 3 subplots
        fig = plt.figure(figsize=(14, 10))
        grid = fig.add_gridspec(3, 2, height_ratios=[1, 1.2, 2.2])

        ax_shapes = fig.add_subplot(grid[0, :])
        ax_signals = fig.add_subplot(grid[1, :])
        ax_spectra = fig.add_subplot(grid[2, :])

        fig.suptitle("Exercício 1 — Comparação de Janelas Temporais e Resolução Espectral", fontsize=16, fontweight="bold")

        # ── 1. Plotar Formato Temporal das Janelas w[n] ───────────────────────
        ax_shapes.set_title("Formato das Janelas w[n] no Tempo", fontsize=12, fontweight="bold")
        for janela in janelas:
            w = janela.gerar(N)
            ax_shapes.plot(w, label=janela.nome, color=self.PALETAS[janela.nome], linewidth=2)
        ax_shapes.set_xlabel("n (amostras)")
        ax_shapes.set_ylabel("Amplitude")
        ax_shapes.grid(True, alpha=0.3)
        ax_shapes.legend(loc="lower center", ncol=5)
        ax_shapes.set_xlim(0, N - 1)

        # ── 2. Plotar Sinais Janelados x_w[n] (Trecho de 100 amostras para visualização) ─
        ax_signals.set_title("Sinais Janelados x_w[n] (Primeiras 150 amostras)", fontsize=12, fontweight="bold")
        n_vis = min(150, N)
        for janela in janelas:
            x_w = janela.aplicar(sinal_original)
            ax_signals.plot(x_w[:n_vis], label=janela.nome, color=self.PALETAS[janela.nome], alpha=0.85)
        ax_signals.set_xlabel("n (amostras)")
        ax_signals.set_ylabel("x[n] · w[n]")
        ax_signals.grid(True, alpha=0.3)
        ax_signals.set_xlim(0, n_vis - 1)

        # ── 3. Plotar Espectros de Magnitude em dB (Normalizados) ────────────
        ax_spectra.set_title("Comparação dos Espectros de Magnitude em dB (Zoom: 50 Hz a 160 Hz)", fontsize=12, fontweight="bold")

        # Importar CalculadoraFFT localmente para evitar import circular
        from pds.transformadas.calculadoras import CalculadoraFFT
        calculadora_fft = CalculadoraFFT()

        for janela in janelas:
            x_w = janela.aplicar(sinal_original)
            resultado = calculadora_fft.calcular(x_w)

            # Obter coeficientes até Nyquist
            coefs_nyq = resultado.coeficientes[:N // 2 + 1]
            mags = [abs(c) for c in coefs_nyq]

            # Encontrar máximo para normalização (em dB, escala relativa ao pico)
            max_mag = max(mags) if max(mags) > 1e-15 else 1e-15
            mags_db = [20 * math.log10(max(m, 1e-10) / max_mag) for m in mags]

            ax_spectra.plot(
                frequencias,
                mags_db,
                label=f"{janela.nome}",
                color=self.PALETAS[janela.nome],
                linewidth=2.0
            )

        # Destacar os tons teóricos de f1=100Hz e f2=110Hz
        ax_spectra.axvline(100, color="gray", linestyle="--", alpha=0.7)
        ax_spectra.text(98, -50, "f1 = 100 Hz\n(0 dB)", color="black", ha="right", fontsize=9, fontweight="bold")
        ax_spectra.axvline(110, color="gray", linestyle="--", alpha=0.7)
        ax_spectra.text(112, -50, "f2 = 110 Hz\n(-20 dB)", color="black", ha="left", fontsize=9, fontweight="bold")

        ax_spectra.set_xlabel("Frequência (Hz)")
        ax_spectra.set_ylabel("Magnitude Espectral (dB)")
        ax_spectra.set_ylim(-70, 5)  # focado na faixa de interesse para ver lóbulos laterais
        ax_spectra.set_xlim(50, 160)  # Zoom nos tons para ver a capacidade de resolução
        ax_spectra.grid(True, which="both", alpha=0.3)
        ax_spectra.legend(loc="upper right")

        plt.tight_layout()
        caminho = os.path.join(diretorio_saida, f"{nome_arquivo}.png")
        fig.savefig(caminho, dpi=150, bbox_inches="tight")
        plt.close(fig)

        print(f"  📊 Gráfico comparativo de janelas salvo em: {caminho}")
        return caminho
