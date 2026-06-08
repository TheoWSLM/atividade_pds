"""
Gerador de gráficos de espectro e comparação de complexidade.

Produz os arquivos PNG de espectro e complexidade.
Nenhum cálculo matemático ocorre aqui.
"""

import math
import os

import matplotlib
import matplotlib.pyplot as plt

# Backend não-interativo: gera PNGs sem exigir display gráfico
matplotlib.use("Agg")


class GeradorGraficos:
    """
    Gera gráficos de espectro e comparação de complexidade como arquivos PNG.

    Todos os métodos recebem o diretório de saída por parâmetro,
    tornando a classe testável sem dependência do sistema de arquivos global.
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
        """
        Gera figura com 3 subplots: sinal, magnitude e fase.

        Args:
            sequencia:       Sequência de entrada x[n].
            coeficientes:    Coeficientes espectrais X[k].
            titulo:          Título da figura.
            nome_arquivo:    Nome do arquivo (sem extensão).
            diretorio_saida: Diretório onde o PNG será salvo.

        Returns:
            Caminho completo do arquivo PNG gerado.
        """
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
        """
        Plota curvas de operações de dois algoritmos em escala log-log.

        Args:
            tamanhos:      Lista de valores de N.
            operacoes_a:   Total de operações do algoritmo A para cada N.
            operacoes_b:   Total de operações do algoritmo B para cada N.
            rotulo_a:      Legenda da curva A.
            rotulo_b:      Legenda da curva B.
            diretorio_saida: Diretório de saída.

        Returns:
            Caminho completo do arquivo PNG gerado.
        """
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

        # Curvas teóricas (pontilhadas) para referência
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

    # ── Método auxiliar privado ──────────────────────────────────────

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
        """Plota um stem plot padronizado em um eixo matplotlib."""
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
