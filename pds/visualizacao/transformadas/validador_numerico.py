"""
Validação numérica de coeficientes espectrais contra a implementação
de referência do NumPy.

Compara nossos resultados com a referência da biblioteca e reporta divergências.
Nenhuma lógica de cálculo ou apresentação visual ocorre aqui.
"""

import numpy as np


class ValidadorNumerico:
    """
    Compara coeficientes calculados manualmente com numpy.fft.fft.

    O NumPy é usado exclusivamente como oráculo de referência —
    o cálculo da DFT/FFT é feito inteiramente pelas nossas classes.
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
        """
        Valida nossos coeficientes contra numpy.fft.fft.

        Imprime o resultado da comparação no terminal e,
        em caso de divergência, exibe quais índices divergiram.

        Args:
            sequencia:           Sequência de entrada original.
            coeficientes_nossos: Coeficientes calculados pela nossa implementação.
            nome_algoritmo:      Nome para identificar a implementação no log.

        Returns:
            True se todos os coeficientes coincidem dentro da tolerância.
        """
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
        referencia: "np.ndarray",
    ) -> None:
        """Exibe os índices onde ocorreram divergências."""
        for k, (nosso, ref) in enumerate(zip(nossos, referencia)):
            diferenca = abs(nosso - ref)
            if diferenca > self._tolerancia:
                print(
                    f"    k={k}: calculado={nosso:.6f}, "
                    f"numpy={ref:.6f}, "
                    f"diferença={diferenca:.2e}"
                )
