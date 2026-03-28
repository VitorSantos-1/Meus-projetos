# Intervalos de Confiança ####
# Empresa quer saber se a média de satisfação dos clientes com o novo produto é significativamente diferente de 7 em uma escala de 1 a 10.

# Passo 1: Coletar Dados
set.seed(123)                                                                 # Definindo uma "semente" para o gerador de números aleatórios.
satisfacao <- rnorm(100, mean = 7.2, sd = 1.5)                                # Gera números aleatórios seguindo uma distribuição normal. 
                                                                              # Aqui, está gerando 100 valores (n), com média(mean) e desvio padrão(sd).
# Passo 2: Calcular a Média e o Desvio Padrão da Amostra
media_amostra <- mean(satisfacao)                                             # Calculando a média aritmética da 'satisfacao'.
desvio_padrao <- sd(satisfacao)                                               # Calculando o desvio padrão da 'atisfacao'.

# Passo 3: Calcular o Intervalo de Confiança de 95%
erro_padrao <- desvio_padrao / sqrt(length(satisfacao))                       # Calculando a raiz quadrada(sqrt) do length() tamanho da amostra(n = 100).
nivel_confianca <- 0.95                                                       # Definindo o nivel de confiança 95% = 0.95
probabilidade <- nivel_confianca + (1 - nivel_confianca) / 2                  # Calculando a probabilidade
t_critico <- qt(probabilidade, length(satisfacao) - 1)                        # qt(é a probabilidade) df = length() Pegando o tamanho da minha amostra - 1
limite_inferior <- media_amostra - t_critico * erro_padrao                    # Esse é o calculo do limite inferior
limite_superior <- media_amostra + t_critico * erro_padrao                    # Esse é o calculo do limite superior

# Vendo como ficou
cat("IC 95%: [", limite_inferior, ", ", limite_superior, "]\n")

# IC = Intervalo de Confiança é de 95% para a média de satisfação, por
# exemplo, [7,06, 7.60]. Isso significa que, com 95% de confiança, a média verdadeira de
# satisfação está dentro desse intervalo.

# Análise de erros ####

# Passo 4: Realizar um Teste t
teste_t <- t.test(satisfacao, mu = 7)                                         # Realizando um Teste t de Student para uma amostra
print(teste_t)                                                                # Ele verifica se a média observada na amostra ('satisfacao') é estatisticamente diferente de um valor hipotético ('mu'= 7).

# t.test = Teste t: O p-valor do teste t é, 0.016. Como o p-valor é < 0.05, rejeitamos a
# hipótese nula de que a média de satisfação é igual a 7. Portanto, podemos concluir que a
# média de satisfação dos clientes é significativamente diferente de 7 que é o que a hipotese alternativa nos diz.


# Reamostragem ####

# Passo 5: Aplicar o Método Bootstrap
library(boot)
# Função para calcular a média
media_boot <- function(data, indices) {                                       # Cria uma função personalizada definida pelo usuário.
  return(mean                                                                 # Aqui, está sendo criada uma função específica para ser lida pelo pacote 'boot'.
         (data[indices]))
}

# Aplicar o bootstrap com 1000 reamostragens
resultado_boot <- boot(data = satisfacao, statistic = media_boot, R = 1000)   # Aplica o método de bootstrap. 
                                                                              # Ele cria um número 'R' (1000) de novas amostras retiradas com reposição a partir dos dados originais e aplica a função 'statistic' (sua função 'media_boot') em cada uma delas.
# Calcular o intervalo de confiança
ic_boot <- boot.ci(resultado_boot, type = "perc")                             # Calcula o Intervalo de Confiança do bootstrap com base nos resultados gerados pela função boot().   
print(ic_boot)                                                                # O parâmetro type="perc" indica que está usando o método dos percentis.

# Passo 6: Aplicar o Método Jackknife
# Calcular a média excluindo uma observação
media_jackknife <- function(data) {
  n <- length(data)
  jackknife_means <- sapply(1:n, function(i) mean(data[-i]))
  return(jackknife_means)
}

media_jackknife(satisfacao)

# Graficos ####
# Gerar amostra da satisfação normal
dados_normais <- rnorm(100, mean = 7.2, sd = 1.5)
hist(dados_normais, breaks = 30, main = "Historiograma de distribuição normal", xlab = "valores", col = "blue")

# Gerar amostra da satisfação binomial
dados_binomiais <- rbinom(100, size = 10, prob = 0.5)
hist(dados_binomiais, breaks = 30, main = "Historiograma de distribuição binomial", xlab = "valores", col = "red")

# Eles lado a lado
par(mfrow = c(1,2))
hist(dados_normais, breaks = 30, main = "Historiograma de distribuição normal", col = "blue")
hist(dados_binomiais, breaks = 30, main = "Historiograma de distribuição binomial", col = "blue")