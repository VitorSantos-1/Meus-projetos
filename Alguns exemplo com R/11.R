# Amostragem ####

z <- 1.96      # é o padrão mais ultilizado de confiança( 95% )
p <- 0.5       # representa a propoçao esperada, 0,5 é o padrão quando nao se temos uma proporção especifica
e <- 0.05      # representa a taxa de erro

# formula do calculo
n <- (z^2 * p * (1-p)) / e^2

# o calculo
populacao <- 1000
n_calculado <- (n * populacao)/(n + (populacao - 1))

# visualizando o calculo
print(n_calculado)

# Definindo a populaçao
população <- 1:1000

# Realizando uma amostragem aleatória simples
set.seed(123) # para a reprodutibilidade
amostra <- sample(população,
                  size = ceiling(n_calculado), # Arredonda 369.98 para 370 automaticamente
                  replace = FALSE
)
# Visualizando a amostra
print(amostra)

# Por exemplo, Se for comunicar isso para uma equipe, a fala ideal seria:
# Baseado na nossa base para este produto que é de 10.000 usuários. 
# Para termos 95% de segurança nas decisões com a margem de erro de apenas 5%, 
# não precisamos testar o produto com todos eles, o que seria caro e demorado.
# O cálculo estatístico nos garante que só precisamos coletar o feedback de 370 usuários selecionados aleatoriamente. 
# A resposta desse pequeno grupo vai refletir com precisão o que a base inteira pensa.

# -------------------------------------------------------------------------------------------------------------------

# TLC - Teorema do Limite Central ####

# O objetivo aqui é provar na prática que a média de várias amostras 
# sempre forma uma curva de sino (Normal), não importa a origem dos dados.
set.seed(123)                                  # Fixa o "sorteio" para que o resultado seja o mesmo toda vez que rodar

# Criando uma "máquina" (função) que coleta amostras e calcula a média delas
amostra_media <- function(n,                   # Quantas vezes vamos repetir o processo todo
                          tamanho_amostra)     # Quantos itens cada amostra terá
{                                              # Iniciando a lista
  medias <- replicate(n,                       # 4. Repete o processo abaixo 'n' vezes e guarda os resultados
                      mean(                    # 3. Calcula a média matemática dessa amostra sorteada
                        runif(                 # 2. Sorteia números aleatórios (distribuição uniforme)...
                          tamanho_amostra,     # ...nesta quantidade (ex: 30 números)...
                          min = 0,             # ...começando de zero...
                          max = 100            # ...até 100.
                        )
                      )
  )
  return(medias)                               # Devolve a lista com todas as médias que foram calculadas
}                                              # Terminando a lista

# Executando a função: sorteamos 30 números, calculamos a média, e repetimos isso 1.000 vezes
medias_amostrais <- amostra_media(1000, 30)

# 2. DESENHANDO O GRÁFICO (E guardando ele na letra 'h')
h <- hist(
  medias_amostrais,
  breaks = 30,
  ylim = c(0, 85),                             # Aumentamos o teto do gráfico para 85 para o texto não ficar cortado
  main = "Distribuição das Médias Amostrais",
  xlab = "Valores das Médias",
  ylab = "Frequência (Quantidade exata de amostras)",
  col = "darkcyan",
  border = "white"
)

# 3. COLOCANDO OS NÚMEROS E A % EM CIMA DAS BARRAS
# O R vai pegar a altura da barra (h$counts) e escrever ex: "62 \n (6.2%)"
text(
  x = h$mids,                                  # Fica exatamente no meio da barra
  y = h$counts,                                # Fica exatamente no topo da barra
  
  # A mágica do texto: Pega a quantidade, pula uma linha (\n) e calcula a %
  labels = ifelse(h$counts > 0, 
                  paste0(h$counts, "\n", (h$counts / 1000) * 100, "%"), 
                  ""),
  pos = 3,                                     # Avisa o R para colocar o texto do lado de FORA/ACIMA da barra
  cex = 0.5,                                   # Tamanho da fonte (0.7 é ideal para os números não se atropelarem)
  col = "black"
)

# "Pessoal, o que esse gráfico prova para nós?
# 1. A montanha no meio: Cada barrinha verde é o resultado de uma amostra 
# de apenas 30 itens. Reparem que as barras mais altas se acumulam bem no meio.
# 
# 2. O pico no 50: O número 50 é a média real de toda a nossa base de dados. 
# O gráfico mostra que, mesmo usando só 30 itens por vez, nós acertamos na mosca 
# ou chegamos muito perto da verdade na esmagadora maioria das vezes.
#
# Conclusão: Não precisamos gastar tempo e dinheiro analisando 100% de tudo. 
# A matemática prova que pegar amostras pequenas (30 itens) já é mais do que 
# suficiente para termos um retrato fiel e confiável da realidade."