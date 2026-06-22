#!/usr/bin/env python3
"""
Atividade de Processamento Digital de Sinais (PDS)
===================================================

Ponto de entrada da aplicação. Orquestra a execução dos exercícios
e gera o gráfico comparativo de complexidade para múltiplos valores de N.

Uso:
    python main.py           → Executa todos os exercícios
    python main.py --ex3     → Executa apenas o Exercício 3
    python main.py --ex4     → Executa apenas o Exercício 4
"""

import argparse

from pds.transformadas import CalculadoraDFT, CalculadoraFFT, GeradorGraficos


def exibir_banner() -> None:
    """Exibe o cabeçalho do projeto no terminal."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     ██████╗ ██████╗ ███████╗                                         ║
║     ██╔══██╗██╔══██╗██╔════╝                                         ║
║     ██████╔╝██║  ██║███████╗                                         ║
║     ██╔═══╝ ██║  ██║╚════██║                                         ║
║     ██║     ██████╔╝███████║                                         ║
║     ╚═╝     ╚═════╝ ╚══════╝                                         ║
║                                                                      ║
║     Processamento Digital de Sinais                                  ║
║     Atividade: DFT e FFT                                             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")


def gerar_grafico_comparativo_complexidade() -> None:
    """
    Gera o gráfico de comparação de operações DFT vs FFT
    para tamanhos N = 2, 4, 8, ..., 256.

    Usa CalculadoraDFT e CalculadoraFFT diretamente pois este
    método pertence ao ponto de entrada, não ao domínio.
    """
    print("\n" + "─" * 70)
    print("  GRÁFICO COMPARATIVO: Operações DFT × FFT para N = 2, 4, ..., 256")
    print("─" * 70)

    calculadora_dft = CalculadoraDFT()
    calculadora_fft = CalculadoraFFT()
    gerador = GeradorGraficos()

    tamanhos = [2 ** potencia for potencia in range(1, 9)]  # 2 → 256
    operacoes_dft: list[int] = []
    operacoes_fft: list[int] = []

    for tamanho in tamanhos:
        sequencia = list(range(tamanho))

        resultado_dft = calculadora_dft.calcular(sequencia)
        resultado_fft = calculadora_fft.calcular(sequencia)

        operacoes_dft.append(resultado_dft.total_operacoes)
        operacoes_fft.append(resultado_fft.total_operacoes)

        razao = resultado_dft.total_operacoes / max(resultado_fft.total_operacoes, 1)
        print(
            f"  N = {tamanho:>4d}  |  "
            f"DFT: {resultado_dft.total_operacoes:>8d}  |  "
            f"FFT: {resultado_fft.total_operacoes:>6d}  |  "
            f"Razão: {razao:>6.1f}×"
        )

    gerador.plotar_comparacao_complexidade(
        tamanhos=tamanhos,
        operacoes_a=operacoes_dft,
        operacoes_b=operacoes_fft,
    )


def main() -> None:
    analisador = argparse.ArgumentParser(
        description="Atividade de PDS — Transformadas, Janelamento e Filtros FIR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py           Executa todos os exercícios
  python main.py --ex1     Apenas Exercício 1 (Janelamento, N=512)
  python main.py --ex2     Apenas Exercício 2 (Filtro FIR PB, M=60)
  python main.py --ex3     Apenas Exercício 3 (DFT/FFT, N=4)
  python main.py --ex4     Apenas Exercício 4 (FFT, N=8)
        """,
    )
    analisador.add_argument(
        "--ex1", action="store_true",
        help="Executar apenas o Exercício 1 (Janelamento e Espectros)"
    )
    analisador.add_argument(
        "--ex2", action="store_true",
        help="Executar apenas o Exercício 2 (Filtro FIR Passa-Baixas)"
    )
    analisador.add_argument(
        "--ex3", action="store_true",
        help="Executar apenas o Exercício 3 (DFT e FFT, N=4)"
    )
    analisador.add_argument(
        "--ex4", action="store_true",
        help="Executar apenas o Exercício 4 (FFT, N=8)"
    )

    argumentos = analisador.parse_args()
    executar_tudo = not (argumentos.ex1 or argumentos.ex2 or argumentos.ex3 or argumentos.ex4)

    exibir_banner()

    if argumentos.ex1 or executar_tudo:
        from exercicios.exercicio1 import executar as executar_ex1
        executar_ex1()

    if argumentos.ex2 or executar_tudo:
        from exercicios.exercicio2 import executar as executar_ex2
        executar_ex2()

    if argumentos.ex3 or executar_tudo:
        from exercicios.exercicio3 import executar as executar_ex3
        executar_ex3()

    if argumentos.ex4 or executar_tudo:
        from exercicios.exercicio4 import executar as executar_ex4
        executar_ex4()

    if executar_tudo:
        gerar_grafico_comparativo_complexidade()

    print("\n✅ Execução concluída! Gráficos salvos em ./resultados/\n")


if __name__ == "__main__":
    main()
