"""
Exercício 4 — FFT para x[n] = {0, 1, 2, 3, 4, 5, 6, 7}  (N = 8)

Objetivos:
    1. Calcular a FFT da sequência de 8 amostras
    2. Demonstrar o reordenamento bit-reversal e cada estágio butterfly
    3. Verificar a simetria conjugada do espectro (X[k] = X*[N-k])
    4. Apresentar o espectro de magnitude e fase
    5. Comparar o custo computacional com a DFT direta equivalente
"""

import math

from pds.transformadas import (
    CalculadoraFFT,
    DecomposicaoButterfly,
    GeradorGraficos,
    ValidadorNumerico,
)


def executar() -> None:
    """Executa a resolução completa do Exercício 4."""

    print("\n" + "█" * 70)
    print("█  EXERCÍCIO 4 — FFT para x[n] = {0,1,2,3,4,5,6,7}  (N = 8)")
    print("█" * 70)

    sequencia = [0, 1, 2, 3, 4, 5, 6, 7]
    tamanho = len(sequencia)

    # ── Instanciar dependências ───────────────────────────────────────
    calculadora = CalculadoraFFT()
    decomposicao = DecomposicaoButterfly()
    validador = ValidadorNumerico()
    graficos = GeradorGraficos()

    # ── Parte 1: Cálculo ─────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("  PARTE 1: Cálculo da FFT (Cooley-Tukey)")
    print("─" * 70)

    resultado = calculadora.calcular(sequencia)
    print(resultado)

    validador.validar(sequencia, resultado.coeficientes, "FFT Manual (N=8)")

    # ── Parte 2: Decomposição butterfly passo a passo ─────────────────
    print("\n" + "─" * 70)
    print("  PARTE 2: Decomposição Butterfly Passo a Passo")
    print("─" * 70)

    decomposicao.exibir(sequencia)

    # ── Parte 3: Espectro ─────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("  PARTE 3: Espectro de Frequência")
    print("─" * 70)

    graficos.plotar_espectro(
        sequencia=sequencia,
        coeficientes=resultado.coeficientes,
        titulo=f"Exercício 4 — FFT de x[n] = {sequencia} (N={tamanho})",
        nome_arquivo="ex4_fft_espectro_n8",
    )

    # ── Parte 4: Análise do espectro ──────────────────────────────────
    print(f"""
  ┌─ ANÁLISE DO ESPECTRO (N = {tamanho}):
  │
  │  • X[0] = {resultado.coeficientes[0].real:.0f}  (componente DC = soma de todos x[n])
  │  • O espectro de entrada real é conjugado-simétrico: X[k] = X*[N-k]
  │    Verificação:
  │""")

    for k in range(1, tamanho // 2):
        coef_k = resultado.coeficientes[k]
        coef_n_menos_k = resultado.coeficientes[tamanho - k]
        conjugado = complex(coef_k.real, -coef_k.imag)
        coincide = abs(coef_n_menos_k - conjugado) < 1e-10
        icone = "✅" if coincide else "❌"
        print(
            f"  │    X[{k}] = {coef_k.real:+.4f}{coef_k.imag:+.4f}j  "
            f"X[{tamanho - k}]* = {conjugado.real:+.4f}{conjugado.imag:+.4f}j  {icone}"
        )

    log2_tamanho = int(math.log2(tamanho))
    mult_fft_teorica = (tamanho // 2) * log2_tamanho
    soma_fft_teorica = tamanho * log2_tamanho
    mult_dft_equivalente = tamanho ** 2
    soma_dft_equivalente = tamanho * (tamanho - 1)
    razao = (mult_dft_equivalente + soma_dft_equivalente) / max(
        mult_fft_teorica + soma_fft_teorica, 1
    )

    print(f"""  │
  │  • Operações realizadas pela FFT:
  │    - Multiplicações: {resultado.multiplicacoes}  (teórico: (N/2)·log₂N = {mult_fft_teorica})
  │    - Somas:          {resultado.somas}  (teórico: N·log₂N = {soma_fft_teorica})
  │    - Estágios:       log₂{tamanho} = {log2_tamanho}
  │
  │  • Custo equivalente pela DFT direta:
  │    - Multiplicações: N² = {mult_dft_equivalente}
  │    - Somas:          N·(N-1) = {soma_dft_equivalente}
  │    - Razão:          {razao:.1f}× mais operações do que a FFT
  └─
""")
