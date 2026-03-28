
#-------------------------------------------------------------------
lancamento_moeda <- rbinom(100, size = 1, prob = 0.5)
total_caras <- sum(lancamento_moeda)
cat("Nº total de caras em 100 lançamentos: ", total_caras, "\n")

#-------------------------------------------------------------------
chamadas_callcenter <- rpois(10, lambda = 5)
chamadas_callcenter

#-------------------------------------------------------------------
alturas <- c(172, 176, 180, 169, 173, 177, 174, 175, 178)
resultado_teste<- t.test(alturas, mu = 175)
resultado_teste