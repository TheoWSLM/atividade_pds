"""
Análise analítica de janelas: largura de lóbulo principal, lóbulos laterais e vazamento espectral.
"""

from tabulate import tabulate


from pds.janelas.dominio import (
    JanelaRetangular,
    JanelaTriangular,
    JanelaHann,
    JanelaHamming,
    JanelaBlackman,
)


class AnalisadorJanelas:
    """
    Realiza a análise das características teóricas e práticas das janelas.
    """

    @staticmethod
    def obter_janelas() -> list:
        """Gera instâncias das 5 janelas para consulta de propriedades."""
        return [
            JanelaRetangular(),
            JanelaTriangular(),
            JanelaHann(),
            JanelaHamming(),
            JanelaBlackman(),
        ]

    def gerar_tabela_comparativa(self) -> str:
        """Retorna a tabela comparativa teórica formatada como string."""
        cabecalhos = [
            "Janela",
            "Largura Lóbulo Principal (≈)",
            "Pico Lóbulo Lateral",
            "Taxa de Decaimento",
        ]
        linhas = [
            [
                j.nome,
                j.largura_lobulo_principal_bins,
                f"{j.atenuacao_sidelobe_db:.1f} dB",
                f"{j.taxa_decaimento_db_oitava:+.1f} dB/oitava",
            ]
            for j in self.obter_janelas()
        ]
        return tabulate(
            linhas,
            headers=cabecalhos,
            tablefmt="simple_outline",
        )

    def gerar_relatorio_analise(self, N: int, fs: float, f1: float, f2: float) -> str:
        """
        Gera a discussão teórica detalhada sobre o vazamento espectral e a resolução
        das duas componentes frequenciais do Exercício 1.
        """
        resolucao_bin = fs / N
        distancia_hz = abs(f2 - f1)
        distancia_bins = distancia_hz / resolucao_bin

        sep = "═" * 75
        linhas = [
            sep,
            f"  ANÁLISE DE VAZAMENTO ESPECTRAL E RESOLUÇÃO DE TONES (N = {N}, fs = {fs} Hz)",
            sep,
            f"  • Componentes: f1 = {f1} Hz (A1 = 1.0, 0 dB) e f2 = {f2} Hz (A2 = 0.1, -20 dB)",
            f"  • Espaçamento entre frequências: {distancia_hz} Hz",
            f"  • Resolução de frequência por bin do DFT: {resolucao_bin:.3f} Hz/bin",
            f"  • Separação em número de bins espectrais: {distancia_bins:.2f} bins",
            "",
            "  ┌─ TABELA DE PROPRIEDADES TEÓRICAS DAS JANELAS:",
            self.gerar_tabela_comparativa(),
            "",
            "  ┌─ AVALIAÇÃO DOS COMPORTAMENTOS NO ESPECTRO:",
            "  │",
            "  ├─ 1. Janela Retangular:",
            "  │  • Tem o lóbulo principal mais estreito (2 bins), o que daria a melhor",
            "  │    resolução espectral teórica.",
            "  │  • Contudo, o pico de lóbulo lateral é de apenas -13 dB. Como o tom fraco",
            "  │    em 110 Hz tem amplitude de 0.1 (-20 dB), ele é COMPLETAMENTE MASCARADO",
            "  │    ou gravemente distorcido pelo vazamento espectral (sidelobes) do tom forte.",
            "  │",
            "  ├─ 2. Janela Triangular (Bartlett):",
            "  │  • Aumenta a largura do lóbulo para 4 bins e atenua o lóbulo lateral para -26 dB.",
            "  │  • A atenuação é suficiente para que o tom em 110 Hz apareça como um ombro ou",
            "  │    pequeno pico, mas ainda sofre forte interferência dos lóbulos da janela.",
            "  │",
            "  ├─ 3. Janelas de Hann e Hamming:",
            "  │  • Ambas possuem lóbulo principal de 4 bins. A Hamming possui menor pico lateral",
            "  │    (-43 dB vs -32 dB da Hann), mas a Hann decai mais rapidamente (-18 vs -6 dB/oitava).",
            "  │  • Ambas conseguem resolver com CLAREZA o segundo tom em 110 Hz, mostrando um pico",
            "  │    nítido a 20 dB abaixo do pico principal, livre da interferência de vazamento.",
            "  │  • Hamming é historicamente preferida para separar tons de amplitudes muito distantes",
            "  │    devido ao seu menor lóbulo lateral inicial.",
            "  │",
            "  ├─ 4. Janela de Blackman:",
            "  │  • Oferece a melhor atenuação de lóbulos laterais (-58 dB).",
            "  │  • Porém, seu lóbulo principal é muito largo (6 bins). Como a distância espectral",
            "  │    dos dois tons é de apenas 5.12 bins (menor que a largura de 6 bins), os lóbulos",
            "  │    principais de f1 e f2 se sobrepõem e se fundem (overlap).",
            "  │  • Consequentemente, a Blackman dificulta a visualização de dois picos distintos,",
            "  │    fundindo as frequências em uma resposta única alargada.",
            "  │",
            "  └─ CONCLUSÃO PRÁTICA: O compromisso (trade-off) entre largura de lóbulo principal",
            "     e atenuação de lóbulos laterais é evidente. Para esta atividade específica,",
            "     as janelas de Hann e Hamming oferecem o melhor equilíbrio, permitindo a separação",
            "     perfeita e visualização das duas componentes do sinal.",
            sep,
        ]
        return "\n".join(linhas)

    def imprimir_relatorio(self, N: int, fs: float, f1: float, f2: float) -> None:
        """Imprime o relatório analítico no terminal."""
        print(self.gerar_relatorio_analise(N, fs, f1, f2))
