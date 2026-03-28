# Criando um conjuntos de dados simulado
dados <- data.frame(
	resultado_exame = c("Positivo", "Positivo", "Negativo", "Positivo", "Negativo", "Negativo", "Positivo"),  # CRIANDO UM VETOR COM RESULTADO DO EXAME POSITIVO OU NEGATIVO
	doenca = c(TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, TRUE)  # CRIANDO UM VETOR COM TRUE INDICA QUE HOUVE DOENÇA, FALSE INDICA QUE NÃO HOUVE DOENÇA
)

# Calculando a probabilidade condicional de ter a doença dado que o exame foi positivo
positivo <- subset(dados, resultado_exame == "Positivo")              # SUBSET FAZ É SUBSELEÇÃO DE DADOS DE UMA BASE DE DADOS ESPECÍFICA DE ACORDO COM UMA CONDICAO ESPECIFICADA
prob_doenca_dado_positivo <- sum(positivo$doenca) / nrow(positivo)    # AQUI O SUM, FAZ A SOMA DE TODOS OS VALORES DO VETOR POSITIVO, E DIVIDE PELA QUANTIDADE DE LINHAS DO NROW, QUE É O QUE FAZ A CONTAGEM DE LINHAS DO VETOR POSITIVO
print(prob_doenca_dado_positivo)                                      # PRINT INDICA QUE O RESULTADO SERÁ IMPRESSO NO CONSOLE