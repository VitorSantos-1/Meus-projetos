#-------------------------------------------------------------------------------------------------------------------------
# EXERCICIO ####
# CALCULANDO O TAMANHO DA AMOSTRA E SIMULAR A ESTIMATIVA

# Cenário: Imagine-se como analista de qualidade em uma fábrica de eletrônicos que precisa avaliar a proporção de
# produtos defeituosos em uma linha de produção. A fábrica produz 10.000 unidades por dia.
# Você decide usar amostragem para estimar a proporção de produtos defeituosos com alta precisão.

# PARTE 1: CÁLCULO DO TAMANHO DA AMOSTRA

# Definindo os parâmetros do problema para o cálculo do tamanho da amostra:
N  <- 10000     # Tamanho total da população (10.000 unidades produzidas diariamente).
Z  <- 1.96      # Valor Z para 95% de confiança (1.96 é o valor crítico para um nível de confiança de 95%).
p  <- 0.05      # Proporção esperada de defeituosos na população (5% ou 0.05).
e  <- 0.01      # Erro amostral máximo tolerável (margem de erro de 1% ou 0.01).

# 1. Calculando o tamanho da amostra para proporção (considerando população "infinita" inicialmente):
# Esta é a primeira aproximação do tamanho da amostra, sem considerar o tamanho limitado da população.
# Fórmula: n_inf = (Z^2 * p * (1 - p)) / (e^2)
n_inf <- (Z^2 * p * (1 - p)) / (e^2)
print(n_inf)

# 2. Ajustando para a população finita:
# Como a população é finita (10.000 unidades), aplicamos uma correção para obter um tamanho de amostra mais preciso.
# Fórmula: n_aj = (n_inf * N) / (n_inf + (N - 1))
n_aj <- (n_inf * N) / (n_inf + (N - 1))
print(n_aj)

# 3. Arredondando o tamanho da amostra para cima:
# Arredondamos o valor para o próximo número inteiro para garantir que tenhamos o mínimo necessário de observações.
n_ajustado <- ceiling(n_aj)
print(n_ajustado)

# -------------------------------------------------------------------------------------------------------------------------
# FUNÇÃO PARA CALCULAR O TAMANHO DA AMOSTRA (PARA REAPROVEITAMENTO)

# Esta função encapsula os cálculos acima, permitindo que você os reutilize facilmente com diferentes parâmetros.
# Ela recebe o tamanho da população (N) e, opcionalmente, Z, p e e (com valores padrão já definidos).
# A função retorna o tamanho da amostra ajustado e arredondado para cima.
tamanho_amostra_prop <- function(N,
                                 Z = 1.96,
                                 p = 0.05,
                                 e = 0.01) {
  # Calcula o tamanho da amostra inicial (população infinita)
  n_inf <- (Z^2 * p * (1 - p)) / (e^2)
  
  # Aplica a correção para população finita
  n_aj  <- (n_inf * N) / (n_inf + (N - 1))
  
  # Arredonda o resultado para cima e o retorna
  ceiling(n_aj)
}

# Exemplo de como usar a função com os parâmetros do problema:
# tamanho_amostra_prop(N = 10000, Z = 1.96, p = 0.05, e = 0.01)
# Este comando também retornaria 1544.

# -------------------------------------------------------------------------------------------------------------------------
# PARTE 2: SIMULAÇÃO DA AMOSTRAGEM E ESTIMATIVA DA PROPORÇÃO

# Para garantir que os resultados da simulação sejam os mesmos toda vez que você rodar o código,
# usamos 'set.seed()'. Isso é útil para reprodutibilidade de experimentos.
set.seed(123)

# Definindo os parâmetros para a simulação da amostragem:
N  <- 10000         # Tamanho da população (10.000 unidades).
n  <- n_ajustado    # Tamanho da amostra ajustado, calculado anteriormente (1544).
p_real <- 0.05      # Proporção "real" de defeituosos na população (5% ou 0.05).
# Em um cenário real, o p_real seria desconhecido; aqui, é usado para simular a população.

# 1. Criando a população para simulação:
# 'rbinom(N, size = 1, prob = p_real)' gera N valores (0 ou 1).
# Onde '1' representa um item defeituoso e '0' um item bom, com a probabilidade 'p_real' de ser defeituoso.
populacao <- rbinom(N,
                    size = 1,
                    prob = p_real)

# 2. Realizando uma amostragem aleatória simples sem reposição:
# 'sample(1:N, size = n, replace = FALSE)' seleciona 'n' índices únicos da população.
# Usamos esses índices para extrair os itens correspondentes da população original.
indices_amostra <- sample(1:N,
                          size = n,
                          replace = FALSE)

# A 'amostra' agora contém os 1544 itens selecionados (0s e 1s) que serão analisados.
amostra <- populacao[indices_amostra]
print(amostra) # Exibe os primeiros itens da amostra (0 para bom, 1 para defeituoso).

# 3. Coletando dados e calculando a proporção de defeitos na amostra:
# 'sum(amostra)' soma todos os '1s' na amostra, que representam os itens defeituosos.
defeituosos <- sum(amostra)
print(defeituosos) # Exibe o número total de itens defeituosos encontrados na amostra (neste caso, 68).

# Calculando a proporção de defeituosos na amostra:
# p_amostral = (número de defeituosos) / (tamanho da amostra)
p_amostral <- defeituosos / n
print(p_amostral) # Exibe a proporção de defeituosos na amostra (aproximadamente 0.04404145 ou 4.40%).

# 4. Inferindo para a população:
# Com base na proporção amostral de 0.0440, podemos inferir que a proporção de produtos defeituosos
# na população de 10.000 unidades é, aproximadamente, 4.40%.

# -------------------------------------------------------------------------------------------------------------------------
# CÁLCULO DO INTERVALO DE CONFIANÇA DE 95% PARA A PROPORÇÃO

# Definindo o nível de significância (alpha):
alpha <- 0.05

# Calculando o valor Z para um intervalo de confiança de 95%:
# 'qnorm(1 - alpha/2)' retorna o valor Z correspondente (aproximadamente 1.96).
Z_ic <- qnorm(1 - alpha/2)

# Calculando o erro padrão da proporção amostral:
# Fórmula: erro_padrao = sqrt(p_amostral * (1 - p_amostral) / n)
erro_padrao <- sqrt(p_amostral * (1 - p_amostral) / n)

# Calculando o limite inferior do intervalo de confiança:
lim_inf <- p_amostral - Z_ic * erro_padrao

# Calculando o limite superior do intervalo de confiança:
lim_sup <- p_amostral + Z_ic * erro_padrao

# Exibindo o intervalo de confiança:
print(c(lim_inf, lim_sup)) # O intervalo de confiança é aproximadamente [0.0338, 0.0543].

# Este intervalo nos dá uma faixa de valores onde a verdadeira proporção populacional
# de defeituosos provavelmente se encontra, com 95% de confiança.
# Ou seja, temos 95% de confiança de que a proporção real de defeituosos na população
# está entre 3.38% e 5.43%.