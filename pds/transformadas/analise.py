"""
Análise comparativa de desempenho e corretude entre DFT e FFT.
"""

from dataclasses import dataclass
import math
from tabulate import tabulate

from .calculadoras import ProtocoloTransformada, ResultadoTransformada


@dataclass(frozen=True)
class ResultadoComparacao:
    """
    Agrupa os resultados de dois algoritmos para análise comparativa.
    """

    resultado_a: ResultadoTransformada
    resultado_b: ResultadoTransformada
    sequencia_original: tuple[float | int, ...]
    resultados_identicos: bool
    tolerancia_usada: float

    @property
    def aceleracao(self) -> float:
        """Aceleração de A em relação a B (razão de tempo de execução)."""
        denominador = max(self.resultado_b.tempo_segundos, 1e-15)
        return self.resultado_a.tempo_segundos / denominador

    @property
    def razao_operacoes(self) -> float:
        """Razão do total de operações de A em relação a B."""
        denominador = max(self.resultado_b.total_operacoes, 1)
        return self.resultado_a.total_operacoes / denominador


class ComparadorAlgoritmos:
    """
    Executa dois algoritmos sobre a mesma entrada e mede suas diferenças.
    """

    TOLERANCIA_PADRAO = 1e-10

    def __init__(
        self,
        algoritmo_a: ProtocoloTransformada,
        algoritmo_b: ProtocoloTransformada,
        tolerancia: float = TOLERANCIA_PADRAO,
    ) -> None:
        self._algoritmo_a = algoritmo_a
        self._algoritmo_b = algoritmo_b
        self._tolerancia = tolerancia

    def _coeficientes_coincidem(self, coefs_a: list[complex], coefs_b: list[complex]) -> bool:
        """Verifica se dois conjuntos de coeficientes são numericamente equivalentes."""
        if len(coefs_a) != len(coefs_b):
            return False

        return all(
            abs(coef_a - coef_b) <= self._tolerancia
            for coef_a, coef_b in zip(coefs_a, coefs_b)
        )

    def comparar(self, sequencia: list[float | int]) -> ResultadoComparacao:
        """Executa ambos os algoritmos e retorna as métricas comparativas."""
        resultado_a = self._algoritmo_a.calcular(sequencia)
        resultado_b = self._algoritmo_b.calcular(sequencia)

        coincide = self._coeficientes_coincidem(
            resultado_a.coeficientes,
            resultado_b.coeficientes,
        )

        return ResultadoComparacao(
            resultado_a=resultado_a,
            resultado_b=resultado_b,
            sequencia_original=tuple(sequencia),
            resultados_identicos=coincide,
            tolerancia_usada=self._tolerancia,
        )


