# 📡 Atividade de Processamento Digital de Sinais (PDS)

> **DFT, FFT, Janelamento Espectral e Projeto de Filtros FIR**
> Implementação manual de algoritmos puros de PDS, simulações comparativas e visualizações espectrais de alto nível.

---

## 🏛️ Arquitetura Arquitetural: Fatiamento Vertical (Vertical Slice)

O projeto foi reestruturado seguindo o padrão de **Vertical Slice (Coesão por Funcionalidade)**. Em vez de espalhar a lógica de um mesmo assunto por várias pastas de infraestrutura profunda, agrupamos os componentes de domínio, análise e visualização em módulos coesos e focados:

```
pds/
  ├── transformadas/     → Algoritmos de Fourier, Cooley-Tukey e analise de complexidade (Ex 3 e 4)
  │     ├── calculadoras.py
  │     ├── decomposicao.py
  │     ├── analise.py
  │     └── visualizacao.py
  ├── janelas/           → Implementação de janelas e sinal multitonal (Ex 1)
  │     ├── dominio.py
  │     ├── analise.py
  │     └── visualizacao.py
  └── filtros/           → Projeto de filtros FIR e resposta em frequência (Ex 2)
        ├── dominio.py
        ├── analise.py
        └── visualizacao.py

exercicios/              → Orquestração dos pontos de entrada executáveis
  ├── exercicio1.py      → Janelamento e Resolução Espectral (N=512)
  ├── exercicio2.py      → Projeto de Filtro FIR PB (M=60)
  ├── exercicio3.py      → DFT vs FFT Cooley-Tukey (N=4)
  └── exercicio4.py      → Decomposição Butterfly da FFT Cooley-Tukey (N=8)
```

Essa organização garante **Alta Coesão** e **Baixo Acoplamento**, facilitando a expansão do código e a legibilidade para fins didáticos e práticos.

---

## 🚀 Como Executar

### Pré-requisitos

*   Python 3.10+
*   Gerenciador `make`

### Comandos Disponíveis via `make`

```bash
# Executar TODOS os exercícios (cria o virtualenv automaticamente)
make executar

# Executar apenas o Exercício 1 (Janelamento Espectral)
make ex1

# Executar apenas o Exercício 2 (Projeto de Filtro FIR Passa-Baixas)
make ex2

# Executar apenas o Exercício 3 (Comparação DFT/FFT, N=4)
make ex3

# Executar apenas o Exercício 4 (Butterfly FFT Cooley-Tukey, N=8)
make ex4

# Validar implementações manuais contra referências NumPy
make validar

# Verificar estilo de código e lints (Ruff)
make lint

# Limpar o ambiente de desenvolvimento e arquivos gerados
make limpar
```

---

## 📋 Detalhamento dos Exercícios

| Exercício | Descrição | Fórmulas e Parâmetros | Resultados e Discussão |
| :---: | :--- | :--- | :--- |
| **1** | **Janelamento Espectral** | $x[n] = \cos(0.2\pi n) + 0.1\cos(0.22\pi n)$, $N=512$, $f_s=1\text{ kHz}$. Janelas: Retangular, Triangular, Hann, Hamming, Blackman. | Análise de vazamento espectral. Mostra a necessidade de janelamento para identificar componentes espectrais de baixa amplitude próximas a componentes fortes. |
| **2** | **Projeto de Filtro FIR PB** | Ordem $M=60$, $f_s=8000\text{ Hz}$, $f_c=1200\text{ Hz}$. Resposta ideal: $h_{ideal}[n] = \frac{\sin(\omega_c (n-M/2))}{\pi(n-M/2)}$. | Projeto de filtro passa-baixas digital. Aplicação das 5 janelas sobre os coeficientes ideais e avaliação do trade-off de atenuação na stopband vs banda de transição. |
| **3** | **DFT vs FFT (N=4)** | $x[n] = \{0, 1, 2, 3\}$. Comparação de operações e tempo de execução. | Demonstração matemática de equivalência de coeficientes e cálculo de complexidade operacional. |
| **4** | **Estágios da FFT (N=8)** | $x[n] = \{0, 1, \dots, 7\}$. Bit-reversal e estágios butterfly passo a passo. | Detalhamento completo no console de cada estágio e fator twiddle da FFT. |

