# ──────────────────────────────────────────────────────────────────────
#  Atividade PDS — Makefile
#  Processamento Digital de Sinais: DFT e FFT
# ──────────────────────────────────────────────────────────────────────

PYTHON    := python3
VENV      := .venv
VENV_BIN  := $(VENV)/bin
PIP       := $(VENV_BIN)/pip
PYTHON_V  := $(VENV_BIN)/python
RESULTADOS := resultados

# ── Cores para output ─────────────────────────────────────────────────
VERDE   := \033[0;32m
AMARELO := \033[0;33m
CIANO   := \033[0;36m
VERMELHO := \033[0;31m
RESET   := \033[0m

.PHONY: help configurar executar ex3 ex4 validar lint limpar

# ── Target padrão ─────────────────────────────────────────────────────
help: ## Exibe esta ajuda
	@echo ""
	@echo "$(CIANO)╔══════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(CIANO)║  Atividade PDS — DFT e FFT — Makefile                       ║$(RESET)"
	@echo "$(CIANO)╚══════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(VERDE)%-14s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ── Configuração do ambiente ───────────────────────────────────────────
$(VENV)/pyvenv.cfg:
	@echo "$(AMARELO)► Criando virtualenv em $(VENV)/...$(RESET)"
	@$(PYTHON) -m venv $(VENV)
	@echo "$(AMARELO)► Instalando dependências...$(RESET)"
	@$(PIP) install --upgrade pip -q
	@$(PIP) install -r requirements.txt -q
	@echo "$(VERDE)✅ Ambiente configurado!$(RESET)"

configurar: $(VENV)/pyvenv.cfg ## Cria o virtualenv e instala dependências

# ── Execução ──────────────────────────────────────────────────────────
executar: configurar ## Executa TODOS os exercícios (1, 2, 3 e 4)
	@echo "$(CIANO)► Executando todos os exercícios...$(RESET)"
	@$(PYTHON_V) main.py

ex1: configurar ## Executa apenas o Exercício 1 (Janelamento, N=512)
	@echo "$(CIANO)► Exercício 1: Janelamento e Resolução Espectral...$(RESET)"
	@$(PYTHON_V) main.py --ex1

ex2: configurar ## Executa apenas o Exercício 2 (Filtro FIR PB, M=60)
	@echo "$(CIANO)► Exercício 2: Projeto de Filtro FIR Passa-Baixas...$(RESET)"
	@$(PYTHON_V) main.py --ex2

ex3: configurar ## Executa apenas o Exercício 3 (DFT/FFT, N=4)
	@echo "$(CIANO)► Exercício 3: DFT e FFT para x[n] = {0,1,2,3}...$(RESET)"
	@$(PYTHON_V) main.py --ex3

ex4: configurar ## Executa apenas o Exercício 4 (FFT, N=8)
	@echo "$(CIANO)► Exercício 4: FFT para x[n] = {0,...,7}...$(RESET)"
	@$(PYTHON_V) main.py --ex4

# ── Validação e qualidade ─────────────────────────────────────────────
validar: configurar ## Valida resultados contra numpy.fft (oráculo de referência)
	@echo "$(CIANO)► Validando implementações contra NumPy...$(RESET)"
	@$(PYTHON_V) validar.py
	@echo "$(VERDE)✅ Validação concluída!$(RESET)"

lint: configurar ## Verifica estilo de código com ruff
	@echo "$(AMARELO)► Verificando estilo com ruff...$(RESET)"
	@$(PIP) install ruff -q
	@$(VENV_BIN)/ruff check pds/ exercicios/ main.py
	@echo "$(VERDE)✅ Lint OK$(RESET)"

# ── Limpeza ───────────────────────────────────────────────────────────
limpar: ## Remove virtualenv, resultados gerados e caches Python
	@echo "$(VERMELHO)► Removendo artefatos...$(RESET)"
	@rm -rf $(VENV) $(RESULTADOS)
	@find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true
	@echo "$(VERDE)✅ Limpeza concluída!$(RESET)"
