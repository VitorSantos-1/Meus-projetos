# Testes estatísticos ####
set.seed(123)                                                    # gerando
grupo_tratamento <- rnorm(100, mean = 5.5, sd = 1)               # criando o grupo com a média 5.5 e desvio padrao de 1
grupo_controle <- rnorm(100, mean = 5, sd = 1)                   # criando o grupo com a média 5 e desvio padrao de 1

t.test(grupo_tratamento, grupo_controle)                         # comparando a média dos 2

# O p-valor de 3.941e-07 não é a probabilidade da média ser 5.5.
# Pense nele como um "teste de acaso": ele nos diz que, se os dois
# grupos fossem realmente iguais na prática, a chance de acharmos
# essa diferença entre eles por pura sorte seria quase zero.
# Como essa chance é minúscula, concluímos que não foi sorte:
# a diferença entre as médias é real estatisticamente significativa.
# Então nesse caso, estatisticamente falando, o medicamento esta fazendo efeito.

# Teste A/B e HIPÓTESES ####
set.seed(123)
grupo_a <- rbinom(1000, 1, prob = 0.15)                          # 15% de conversão
grupo_b <- rbinom(1000, 1, prob = 0.18)                          # 18% de conversão
prop.test(c(sum(grupo_a), sum(grupo_b)),
          c(length(grupo_a), length(grupo_b)))                   # realizando teste A/B


# 1. P-valor (0.1427): É maior que a nossa margem de erro aceitável (0.05). 
# Isso significa que a diferença que vimos entre os grupos tem uma boa chance 
# de ter acontecido apenas por acaso (sorte).
#
# 2. Intervalo de Confiança: Vai de um número negativo até um positivo, o que 
# significa que o "Zero" (que representa "diferença nenhuma") está no meio do 
# caminho. Como o zero é uma possibilidade real, não podemos bater o martelo.
#
# 3. Conclusão: O grupo B até converteu um pouco mais(17.2% contra 14.7%),
# mas, como vimos acima, os testes mostram que isso não passou de um possível 
# acaso.
# Na prática, consideramos que os dois grupos estão empatados.

# Tratamento ####

tratamento_a <- rnorm(100, mean = 60, sd = 10)                   # criando o grupo de tratamento com a média 60 e o desvio padrao de 10
tratamento_b <- rnorm(100, mean = 65, sd = 10)                   # criando o grupo de tratamento com a média 65 e o desvio padrao de 10

t.test(tratamento_a, tratamento_b)                               # comparando as média

# H0: O novo medicamento não tem efeito estatisticamento significativo, comparado ao placebo
# H1: O novo medicamento tem um efeito estatisticamento significativo, comparado ao placebo
# Nesse caso, iremos rejeitar a hipotese 0, pq no resultado final a Hipotese 1 mostra que o teste tem efeito comparado ao placebo.