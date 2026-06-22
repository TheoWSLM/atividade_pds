"""
Visualização gráfica e validação numérica para DFT e FFT.
"""

import math
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Configurar backend não-interativo do matplotlib
matplotlib.use("Agg")


class GeradorGraficos:
    """
    Gera gráficos de espectro de transformada (sinal, magnitude, fase)
    e gráficos de comparação de complexidade.
    """

    PALETA = {
        "sinal": "#2196F3",
        "magnitude": "#E91E63",
        "fase": "#4CAF50",
        "curva_a": "#E91E63",
        "curva_b": "#2196F3",
    }

    def plotar_espectro(
        self,
        sequencia: list[float | int],
        coeficientes: list[complex],
        titulo: str,
        nome_arquivo: str,
        diretorio_saida: str = "resultados",
    ) -> str:
        """Gera figura com 3 subplots: sinal, magnitude e fase (escala linear)."""
        os.makedirs(diretorio_saida, exist_ok=True)

        tamanho = len(sequencia)
        magnitudes = [abs(c) for c in coeficientes]
        fases = [
            math.atan2(c.imag, c.real) if abs(c) >= 1e-10 else 0.0
            for c in coeficientes
        ]

        fig, eixos = plt.subplots(3, 1, figsize=(10, 8))
        fig.suptitle(titulo, fontsize=14, fontweight="bold")

        self._plotar_stem(
            eixo=eixos[0],
            indices=list(range(tamanho)),
            valores=list(sequencia),
            cor=self.PALETA["sinal"],
            rotulo_x="n (amostras)",
            rotulo_y="x[n]",
            titulo_subplot="Sinal de Entrada x[n]",
        )

        self._plotar_stem(
            eixo=eixos[1],
            indices=list(range(tamanho)),
            valores=magnitudes,
            cor=self.PALETA["magnitude"],
            rotulo_x="k (frequência)",
            rotulo_y="|X[k]|",
            titulo_subplot="Espectro de Magnitude |X[k]|",
        )

        self._plotar_stem(
            eixo=eixos[2],
            indices=list(range(tamanho)),
            valores=fases,
            cor=self.PALETA["fase"],
            rotulo_x="k (frequência)",
            rotulo_y="∠X[k] (rad)",
            titulo_subplot="Espectro de Fase ∠X[k]",
        )

        plt.tight_layout()
        caminho = os.path.join(diretorio_saida, f"{nome_arquivo}.png")
        fig.savefig(caminho, dpi=150, bbox_inches="tight")
        plt.close(fig)

        print(f"  📊 Gráfico salvo em: {caminho}")
        return caminho

    def plotar_comparacao_complexidade(
        self,
        tamanhos: list[int],
        operacoes_a: list[int],
        operacoes_b: list[int],
        rotulo_a: str = "DFT — O(N²)",
        rotulo_b: str = "FFT — O(N·log₂N)",
        diretorio_saida: str = "resultados",
    ) -> str:
        """Plota curvas de operações de dois algoritmos em escala log-log."""
        os.makedirs(diretorio_saida, exist_ok=True)

        fig, eixo = plt.subplots(figsize=(10, 6))

        eixo.plot(
            tamanhos, operacoes_a, "o-",
            color=self.PALETA["curva_a"], linewidth=2, markersize=8, label=rotulo_a,
        )
        eixo.plot(
            tamanhos, operacoes_b, "s-",
            color=self.PALETA["curva_b"], linewidth=2, markersize=8, label=rotulo_b,
        )

        # Referências teóricas tracejadas
        intervalo = range(2, max(tamanhos) + 1)
        eixo.plot(
            intervalo,
            [n**2 + n * (n - 1) for n in intervalo],
            "--", color=self.PALETA["curva_a"], alpha=0.3,
            label="N² + N(N-1) teórico",
        )
        eixo.plot(
            intervalo,
            [
                (n // 2) * int(math.log2(n)) + n * int(math.log2(n))
                if n > 1 and (n & (n - 1)) == 0
                else None
                for n in intervalo
            ],
            "--", color=self.PALETA["curva_b"], alpha=0.3,
            label="(N/2+N)·log₂N teórico",
        )

        eixo.set_xlabel("N (tamanho da sequência)", fontsize=12)
        eixo.set_ylabel("Total de operações complexas", fontsize=12)
        eixo.set_title(
            "Comparação de Complexidade: DFT × FFT", fontsize=14, fontweight="bold"
        )
        eixo.legend(fontsize=10)
        eixo.grid(True, alpha=0.3)
        eixo.set_yscale("log")
        eixo.set_xscale("log", base=2)

        plt.tight_layout()
        caminho = os.path.join(diretorio_saida, "comparacao_complexidade.png")
        fig.savefig(caminho, dpi=150, bbox_inches="tight")
        plt.close(fig)

        print(f"  📊 Gráfico comparativo salvo em: {caminho}")
        return caminho

    @staticmethod
    def _plotar_stem(
        eixo: plt.Axes,
        indices: list[int],
        valores: list[float],
        cor: str,
        rotulo_x: str,
        rotulo_y: str,
        titulo_subplot: str,
    ) -> None:
        marcadores, hastes, linha_base = eixo.stem(
            indices, valores, linefmt="-", markerfmt="o", basefmt="-"
        )
        marcadores.set_color(cor)
        hastes.set_color(cor)
        linha_base.set_color("gray")
        eixo.set_xlabel(rotulo_x)
        eixo.set_ylabel(rotulo_y)
        eixo.set_title(titulo_subplot)
        eixo.set_xticks(indices)
        eixo.grid(True, alpha=0.3)


class ValidadorNumerico:
    """
    Compara coeficientes espectrais calculados com numpy.fft.fft para validação.
    """

    TOLERANCIA_PADRAO = 1e-10

    def __init__(self, tolerancia: float = TOLERANCIA_PADRAO) -> None:
        self._tolerancia = tolerancia

    def validar(
        self,
        sequencia: list[float | int],
        coeficientes_nossos: list[complex],
        nome_algoritmo: str = "Implementação manual",
    ) -> bool:
        """Compara nossa lista de coeficientes contra a do NumPy."""
        referencia_numpy = np.fft.fft(sequencia)
        nossos_como_array = np.array(coeficientes_nossos)

        coincide = bool(np.allclose(nossos_como_array, referencia_numpy, atol=self._tolerancia))

        print(f"\n  Validação [{nome_algoritmo}] vs. numpy.fft.fft: ", end="")

        if coincide:
            print("✅ RESULTADOS IDÊNTICOS")
        else:
            print("❌ DIVERGÊNCIA DETECTADA")
            self._imprimir_divergencias(coeficientes_nossos, referencia_numpy)

        return coincide

    def _imprimir_divergencias(
        self,
        nossos: list[complex],
        referencia: np.ndarray,
    ) -> None:
        for k, (nosso, ref) in enumerate(zip(nossos, referencia)):
            diferenca = abs(nosso - ref)
            if diferenca > self._tolerancia:
                print(
                    f"    k={k}: calculado={nosso:.6f}, "
                    f"numpy={ref:.6f}, "
                    f"diferença={diferenca:.2e}"
                )
