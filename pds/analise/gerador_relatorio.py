"""
Gerador de relatório textual para comparação entre algoritmos.

Transforma um ResultadoComparacao em texto formatado para o terminal.
Nenhuma lógica de cálculo acontece aqui.
"""

import math

from tabulate import tabulate

from .resultado_comparacao import ResultadoComparacao


class GeradorRelatorio:
    """
    Formata e imprime o relatório comparativo de dois algoritmos.

    Produz tabelas de:
    - Coeficientes espectrais (DFT vs FFT)
    - Contagem de operações (real vs teórica)
    - Tempo de execução e aceleração
    - Complexidade computacional
    - Verificação de corretude
    """

    LARGURA_SEPARADOR = 70

    def gerar(self, comparacao: ResultadoComparacao) -> str:
        """
        Gera o relatório completo como string.

        Args:
            comparacao: Resultado produzido pelo ComparadorAlgoritmos.

        Returns:
            String multilinha com o relatório formatado.
        """
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

    # ── Seções privadas ──────────────────────────────────────────────

    def _secao_coeficientes(self, comparacao: ResultadoComparacao) -> str:
        """Tabela com os coeficientes espectrais dos dois algoritmos."""
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
        """Tabela comparando operações reais versus teóricas."""
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
        """Tabela de tempo de execução e aceleração."""
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
        """Tabela de complexidade computacional teórica."""
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
        """Informa se os coeficientes dos dois algoritmos coincidem."""
        icone = "✅ IDÊNTICOS" if comparacao.resultados_identicos else "❌ DIVERGÊNCIA"
        mensagem = (
            f"    Coeficientes idênticos (tolerância: {comparacao.tolerancia_usada})."
            if comparacao.resultados_identicos
            else "    ATENÇÃO: os coeficientes diferem além da tolerância!"
        )
        return f"  ┌─ VERIFICAÇÃO DE CORRETUDE: {icone}\n{mensagem}"
