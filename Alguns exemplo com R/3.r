# Calculando a probabilidade de peça defeituosa

# fornecedor1
p_def_f1 <- 0.05
# fornecedor2
p_def_f2 <- 0.10

# A probabilidade de escolher o fornecedor 1 e 2
p_f1 <- 0.60
p_f2 <- 0.40

# Calculando a probabilidade total de peça defeituosa
p_defeituosa <- p_f1 * p_def_f1 + p_f2 * p_def_f2
print(p_defeituosa)