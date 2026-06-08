"""
Script de validação: compara nossas implementações contra numpy.fft.fft.

Executado via `make validar`. Retorna código 0 se todos os testes
passarem, 1 se houver divergências.
"""

import sys

from pds.dominio import CalculadoraDFT, CalculadoraFFT
from pds.visualizacao import ValidadorNumerico


def main() -> None:
    sequencias = {
        "N=4":  [0, 1, 2, 3],
        "N=8":  list(range(8)),
        "N=16": list(range(16)),
        "N=32": list(range(32)),
    }

    dft = CalculadoraDFT()
    fft = CalculadoraFFT()
    validador = ValidadorNumerico()

    aprovados = 0
    total = 0

    print("")
    for nome, sequencia in sequencias.items():
        resultado_dft = dft.calcular(sequencia)
        aprovado_dft = validador.validar(
            sequencia, resultado_dft.coeficientes, f"DFT {nome}"
        )
        aprovados += int(aprovado_dft)
        total += 1

        resultado_fft = fft.calcular(sequencia)
        aprovado_fft = validador.validar(
            sequencia, resultado_fft.coeficientes, f"FFT {nome}"
        )
        aprovados += int(aprovado_fft)
        total += 1

    print(f"\n  Resultado: {aprovados}/{total} testes aprovados")

    if aprovados < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
