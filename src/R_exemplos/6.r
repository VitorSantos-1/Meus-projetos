# Imagine que você é um consultor de uma empresa de marketing digital e está avaliando a eficácia de duas campanhas publicitárias, A e B. 
# Durante um mês, a Campanha A foi exibida para 1.000 pessoas e resultou em 200 conversões, 
# enquanto a Campanha B foi exibida para 1.000 pessoas e resultou em 250 conversões. 
# A empresa deseja saber se a diferença nas taxas de conversão entre as duas campanhas é estatisticamente significativa.

conv_a <- 200
pessoa_a <- 1000
conv_b <- 250
pessoa_b <- 1000

prob_1 <- conv_a / pessoa_a
prob_b <- conv_b / pessoa_b

prop.test(c(conv_a,conv_b), c(pessoa_a, pessoa_b))