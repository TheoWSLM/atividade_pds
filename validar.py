"""
Script de validação: compara nossas implementações contra numpy.fft.fft.

Executado via `make validar`. Retorna código 0 se todos os testes
passarem, 1 se houver divergências.
"""

import sys
import numpy as np

from pds.transformadas import CalculadoraDFT, CalculadoraFFT, ValidadorNumerico


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

    # ── Validação Adicional: Filtro FIR (Exercício 2) ──────────────────
    from pds.filtros import ProjetistaFiltroFIR
    from pds.janelas import JanelaHamming

    projetista = ProjetistaFiltroFIR(fs=8000.0, fc=1200.0, ordem=60)
    filtro = projetista.projetar_janelado(JanelaHamming())

    # Referência independente usando numpy
    M = 60
    wc = 2 * np.pi * 1200.0 / 8000.0
    n = np.arange(M + 1)
    n_c = n - M / 2.0
    h_ideal_numpy = np.zeros(M + 1)
    for idx, nc_val in enumerate(n_c):
        if abs(nc_val) < 1e-9:
            h_ideal_numpy[idx] = wc / np.pi
        else:
            h_ideal_numpy[idx] = np.sin(wc * nc_val) / (np.pi * nc_val)

    w_hamming_numpy = 0.54 - 0.46 * np.cos(2 * np.pi * n / M)
    h_ref_numpy = h_ideal_numpy * w_hamming_numpy

    coincide_filtro = bool(np.allclose(filtro.coeficientes, h_ref_numpy, atol=1e-10))
    print(f"\n  Validação [Filtro FIR Hamming M=60] vs. NumPy: ", end="")
    if coincide_filtro:
        print("✅ RESULTADOS IDÊNTICOS")
        aprovados += 1
    else:
        print("❌ DIVERGÊNCIA DETECTADA")
    total += 1

    print(f"\n  Resultado: {aprovados}/{total} testes aprovados")

    if aprovados < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
