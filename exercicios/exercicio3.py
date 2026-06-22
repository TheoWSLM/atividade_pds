"""
Exercício 3 — DFT e FFT para x[n] = {0, 1, 2, 3}  (N = 4)

Objetivos:
    1. Calcular a DFT da sequência x[n] = {0, 1, 2, 3}
    2. Calcular a FFT da mesma sequência pelo algoritmo Cooley-Tukey
    3. Comparar os dois métodos em termos de:
       - Coeficientes espectrais (devem ser idênticos)
       - Número de operações (multiplicações e somas complexas)
       - Tempo de execução
       - Complexidade computacional O(N²) vs O(N·log₂N)
"""

import math

from pds.transformadas import (
    CalculadoraDFT,
    CalculadoraFFT,
    ComparadorAlgoritmos,
    GeradorRelatorio,
    GeradorGraficos,
    ValidadorNumerico,
)


def executar() -> None:
    """Executa a resolução completa do Exercício 3."""

    print("\n" + "█" * 70)
    print("█  EXERCÍCIO 3 — DFT e FFT para x[n] = {0, 1, 2, 3}  (N = 4)")
    print("█" * 70)

    sequencia = [0, 1, 2, 3]
    tamanho = len(sequencia)

    # ── Instanciar dependências ───────────────────────────────────────
    calculadora_dft = CalculadoraDFT()       # calcula DFT
    calculadora_fft = CalculadoraFFT()       # calcula FFT
    validador = ValidadorNumerico()          # compara contra NumPy
    graficos = GeradorGraficos()             # gera arquivos PNG

    comparador = ComparadorAlgoritmos(
        algoritmo_a=calculadora_dft,
        algoritmo_b=calculadora_fft,
    )
    relatorio = GeradorRelatorio()           # formata texto

    # ── Parte 1: DFT ─────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("  PARTE 1: Cálculo da DFT (Fórmula Direta)")
    print("─" * 70)

    resultado_dft = calculadora_dft.calcular(sequencia)
    print(resultado_dft)

    validador.validar(sequencia, resultado_dft.coeficientes, "DFT Manual")

    graficos.plotar_espectro(
        sequencia=sequencia,
        coeficientes=resultado_dft.coeficientes,
        titulo=f"Exercício 3 — DFT de x[n] = {sequencia} (N={tamanho})",
        nome_arquivo="ex3_dft_espectro",
    )

    # ── Parte 2: FFT ─────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("  PARTE 2: Cálculo da FFT (Cooley-Tukey)")
    print("─" * 70)

    resultado_fft = calculadora_fft.calcular(sequencia)
    print(resultado_fft)

    validador.validar(sequencia, resultado_fft.coeficientes, "FFT Manual")

    graficos.plotar_espectro(
        sequencia=sequencia,
        coeficientes=resultado_fft.coeficientes,
        titulo=f"Exercício 3 — FFT de x[n] = {sequencia} (N={tamanho})",
        nome_arquivo="ex3_fft_espectro",
    )

    # ── Parte 3: Comparação DFT × FFT ────────────────────────────────
    print("\n" + "─" * 70)
    print("  PARTE 3: Comparação DFT × FFT")
    print("─" * 70)

    resultado_comparacao = comparador.comparar(sequencia)
    relatorio.imprimir(resultado_comparacao)

    # ── Parte 4: Análise teórica ──────────────────────────────────────
    print("\n" + "─" * 70)
    print("  PARTE 4: Análise Teórica Complementar")
    print("─" * 70)

    log2_tamanho = int(math.log2(tamanho))
    mult_dft = tamanho ** 2
    soma_dft = tamanho * (tamanho - 1)
    mult_fft = (tamanho // 2) * log2_tamanho
    soma_fft = tamanho * log2_tamanho
    razao = (mult_dft + soma_dft) / max(mult_fft + soma_fft, 1)

    print(f"""
  Para N = {tamanho}:

  ┌─ DFT (método direto):
  │  • Multiplicações complexas: N²      = {tamanho}² = {mult_dft}
  │  • Somas complexas:          N·(N-1) = {tamanho}·{tamanho - 1} = {soma_dft}
  │  • Total:                    {mult_dft + soma_dft} operações
  │  • Complexidade:             O(N²)
  │
  ├─ FFT (Cooley-Tukey):
  │  • Estágios:                 log₂({tamanho}) = {log2_tamanho}
  │  • Multiplicações complexas: (N/2)·log₂N = {tamanho // 2}·{log2_tamanho} = {mult_fft}
  │  • Somas complexas:          N·log₂N     = {tamanho}·{log2_tamanho} = {soma_fft}
  │  • Total:                    {mult_fft + soma_fft} operações
  │  • Complexidade:             O(N·log₂N)
  │
  └─ Conclusão:
     • A FFT reduz de {mult_dft + soma_dft} para {mult_fft + soma_fft} operações ({razao:.1f}×).
     • Para N pequeno (N=4), a vantagem é modesta.
     • Para N=1024: DFT ≈ 2M operações vs FFT ≈ 15K → ~137× de redução.
     • Ambos produzem resultados numericamente idênticos.
     • Custo da FFT: N deve ser potência de 2 (zero-padding se necessário).
""")
