library(dplyr)
library(DescTools)

# Produção
prod_1 <- 0.70
prod_2 <- 0.30

# Taxa de erro
prob_1 <- 0.05
prob_2 <- 0.10

# 3. Calcular a PROPORÇÃO REAL de defeitos que cada máquina gera
def_1 <- prod_1 * prob_1
def_2 <- prod_2 * prob_2

# 4. Total de defeitos (Denominador
total_def <- def_1 + def_2

# 5. A Resposta (Bayes): A parte da A dividido pelo todo
resultado <- def_1 / total_def
print(resultado)

dado <- data.frame(
  vendas = c(50, 45, 60, 55, 70, 65, 80, 75, 90, 85, 100, 95),
  mes = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
print(dado)

mediana_vendas <- dado %>%
  pull(vendas) %>%
  median()
print(mediana_vendas)

media_vendas <- dado %>%
  pull(vendas) %>%
  mean()
print(media_vendas)

desvio <- sd(dado$vendas)
print(desvio)

moda <- sort(table(dado$vendas), decreasing = TRUE)
print(moda[1])

dado_1 <- data.frame(
  alturas = c(160, 170, 165, 155, 180.),
  pessoas = c(1, 2, 3, 4, 5))
print(dado_1)

mediana_alturas <- dado_1 %>%
  pull(alturas) %>%
  median()
print(mediana_alturas)

media_alturas <- dado_1 %>%
  pull(alturas) %>%
  mean()
print(media_alturas)

desvio <- sd(dado_1$alturas)
print(desvio)

moda <- sort(table(dado_1$alturas), decreasing = TRUE)
print(moda[1])

variancia <- var(dado_1$alturas)
print(variancia)