class GeradorRelatorio:
    """
    Formata e imprime o relatório comparativo de dois algoritmos.
    """

    LARGURA_SEPARADOR = 70

    def gerar(self, comparacao: ResultadoComparacao) -> str:
        """Gera o relatório completo como string."""
        N = comparacao.resultado_a.tamanho
        sequencia = list(comparacao.sequencia_original)
        sep = "═" * self.LARGURA_SEPARADOR

        secoes = [
            "",
            sep,
            f"  COMPARAÇÃO: {comparacao.resultado_a.nome_algoritmo} × "
            f"{comparacao.resultado_b.nome_algoritmo}",
            f"  Entrada: x[n] = {sequencia}  (N = {N})",
            sep,
            "",
            self._secao_coeficientes(comparacao),
            "",
            self._secao_operacoes(comparacao),
            "",
            self._secao_tempo(comparacao),
            "",
            self._secao_complexidade(comparacao),
            "",
            self._secao_corretude(comparacao),
            "",
            sep,
        ]

        return "\n".join(secoes)

    def imprimir(self, comparacao: ResultadoComparacao) -> None:
        """Imprime o relatório diretamente no terminal."""
        print(self.gerar(comparacao))

    def _secao_coeficientes(self, comparacao: ResultadoComparacao) -> str:
        N = comparacao.resultado_a.tamanho
        cabecalhos = [
            "k",
            f"X_{comparacao.resultado_a.nome_algoritmo[:3]}[k]",
            f"X_{comparacao.resultado_b.nome_algoritmo[:3]}[k]",
            "|X[k]|",
            "∠X[k] (rad)",
        ]
        linhas = []
        for k in range(N):
            coef_a = comparacao.resultado_a.coeficientes[k]
            coef_b = comparacao.resultado_b.coeficientes[k]
            linhas.append([
                k,
                f"{coef_a.real:+.4f}{coef_a.imag:+.4f}j",
                f"{coef_b.real:+.4f}{coef_b.imag:+.4f}j",
                f"{comparacao.resultado_a.magnitudes[k]:.4f}",
                f"{comparacao.resultado_a.fases[k]:+.4f}",
            ])
        return (
            "  ┌─ COEFICIENTES ESPECTRAIS\n"
            + tabulate(linhas, headers=cabecalhos, tablefmt="simple_outline")
        )

    def _secao_operacoes(self, comparacao: ResultadoComparacao) -> str:
        N = comparacao.resultado_a.tamanho
        log2N = int(math.log2(N)) if N > 1 else 0

        mult_a_teorica = N * N
        soma_a_teorica = N * (N - 1)
        mult_b_teorica = (N // 2) * log2N if N > 1 else 0
        soma_b_teorica = N * log2N if N > 1 else 0

        res_a = comparacao.resultado_a
        res_b = comparacao.resultado_b

        cabecalhos = [
            "Operação", "A (real)", "A (teórica)", "B (real)", "B (teórica)", "Razão A/B"
        ]
        linhas = [
            [
                "Multiplicações",
                res_a.multiplicacoes,
                f"N² = {mult_a_teorica}",
                res_b.multiplicacoes,
                f"(N/2)·log₂N = {mult_b_teorica}",
                f"{res_a.multiplicacoes / max(res_b.multiplicacoes, 1):.1f}×",
            ],
            [
                "Somas",
                res_a.somas,
                f"N·(N-1) = {soma_a_teorica}",
                res_b.somas,
                f"N·log₂N = {soma_b_teorica}",
                f"{res_a.somas / max(res_b.somas, 1):.1f}×",
            ],
            [
                "Total",
                res_a.total_operacoes,
                mult_a_teorica + soma_a_teorica,
                res_b.total_operacoes,
                mult_b_teorica + soma_b_teorica,
                f"{comparacao.razao_operacoes:.1f}×",
            ],
        ]
        return (
            "  ┌─ CONTAGEM DE OPERAÇÕES\n"
            + tabulate(linhas, headers=cabecalhos, tablefmt="simple_outline")
        )

    def _secao_tempo(self, comparacao: ResultadoComparacao) -> str:
        res_a = comparacao.resultado_a
        res_b = comparacao.resultado_b
        linhas = [
            [res_a.nome_algoritmo, f"{res_a.tempo_microssegundos:.2f} µs"],
            [res_b.nome_algoritmo, f"{res_b.tempo_microssegundos:.2f} µs"],
            ["Aceleração (A/B)", f"{comparacao.aceleracao:.2f}×"],
        ]
        return (
            "  ┌─ TEMPO DE EXECUÇÃO\n"
            + tabulate(linhas, headers=["Método", "Tempo"], tablefmt="simple_outline")
        )

    def _secao_complexidade(self, comparacao: ResultadoComparacao) -> str:
        N = comparacao.resultado_a.tamanho
        log2N = int(math.log2(N)) if N > 1 else 0
        N_log2N = N * log2N

        linhas = [
            ["DFT", "O(N²)", f"O({N}²) = O({N**2})"],
            ["FFT", "O(N·log₂N)", f"O({N}·{log2N}) = O({N_log2N})"],
            [
                "Redução",
                "—",
                f"{N**2 / max(N_log2N, 1):.1f}× menos operações",
            ],
        ]
        return (
            "  ┌─ COMPLEXIDADE COMPUTACIONAL\n"
            + tabulate(
                linhas,
                headers=["Método", "Complexidade", f"Para N={N}"],
                tablefmt="simple_outline",
            )
        )

    def _secao_corretude(self, comparacao: ResultadoComparacao) -> str:
        icone = "✅ IDÊNTICOS" if comparacao.resultados_identicos else "❌ DIVERGÊNCIA"
        mensagem = (
            f"    Coeficientes idênticos (tolerância: {comparacao.tolerancia_usada})."
            if comparacao.resultados_identicos
            else "    ATENÇÃO: os coeficientes diferem além da tolerância!"
        )
        return f"  ┌─ VERIFICAÇÃO DE CORRETUDE: {icone}\n{mensagem}"
