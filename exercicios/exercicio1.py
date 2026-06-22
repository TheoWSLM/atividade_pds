"""
Exercício 1 — Janelamento Espectral e Resolução de Componentes Frequenciais

Objetivos:
    1. Gerar o sinal discreto multitonal x[n] com duas frequências próximas (100 Hz e 110 Hz)
       com amplitudes muito diferentes (1.0 e 0.1, correspondendo a -20 dB de diferença).
    2. Multiplicar o sinal pelas 5 janelas (Retangular, Triangular, Hann, Hamming, Blackman).
    3. Calcular a FFT para cada sinal janelado usando a CalculadoraFFT manual.
    4. Analisar os efeitos de largura de lóbulo principal e atenuação de lóbulos laterais.
    5. Visualizar graficamente os espectros resultantes em escala de dB.
"""

from pds.janelas import (
    JanelaRetangular,
    JanelaTriangular,
    JanelaHann,
    JanelaHamming,
    JanelaBlackman,
    GeradorSinais,
    AnalisadorJanelas,
    GeradorGraficosJanelas,
)
from pds.transformadas import ValidadorNumerico


def executar() -> None:
    """Executa a resolução completa do Exercício 1."""

    print("\n" + "█" * 70)
    print("█  EXERCÍCIO 1 — JANELAMENTO E ANÁLISE ESPECTRAL DE SINAL MULTITONAL")
    print("█" * 70)

    # ── Parâmetros do sinal ───────────────────────────────────────────
    fs = 1000.0  # Taxa de amostragem: 1 kHz
    N = 512      # Comprimento da sequência (potência de 2)
    f1 = 100.0   # Frequência 1: 100 Hz
    f2 = 110.0   # Frequência 2: 110 Hz
    A1 = 1.0     # Amplitude 1
    A2 = 0.1     # Amplitude 2

    print("\n  Parâmetros:")
    print(f"    • fs = {fs:.1f} Hz  |  N = {N} amostras")
    print(f"    • Componente 1: {f1:.1f} Hz (Amp = {A1:.1f})")
    print(f"    • Componente 2: {f2:.1f} Hz (Amp = {A2:.2f}, -20 dB)")

    # ── 1. Gerar Sinal Original x[n] ──────────────────────────────────
    componentes = [(A1, f1), (A2, f2)]
    sinal_original = GeradorSinais.gerar_cossenos_soma(fs, componentes, N)

    # ── 2. Instanciar Janelas ─────────────────────────────────────────
    janelas = [
        JanelaRetangular(),
        JanelaTriangular(),
        JanelaHann(),
        JanelaHamming(),
        JanelaBlackman(),
    ]

    # ── 3. Validar numericamente contra NumPy para integridade ──────────
    # Validamos os coeficientes espectrais do sinal janelado de Hamming como amostragem
    validador = ValidadorNumerico()
    sinal_janelado_teste = JanelaHamming().aplicar(sinal_original)
    from pds.transformadas.calculadoras import CalculadoraFFT
    calc_fft = CalculadoraFFT()
    resultado_fft_teste = calc_fft.calcular(sinal_janelado_teste)
    validador.validar(sinal_janelado_teste, resultado_fft_teste.coeficientes, "FFT Sinal Janelado (Hamming)")

    # ── 4. Gerar Gráfico Comparativo ──────────────────────────────────
    print("\n  📊 Gerando gráficos comparativos...")
    plotador = GeradorGraficosJanelas()
    plotador.plotar_comparativo_janelas(
        sinal_original=sinal_original,
        janelas=janelas,
        fs=fs,
    )

    # ── 5. Análise Teórica e Discussão de Resultados ─────────────────
    analisador = AnalisadorJanelas()
    analisador.imprimir_relatorio(N, fs, f1, f2)
