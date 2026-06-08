"""
Demonstração passo a passo da decomposição butterfly do algoritmo
Cooley-Tukey (Decimação no Tempo).

A lógica de explicar/visualizar o algoritmo
é separada da lógica de calculá-lo (que fica na CalculadoraFFT).
"""

import cmath
import math


class DecomposicaoButterfly:
    """
    Simula e exibe cada estágio da FFT Cooley-Tukey de forma didática.

    Mostra:
    - O reordenamento bit-reversal inicial
    - Cada estágio com seus fatores twiddle e operações butterfly
    - O estado intermediário dos coeficientes após cada estágio
    """

    @staticmethod
    def inverter_bits(numero: int, quantidade_bits: int) -> int:
        """
        Inverte os bits de um número inteiro (bit-reversal).

        Utilizado para reordenar as amostras antes dos estágios butterfly,
        colocando cada amostra na posição correta.

        Exemplo para 3 bits:
            0 (000) → 0 (000)
            1 (001) → 4 (100)
            2 (010) → 2 (010)
            3 (011) → 6 (110)
        """
        acumulador = 0
        for _ in range(quantidade_bits):
            acumulador = (acumulador << 1) | (numero & 1)
            numero >>= 1
        return acumulador

    def calcular_indices_bit_reversal(
        self, tamanho: int, num_estagios: int
    ) -> list[int]:
        """Retorna a lista de índices reordenados por bit-reversal."""
        return [self.inverter_bits(i, num_estagios) for i in range(tamanho)]

    def exibir(self, sequencia: list[float | int]) -> None:
        """
        Executa e imprime cada estágio da decomposição butterfly.

        Args:
            sequencia: Sequência de entrada x[n]. Comprimento deve ser potência de 2.
        """
        tamanho = len(sequencia)
        num_estagios = int(math.log2(tamanho))

        print(f"\n  ┌─ DECOMPOSIÇÃO COOLEY-TUKEY (N = {tamanho}, {num_estagios} estágios)")
        print(f"  │")
        print(f"  │  Entrada: x[n] = {list(sequencia)}")
        print(f"  │")

        # Reordenamento bit-reversal
        indices_reordenados = self.calcular_indices_bit_reversal(tamanho, num_estagios)
        sequencia_reordenada = [sequencia[indices_reordenados[i]] for i in range(tamanho)]

        print(f"  │  Reordenamento bit-reversal:")
        print(f"  │    Índices originais:    {list(range(tamanho))}")
        print(f"  │    Índices reordenados:  {indices_reordenados}")
        print(f"  │    Sequência reordenada: {list(sequencia_reordenada)}")
        print(f"  │")

        # Simular os estágios butterfly
        coeficientes_atuais = [complex(amostra) for amostra in sequencia_reordenada]

        for estagio in range(1, num_estagios + 1):
            tamanho_bloco = 2 ** estagio
            metade_bloco = tamanho_bloco // 2

            print(f"  ├─ Estágio {estagio} (blocos de tamanho {tamanho_bloco}):")

            for inicio_bloco in range(0, tamanho, tamanho_bloco):
                for k in range(metade_bloco):
                    # Fator twiddle do butterfly
                    angulo = -2 * cmath.pi * k / tamanho_bloco
                    fator_twiddle = cmath.exp(complex(0, angulo))

                    indice_superior = inicio_bloco + k
                    indice_inferior = inicio_bloco + k + metade_bloco

                    # Operação butterfly
                    superior = coeficientes_atuais[indice_superior]
                    produto = fator_twiddle * coeficientes_atuais[indice_inferior]

                    coeficientes_atuais[indice_superior] = superior + produto
                    coeficientes_atuais[indice_inferior] = superior - produto

                    print(
                        f"  │    Butterfly({indice_superior}, {indice_inferior}): "
                        f"W_{tamanho_bloco}^{k} = e^(-j·2π·{k}/{tamanho_bloco}) = "
                        f"{fator_twiddle.real:+.4f}{fator_twiddle.imag:+.4f}j"
                    )

            # Estado intermediário após o estágio
            valores_formatados = [
                f"{c.real:+.2f}{c.imag:+.2f}j" for c in coeficientes_atuais
            ]
            print(f"  │    Estado: {valores_formatados}")
            print(f"  │")

        # Resultado final
        print(f"  └─ Coeficientes finais X[k]:")
        for k, coeficiente in enumerate(coeficientes_atuais):
            print(
                f"       X[{k}] = {coeficiente.real:+8.4f}{coeficiente.imag:+8.4f}j  "
                f"|X[{k}]| = {abs(coeficiente):8.4f}"
            )
