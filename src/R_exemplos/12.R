#-------------------------------------------------------------------------------------------------------------------------

# FDP ####
# Definindo a sequência de valores para a variável x
x <- seq(-4, 4, by = 0.01)

# Calculando a densidade de probabilidade para uma distribuição normal com média 0 e desvio padrão 1
densidade <- dnorm(x, mean = 0, sd = 1)

# Plotando a função de densidade
plot(x, densidade, type = "l", main = "Função de Densidade de Probabilidade Normal", ylab = "Densidade", xlab = "Valores")

#-------------------------------------------------------------------------------------------------------------------------

# FDA ####
# Calculando a função de distribuição acumulada para a mesma distribuição normal
fda <- pnorm(x, mean = 0, sd = 1)

# Plotando a função de distribuição acumulada
plot(x, fda, type = "l", main = "Função de Distribuição Acumulada Normal", 
     ylab = "Probabilidade Acumulada", xlab = "Valores")

#-------------------------------------------------------------------------------------------------------------------------

# DISTRIBUIÇÃO NORMAL ####
# Gerando uma amostra de 1000 dados de uma distribuição normal com média 50 e desvio padrão 10
dados_normais <- rnorm(1000, mean = 50, sd = 10)

# Plotando o histograma dos dados gerados
hist(dados_normais, breaks = 30, col = "lightblue", main = "Histograma de Dados Normais", 
     xlab = "Valores", ylab = "Frequência")

#-------------------------------------------------------------------------------------------------------------------------

# Simulando 1000 experimentos binomiais com 10 tentativas e probabilidade de sucesso 0.5
dados_binomiais <- rbinom(1000, size = 10, prob = 0.5)

# Plotando o histograma dos dados gerados
hist(dados_binomiais, breaks = 10, col = "lightgreen", main = "Histograma de Distribuição Binomial", 
     xlab = "Número de Sucessos", ylab = "Frequência")

#-------------------------------------------------------------------------------------------------------------------------

# DISTRIBUIÇÃO T STUDENT ####
# Gerando uma amostra de 1000 dados de uma distribuição t com 10 graus de liberdade
dados_t <- rt(1000, df = 10)

# Plotando o histograma dos dados gerados
hist(dados_t, breaks = 30, col = "lightcoral", main = "Histograma de Distribuição t de Student", 
     xlab = "Valores", ylab = "Frequência")

#-------------------------------------------------------------------------------------------------------------------------
# COMPARAÇÃO DE DISTRIBUIÇÕES ####

# Gerando os dados para as distribuições
x <- seq(-4, 4, by = 0.01)
densidade_normal <- dnorm(x)
densidade_t <- dt(x, df = 10)
# Plotando as distribuições normal e t
plot(x, 
     densidade_normal, 
     type = "l", 
     col = "blue", 
     lwd = 4, 
     ylab = "Densidade", 
     xlab = "Valores", 
     main = "Comparação de Distribuições")
lines(x, 
      densidade_t, 
      col = "red", 
      lwd = 4)

# Adicionando uma legenda
legend("topright", 
       legend = c("Normal", "t de Student"), 
       col = c("blue", "red"), 
       lwd = 4)