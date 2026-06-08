# 📡 Atividade de Processamento Digital de Sinais (PDS)

> **DFT e FFT — Implementação manual, comparação de complexidade e visualização espectral**

---

## 📥 Como Clonar e Configurar

Para rodar este projeto em qualquer computador, primeiro faça o clone do repositório e acesse a pasta do projeto:

```bash
# Clone este repositório
git clone https://github.com/TheoWSLM/atividade_pds.git

# Acesse o diretório do projeto
cd atividade_pds
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10+
- `make`

### Execução

```bash
# Executar TODOS os exercícios (cria virtualenv automaticamente)
make executar

# Exercício 3 apenas (DFT/FFT, N=4)
make ex3

# Exercício 4 apenas (FFT, N=8)
make ex4

# Validar resultados contra numpy.fft.fft
make validar

# Verificar estilo de código
make lint

# Limpar ambiente e resultados gerados
make limpar

# Ver todos os comandos
make help
```

### Execução manual (sem Make)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py           # Todos os exercícios
python main.py --ex3     # Apenas Exercício 3
python main.py --ex4     # Apenas Exercício 4
python validar.py        # Validação contra NumPy
```

---

| Exercício | Entrada | O que faz |
|:---------:|---------|-----------|
| **3** | `x[n] = {0, 1, 2, 3}` — N=4 | Calcula DFT e FFT, compara operações, tempo e complexidade |
| **4** | `x[n] = {0, 1, 2, 3, 4, 5, 6, 7}` — N=8 | Calcula FFT com decomposição butterfly passo a passo |

---

## 📊 Saídas

Os gráficos são salvos automaticamente em `./resultados/`:

| Arquivo | Conteúdo |
|---------|----------|
| `ex3_dft_espectro.png` | Sinal, magnitude e fase da DFT (N=4) |
| `ex3_fft_espectro.png` | Sinal, magnitude e fase da FFT (N=4) |
| `ex4_fft_espectro_n8.png` | Sinal, magnitude e fase da FFT (N=8) |
| `comparacao_complexidade.png` | Curvas DFT × FFT para N = 2 até 256 (log-log) |

---

## 🏛️ Arquitetura de Camadas

```
exercicios/                       → Orquestra chamadas às camadas abaixo
    ↓ usa
pds/analise/transformadas/        → Compara resultados e gera relatório textual
    ↓ usa
pds/dominio/transformadas/        → Algoritmos puros (DFT, FFT, Butterfly)
    ↓ produz
ResultadoTransformada             → Dado imutável que flui entre as camadas

pds/visualizacao/transformadas/   → Gráficos (PNG) e validação (NumPy)
    ↑ consumida diretamente pelos exercícios
```

---

## 📦 Dependências

| Pacote | Versão | Uso |
|--------|--------|-----|
| `numpy` | ≥ 1.24 | **Validação apenas** — comparar com `np.fft.fft` |
| `matplotlib` | ≥ 3.7 | Geração dos gráficos PNG |
| `tabulate` | ≥ 0.9 | Formatação das tabelas no relatório |

> **Nota:** Todo o cálculo da DFT e FFT usa apenas a biblioteca padrão do Python (`cmath`, `math`, `time`). NumPy é usado exclusivamente como oráculo de referência na validação.
