set.seed(123)                                # gerando
populacao <- rnorm(1000000,                  # definindo a populacao = 1000000 com a media de 5000 e desvio padrao de 1500
                   mean = 5000, 
                   sd = 1500)

amostra <- sample(populacao,                 # definindo minha amostra de 1000 dos 1000000 da populacao sem repetições 
                  size = 1000, 
                  replace = FALSE)

media_amostra <- mean(amostra)               # media da amostra
desvio_padrao_amostra <- sd(amostra)         # desvio padrao da amostra

cat("Média da amostra", media_amostra,"\n")
cat("Desvio da amostra", desvio_padrao_amostra,"\n")

# A ideia aqui é que quanto mais grande minha amostra for mais proxima da realidade ela vai esta da "população"(Nesse caso)

# simulando diferentes tamanhos
amostra_pequena <- sample(populacao, size = 50, replace = FALSE)
amostra_media <- sample(populacao, size = 100, replace = FALSE)
amostra_grande <- sample(populacao, size = 1000, replace = FALSE)
mean(amostra_pequena)
mean(amostra_media)
mean(amostra_grande)

# aqui vemos que a nossa ideia realmente prevalece.
# no caso, quanto mais minha média for mais próxima da minha população ela tendec a ficar mais proxima da média real da população.

# Estudo de caso ####
populacao_eleitores <- rbinom(10000000,
                              1,                                   # definindo a populacao eleitoral = 1000000 com a probabiliddade de de votar é de 0.55
                   prob = 0.55)

amostra_eleitores <- sample(populacao_eleitores,                   # definindo minha amostra de 1000 dos 1000000 da populacao eleitorais sem repetições 
                  size = 5000, 
                  replace = FALSE)

proporcao_eleitoral <- mean(amostra_eleitores)

cat("Proporção estimada de votos para o candidato A ", proporcao_eleitoral ,"\n")

# a ideia aqui é, quanto maior ou mais representativa for a minha amostra, mais a proporção amostral se aproxima da probabilidade real.


#calcular a média
media_boot <- function(data, indices) {
  return(mean(data[indices]))
}

library(boot)
# aplicando bootstrap na amostra
resultado_boot <- boot(data = amostra_eleitores, statistic = media_boot, R = 1000)

erro_padrao <- sd(resultado_boot$t)

cat("Erro padrão estimado",erro_padrao,"\n")

# fazendo esse tipo de amostragem meu erro de estimativa esta menos que 1% esta ótimo
# Finalizando, conforme nos vamos aumentando nosso nivel de amostragem, vamos ficando mais próximo da média real da populacao.