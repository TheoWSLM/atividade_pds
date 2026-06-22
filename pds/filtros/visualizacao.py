"""
Visualização de Filtros FIR: Plotagem da resposta ao impulso h[n] e da resposta em frequência H(e^jω) em dB.
"""

import os
import math
import matplotlib.pyplot as plt
from .dominio import FiltroFIR


class GeradorGraficosFiltros:
    """
    Gera gráficos comparativos para análise de filtros FIR.
    """

    PALETAS = {
        "Retangular": "#E91E63",  # Rosa/Red
        "Triangular": "#FF9800",  # Laranja
        "Hann": "#4CAF50",        # Verde
        "Hamming": "#2196F3",     # Azul
        "Blackman": "#9C27B0",    # Roxo
    }

    def plotar_comparativo_filtros(
        self,
        filtros: list[FiltroFIR],
        fc: float,
        diretorio_saida: str = "resultados",
        nome_arquivo: str = "ex2_resposta_filtros",
    ) -> str:
        """
        Plota a resposta ao impulso h[n] e a resposta em frequência de magnitude (em dB)
        para todos os filtros da lista, permitindo comparação visual direta.
        """
        os.makedirs(diretorio_saida, exist_ok=True)

        fig, eixos = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle("Exercício 2 — Projeto de Filtro Passa-Baixas FIR via Janelamento (M = 60)", fontsize=16, fontweight="bold")

        ax_impulse = eixos[0]
        ax_freq = eixos[1]

        # ── 1. Resposta ao Impulso h[n] ───────────────────────────────────────
        ax_impulse.set_title("Resposta ao Impulso h[n] dos Filtros Projetados", fontsize=12, fontweight="bold")
        for f in filtros:
            ax_impulse.plot(
                f.coeficientes,
                "o-",
                label=f.nome_janela,
                color=self.PALETAS[f.nome_janela],
                markersize=4,
                linewidth=1.5,
                alpha=0.85
            )
        ax_impulse.set_xlabel("n (amostra)")
        ax_impulse.set_ylabel("Amplitude h[n]")
        ax_impulse.grid(True, alpha=0.3)
        ax_impulse.legend()
        ax_impulse.set_xlim(0, filtros[0].ordem)

        # ── 2. Resposta em Frequência de Magnitude em dB ───────────────────────
        ax_freq.set_title("Resposta em Frequência Magnitude |H(e^jω)| em dB", fontsize=12, fontweight="bold")

        for f in filtros:
            frequencias, h_complexo = f.resposta_frequencia(n_fft=2048)
            ganho_dc = abs(h_complexo[0])
            if ganho_dc < 1e-15:
                ganho_dc = 1e-15

            # Calcular ganho em dB normalizado
            ganho_db = [20 * math.log10(max(abs(h), 1e-10) / ganho_dc) for h in h_complexo]

            ax_freq.plot(
                frequencias,
                ganho_db,
                label=f.nome_janela,
                color=self.PALETAS[f.nome_janela],
                linewidth=2.0
            )

        # Destacar a frequência de corte especificada (1200 Hz) e o início da stopband (2000 Hz)
        ax_freq.axvline(fc, color="black", linestyle="--", alpha=0.7)
        ax_freq.text(fc + 50, -5, f"fc = {fc} Hz (-6 dB)", color="black", fontsize=9, fontweight="bold")

        ax_freq.axvline(2000, color="gray", linestyle=":", alpha=0.7)
        ax_freq.text(2000 + 50, -80, "Início Stopband Segura\n(2000 Hz)", color="gray", fontsize=9)

        ax_freq.set_xlabel("Frequência (Hz)")
        ax_freq.set_ylabel("Ganho (dB)")
        ax_freq.set_ylim(-90, 5)  # focado na faixa dinâmica clássica de filtros digitais
        ax_freq.set_xlim(0, filtros[0].fs / 2)  # até Nyquist
        ax_freq.grid(True, which="both", alpha=0.3)
        ax_freq.legend(loc="upper right")

        plt.tight_layout()
        caminho = os.path.join(diretorio_saida, f"{nome_arquivo}.png")
        fig.savefig(caminho, dpi=150, bbox_inches="tight")
        plt.close(fig)

        print(f"  📊 Gráfico de resposta dos filtros salvo em: {caminho}")
        return caminho
