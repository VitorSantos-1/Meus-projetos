# Carregando os dados
data(mtcars)

# Como as caracteristicas do carro, [nº do cilindros, peso ou tipo de transmição], influenciam na eficiência de combustivel? ####

# Variaveis:

# mpg	Miles/(US) gallon
# cyl	Number of cylinders
# disp	Displacement (cu.in.)
# hp	Gross horsepower
# drat	Rear axle ratio
# wt	Weight (1000 lbs)
# qsec	1/4 mile time
# vs	Engine (0 = V-shaped, 1 = straight)
# am	Transmission (0 = automatic, 1 = manual)
# gear	Number of forward gears
# carb	Number of carburetors


# Anallisando a variavel 'mpg' [milhas por galão]
summary(mtcars$mpg)

media_mpg <- mean(mtcars$mpg) # média de milhas por galão
mediana_mpg <- median(mtcars$mpg) # mediana das milhas por galão
desvio_padrao_mpg <- sd(mtcars$mpg) # desvio padrão das milhas por galão
variancia_mpg <- var(mtcars$mpg) # variancia das milhas por galão

# resultado
cat("Média: ", media_mpg,"\nMediana: ", mediana_mpg,"\nDesvio Padrão: ", desvio_padrao_mpg,"\nVariância: ", variancia_mpg)

# criando um histograma
hist(mtcars$mpg,
     main = "Distribução de Milhas por galão",
     xlab = "Milhas por galão",
     col = "skyblue",
     border = "black"
     )
#NOTA: Vimos no grafico que a maior concentração de carros esta entre 15 a 20 milhas por galões

# adicionando a média e a mediana para analise
abline(v = mean(mtcars$mpg), col = "orange", lwd = 2, lty = 2)
text(mean(mtcars$mpg), 2, "Média", col = "black", pos = 4)
abline(v = median(mtcars$mpg), col = "red", lwd = 4, lty = 4)
text(median(mtcars$mpg), 4, "Mediana", col = "black", pos = 2)

#NOTA: Vimos no grafico que a media dos dados esta em ~20, e a mediana esta em ~19

# criar um boxplt para o mpg
boxplot(mtcars$mpg,
        main = "Boxplot de Milhas por galão",
        ylab = "Milhas por galão",
        col = "lightgreen"
        )
# Quartis
# NOTA: Vimos no grafico que o Q1 é entre 10 e 16, Q2 é entre 16 e 19, Q3 é entre 19 e 23 e o Q4 é estre 23 ate 33.

# Verificando os outliers
outliers <- boxplot(mtcars$mpg) $out
cat("Outliers identificados: ",outliers)

# O tipo de transmissão afeta o consumo de combustivel controlando o peso do carro? ####

# Ajustar a ANCOVA
model_ancova <- aov(mpg ~ am + wt, data = mtcars)
# Calculndo a diferença de consumo de combustível[mpg] entre carros manuais e automáticos[am], 
# mas finja que todos os carros pesam exatamente a mesma coisa[wt].]

# Resumo do modelo
summary(model_ancova)
# Se for < 0.05, a diferença é estatisticamente significativa, para afirmar se a transmissão altera o consumo.
# Se for > 0.05, a diferença não é estatisticamente significativa, para afirmar se a transmissão altera o consumo.

# Verificando os coeficientes
coef(model_ancova)
# Intercept: É a base do cálculo. Seria o consumo de um carro automático(pois automático é a categoria base "0")
# Se o número de 'am' for positivo, significa que o carro manual é mais econômico x milhas de galões a mais.
# Se o número de 'am' for negativo, significa que o carro manual é menos econômico x milhas de galões a menos.

# NOTA: Vimos que nos calculos, indica que o carro automatico vai aumentar o consumo, e quanto maior o peso maior o consumo.

# Gráfico 
library(ggplot2)
ggplot(mtcars, aes(x = wt, y = mpg, color = factor(am))) +
  geom_point(size = 3) +
  geom_smooth(method = "lm", aes(group = factor(am)), se = FALSE) +
  labs(title = "ANOVA: Relação entre MPG e Peso ajustado por Tipo de Transmissão",
       x = "Peso do Carro (wt)",
       y = "Milhas por Galão (mpg)",
       color = "Tipo de Transmissão\n(0 = Automática, 1 = Manual)") +
  theme_minimal()

##BRINCANDO COM O R  ####
model_simple <- lm(mpg ~ wt, data = mtcars)
summary(model_simple)

model_multiple <- lm(mpg ~ wt + hp + as.factor(am), data = mtcars)
summary(model_multiple)

## CLUSTER ####
dist_mtcars <- dist(mtcars[, c("mpg", "hp", "wt")])
hc <- hclust(dist_mtcars)
plot(hc, main = "Cluster Hierárquico de Carros")
# Calculando a "distância" entre os carros com base em consumo (mpg), potência (hp) e peso (wt), 
# gerando um dendrograma (um gráfico de árvore) para visualizar as semelhanças.

set.seed(42)
kmeans_model <- kmeans(mtcars[, c("mpg", "hp", "wt")], centers = 3)
mtcars$cluster <- kmeans_model$cluster
# Divide os carros em 3 grupos distintos (clusters). 
# O comando set.seed(42) é usado para que o resultado seja sempre o mesmo toda vez que você rodar o código.


# TESTE DE HIPOTESE ####
t.test(mpg ~ factor(am), data = mtcars)
# Verificando se a diferença de consumo (mpg) entre carros automáticos e manuais 
# é estatisticamente significante ou se ocorreu por puro acaso.

# criando um gráfico de dispersão com uma linha de tendência (método lm) 
# mostrando como o consumo cai conforme o peso aumenta.
library(ggplot2)
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  labs(title = "Relação entre Peso e Consumo de Combustível", x = "Peso", y = "Milhas")

# gera múltiplos gráficos de uma vez, permitindo ver a correlação cruzada entre consumo, peso, potência e deslocamento (disp).
pairs(mtcars[, c("mpg", "wt", "hp", "disp")])