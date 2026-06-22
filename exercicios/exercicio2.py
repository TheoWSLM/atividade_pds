"""
Exercício 2 — Projeto de Filtro Digital Passa-Baixas FIR via Método do Janelamento

Objetivos:
    1. Projetar a resposta ao impulso ideal h_ideal[n] para um filtro passa-baixas
       com fc = 1200 Hz, fs = 8000 Hz, ordem M = 60.
    2. Tratar matematicamente a indefinição em n = M/2 = 30.
    3. Aplicar as 5 janelas (Retangular, Triangular, Hann, Hamming, Blackman).
    4. Avaliar a resposta em frequência (largura da banda de transição e atenuação stopband).
    5. Visualizar e comparar graficamente as atenuações em escala de dB.
"""

from pds.janelas import (
    JanelaRetangular,
    JanelaTriangular,
    JanelaHann,
    JanelaHamming,
    JanelaBlackman,
)
from pds.filtros import (
    ProjetistaFiltroFIR,
    AnalisadorFiltros,
    GeradorGraficosFiltros,
)


def executar() -> None:
    """Executa a resolução completa do Exercício 2."""

    print("\n" + "█" * 70)
    print("█  EXERCÍCIO 2 — PROJETO DE FILTRO PASSA-BAIXAS FIR VIA JANELAMENTO")
    print("█" * 70)

    # ── Parâmetros do filtro ──────────────────────────────────────────
    fs = 8000.0   # Taxa de amostragem: 8 kHz
    fc = 1200.0   # Frequência de corte: 1.2 kHz
    ordem = 60    # Ordem M (61 coeficientes)

    print("\n  Parâmetros de Projeto:")
    print(f"    • Taxa de amostragem (fs): {fs:.1f} Hz")
    print(f"    • Frequência de corte (fc): {fc:.1f} Hz")
    print(f"    • Ordem do filtro (M): {ordem}  |  ({ordem + 1} coeficientes de h[n])")
    print("    • Frequência de corte normalizada (wc): 0.3π rad/amostra")

    # ── 1. Instanciar Projetista e Janelas ─────────────────────────────
    projetista = ProjetistaFiltroFIR(fs=fs, fc=fc, ordem=ordem)

    janelas = [
        JanelaRetangular(),
        JanelaTriangular(),
        JanelaHann(),
        JanelaHamming(),
        JanelaBlackman(),
    ]

    # ── 2. Projetar os 5 Filtros Janelados ──────────────────────────────
    print("\n  📐 Projetando filtros e aplicando janelamento...")
    filtros_projetados = []
    for janela in janelas:
        filtro = projetista.projetar_janelado(janela)
        filtros_projetados.append(filtro)

    # ── 3. Gerar Gráficos de Resposta em Frequência (dB) ───────────────
    print("  📊 Gerando gráficos comparativos de resposta em frequência...")
    plotador = GeradorGraficosFiltros()
    plotador.plotar_comparativo_filtros(
        filtros=filtros_projetados,
        fc=fc,
    )

    # ── 4. Analisar e Comparar Desempenho ──────────────────────────────
    analisador = AnalisadorFiltros()
    relatorio_comparativo = analisador.comparar_filtros(filtros_projetados, f_stopband_inicio=2000.0)
    print("\n" + relatorio_comparativo)
