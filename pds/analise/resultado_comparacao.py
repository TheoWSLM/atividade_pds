"""
Resultado da comparação entre dois algoritmos de transformada espectral.

Estrutura de dados imutável que encapsula todas as métricas geradas
pelo ComparadorAlgoritmos para serem consumidas pelo GeradorRelatorio.
"""

from dataclasses import dataclass

from ..dominio.resultado_transformada import ResultadoTransformada


@dataclass(frozen=True)
class ResultadoComparacao:
    """
    Agrupa os resultados de dois algoritmos para análise comparativa.

    Atributos:
        resultado_a:          Resultado do primeiro algoritmo.
        resultado_b:          Resultado do segundo algoritmo.
        sequencia_original:   Sequência x[n] usada como entrada.
        resultados_identicos: True se ambos produziram os mesmos coeficientes.
        tolerancia_usada:     Tolerância numérica aplicada na verificação.
    """

    resultado_a: ResultadoTransformada
    resultado_b: ResultadoTransformada
    sequencia_original: tuple[float | int, ...]
    resultados_identicos: bool
    tolerancia_usada: float

    @property
    def aceleracao(self) -> float:
        """
        Aceleração de A em relação a B (razão de tempo de execução).

        Valor > 1 indica que B foi mais rápido que A.
        """
        denominador = max(self.resultado_b.tempo_segundos, 1e-15)
        return self.resultado_a.tempo_segundos / denominador

    @property
    def razao_operacoes(self) -> float:
        """Razão do total de operações de A em relação a B."""
        denominador = max(self.resultado_b.total_operacoes, 1)
        return self.resultado_a.total_operacoes / denominador
