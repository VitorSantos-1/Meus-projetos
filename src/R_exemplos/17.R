# Significância estatística #### 

# Abordagem de R. A. Fisher (Significância)
set.seed(123)                                                    
grupo_tratamento <- rnorm(100, mean = 5.5, sd = 1)               
grupo_controle <- rnorm(100, mean = 5, sd = 1)                   

t.test(grupo_tratamento, grupo_controle)                     

# 1. O foco de Fisher não é usar uma linha de corte rígida, mas sim medir 
# o quão forte é a evidência dos seus dados contra a Hipótese Nula (H0).
#
# 2. O p-valor obtido foi extremamente baixo 3.941e-07.
#
# Nesse caso, o p-valor funciona como um "termômetro". Como ele 
# é minúsculo(...e-...), os dados estão gritando que é altamente improvável que 
# os grupos sejam iguais. A evidência de que o tratamento funciona é fortíssima!

# OBS: Se fosse o pvalor fosse (...e+...) o resulta seria ao contrario.


# Abordagem de Neyman-Pearson (Regra de Decisão)
set.seed(123)                                                    
tratamento_a <- rnorm(100, mean = 60, sd = 10)                   
tratamento_b <- rnorm(100, mean = 65, sd = 10)                   

t.test(tratamento_a, tratamento_b)                           

# 1. O foco aqui é criar uma regra estrita de decisão ANTES do teste para 
# controlar a chance de tomarmos uma decisão errada.
# 2. Erro Tipo I (Alfa): Definimos que aceitamos errar em no máximo 5% das vezes 
# (Alfa = 0.05). Esse é o nosso limite para "falso positivo".
# 3. Regra de Decisão: O nosso p-valor (0.0242) ficou menor que o limite do Alfa (0.05).
# 
# Nesse caso, como o valor cruzou a nossa linha de corte, nós 
# REJEITAMOS a Hipótese Nula. Podemos afirmar que o tratamento B é melhor que o A, 
# mantendo a nossa taxa de erro rigorosamente controlada em 5%.

# Método Fisher (Teste Exato para Categorias) ####
set.seed(123)                                                    
grupo_tratamento <- rnorm(100, mean = 5.5, sd = 1)               # Seus dados originais
grupo_controle <- rnorm(100, mean = 5, sd = 1)                   # Seus dados originais

# Transformar os seus números em categorias
# Vamos considerar que qualquer resultado acima de 5.5 significa que a pessoa "Curou"
curados_tratamento <- sum(grupo_tratamento > 5.5)
nao_curados_tratamento <- sum(grupo_tratamento <= 5.5)
curados_controle <- sum(grupo_controle > 5.5)
nao_curados_controle <- sum(grupo_controle <= 5.5)

# Montar a tabelinha que o Fisher exige (Contagem de pessoas)
tabela_medicacao <- matrix(c(curados_tratamento, nao_curados_tratamento,
                             curados_controle, nao_curados_controle),
                           nrow = 2, byrow = TRUE)

# Rodar o teste de Fisher!
fisher.test(tabela_medicacao)

# Nesse caso, em vez de olhar para a "média", o Fisher vai olhar para a "quantidade de pessoas".
# Ele vai te dizer baseado no odds ratio(>1 = o 1º grupo vence | <1 = o 2º grupo vence ) 
# que a quantidade de pessoas curadas no grupo de tratamento foi 
# significativamente maior que no grupo controle. Se o p-valor der baixo (< 0.05), 
# a medicação realmente aprovou mais gente!


# Método Pearson (Correlação) ####
set.seed(123)                                                    
tratamento_a <- rnorm(100, mean = 60, sd = 10)                   # Dados que você gerou
tratamento_b <- rnorm(100, mean = 65, sd = 10)                   # Dados que você gerou

# Aplicando o teste de correlação de Pearson de verdade:
cor.test(tratamento_a, tratamento_b, method = "pearson")


# 1. P-valor: Deu um valor alto (maior que 0.05). Isso significa que 
# não temos evidências estatísticas para dizer que existe uma relação aqui.
# 2. Correlação (cor): Deu um número muito próximo de ZERO. 
# 
# Nesse caso, o teste está nos dizendo: "Não há relação NENHUMA 
# entre o tratamento A e o B". Se o valor de A sobe ou desce, o valor de B 
# não é afetado. Eles são totalmente independentes