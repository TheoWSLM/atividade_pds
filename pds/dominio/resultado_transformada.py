"""
Estrutura de dados compartilhada que representa o resultado
de qualquer transformada espectral (DFT, FFT, DCT, etc.).

Apenas os campos comuns a todas as transformadas
pertencem a esta classe. Campos específicos de cada algoritmo
(ex: num_estagios da FFT) devem ficar em subclasses.
"""

from dataclasses import dataclass


@dataclass
class ResultadoTransformada:
    """
    Resultado genérico de uma transformada espectral discreta.

    Atributos:
        nome_algoritmo:      Identificador legível (ex: "DFT", "FFT Cooley-Tukey").
        tamanho:             N — comprimento da sequência de entrada.
        coeficientes:        X[k] para k = 0, ..., N-1 (números complexos).
        magnitudes:          |X[k]| — espectro de amplitude.
        fases:               ∠X[k] em radianos — espectro de fase.
        multiplicacoes:      Quantidade de multiplicações complexas realizadas.
        somas:               Quantidade de somas complexas realizadas.
        tempo_segundos:      Tempo de execução do cálculo em segundos.
    """

    nome_algoritmo: str
    tamanho: int
    coeficientes: list[complex]
    magnitudes: list[float]
    fases: list[float]
    multiplicacoes: int
    somas: int
    tempo_segundos: float

    @property
    def total_operacoes(self) -> int:
        """Soma de multiplicações e somas complexas."""
        return self.multiplicacoes + self.somas

    @property
    def tempo_microssegundos(self) -> float:
        """Tempo de execução convertido para microssegundos."""
        return self.tempo_segundos * 1_000_000

    def formatar_coeficiente(self, indice: int) -> str:
        """Retorna X[k] formatado como string para exibição."""
        coef = self.coeficientes[indice]
        mag = self.magnitudes[indice]
        fase = self.fases[indice]
        return (
            f"X[{indice}] = {coef.real:+8.4f} {coef.imag:+8.4f}j  "
            f"|X[{indice}]| = {mag:8.4f}  "
            f"∠X[{indice}] = {fase:+8.4f} rad"
        )

    def __str__(self) -> str:
        separador = "=" * 60
        linhas = [
            separador,
            f"  RESULTADO {self.nome_algoritmo} (N = {self.tamanho})",
            separador,
        ]
        for indice in range(self.tamanho):
            linhas.append(f"  {self.formatar_coeficiente(indice)}")
        linhas.extend([
            "─" * 60,
            f"  Multiplicações complexas: {self.multiplicacoes}",
            f"  Somas complexas:          {self.somas}",
            f"  Total de operações:       {self.total_operacoes}",
            f"  Tempo de execução:        {self.tempo_microssegundos:.2f} µs",
            separador,
        ])
        return "\n".join(linhas)
