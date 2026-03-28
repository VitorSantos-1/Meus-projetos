media_populacao <- 0.05                       # media da populacao
media_amostra <- 0.07                         # media da amostra
desvio_padrao_populacao <- 0.02              #desvio padrao conhecido

n <- 50                                      # tamanho da amostra

# fazendo o teste z
z_test <- (media_amostra - media_populacao) / (desvio_padrao_populacao / sqrt(n))
z_test

# fazendo o p-valor
p_valor <- 2* (1- pnorm(abs(z_test)))
p_valor

# nesse caso, um z_test alto sugere uma diferença significativa(quanto maior o z_test maior a diferença)
# entre a media_amostra e media_populacao.
# assim rejeitamos a Hipotese nula, pq ha diferença entre as medias


# fazendo o teste t

vendas_a <- c(150, 160, 145, 170, 155)
vendas_b <- c(180, 175, 165, 160, 170)

# t_test nas duas amostra
t_test <- t.test(vendas_a, vendas_b)
t_test


# p_valor < 0.05, no caso hipotese nula rejeitada pq as vendas sao diferentes