---

## 📊 Gráficos Gerados em `./resultados/`

Ao final da execução, os seguintes gráficos são salvos para análise visual:

| Arquivo | Descrição |
| :--- | :--- |
| `ex1_janelas_e_espectros.png` | Formato temporal das janelas, sinais janelados e espectro de magnitude em dB com zoom na faixa de interesse (50 a 160 Hz) demonstrando o vazamento e resolução de tons. |
| `ex2_resposta_filtros.png` | Coeficientes $h[n]$ do filtro FIR projetado e resposta de magnitude em frequência em dB de $0$ a $4000\text{ Hz}$ com destaque para $f_c = 1200\text{ Hz}$. |
| `ex3_dft_espectro.png` / `ex3_fft_espectro.png` | Magnitude e fase das transformadas DFT e FFT para $N=4$. |
| `ex4_fft_espectro_n8.png` | Espectro e verificação de simetria conjugada para $N=8$. |
| `comparacao_complexidade.png` | Curvas de contagem de operações reais vs. curvas teóricas em escala log-log para $N=2$ até $256$. |

---

## 🧠 Discussão Teórica dos Resultados

### 1. Efeitos de Janelamento (Exercício 1)

O sinal de teste possui uma componente forte em $100\text{ Hz}$ ($A_1=1.0$) e uma componente fraca em $110\text{ Hz}$ ($A_2=0.1$, ou $-20\text{ dB}$).
*   **Retangular**: Possui o lóbulo principal mais estreito (2 bins), mas o lóbulo lateral elevado ($-13\text{ dB}$) causa um vazamento espectral violento. Esse vazamento encobre completamente a componente fraca em $110\text{ Hz}$, que fica invisível sob os lóbulos da componente principal.
*   **Hann & Hamming**: Aumentam o lóbulo principal para 4 bins, mas reduzem drasticamente os lóbulos laterais ($-32\text{ dB}$ para Hann, $-43\text{ dB}$ para Hamming). Ambas as janelas reduzem o vazamento a ponto de revelar com clareza o pico de $-20\text{ dB}$ em $110\text{ Hz}$.
*   **Blackman**: Oferece o menor lóbulo lateral ($-58\text{ dB}$), porém seu lóbulo principal é muito largo (6 bins). Como a distância espectral das frequências é de apenas 5.12 bins, a largura do lóbulo de Blackman faz com que as duas frequências se fundam em um único pico largo na imagem espectral, impedindo a separação visual dos tons.

**Equilíbrio**: Hann e Hamming fornecem a melhor resolução prática para este cenário.

---

### 2. Projeto de Filtro FIR (Exercício 2)

O janelamento da resposta ao impulso ideal do filtro FIR também explicita esse trade-off clássico de projeto:
*   **Janela Retangular**: Gera o filtro com a transição mais íngreme (banda de transição teórica de $120.0\text{ Hz}$), mas a atenuação na banda de rejeição é de apenas $-21\text{ dB}$. Frequências indesejadas na stopband passam com ganho considerável.
*   **Janela de Hamming**: Oferece uma banda de transição de $440\text{ Hz}$, porém com atenuação prática de $-53.7\text{ dB}$ na banda de rejeição, limpando com extrema eficiência as altas frequências acima da zona de corte.
*   **Janela de Blackman**: Produz uma transição bastante suave (banda de transição de $733.3\text{ Hz}$), mas atinge uma atenuação incrível de $-75.2\text{ dB}$ na banda de rejeição.

**Conclusão**: O uso da janela de **Hamming** representa o padrão de projeto mais equilibrado na engenharia de sinal por oferecer corte rápido o suficiente com altos níveis de atenuação na banda de rejeição.
