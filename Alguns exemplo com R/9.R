library(ggplot2)

# Dados simulados ####

horas <- c(1, 2, 3, 4, 5, 6, 7)
notas <- c(50, 55, 60, 65, 70, 75, 80)

# gráfico de dispersão
plot(horas, notas, main="Horas estudadas vs Notas finais", xlab="Horas estudadas", ylab="Notas", pch=19, col="blue")

# Adicionando linha de tendência
abline(lm(notas ~ horas), col="red")

# Esse gráfico nos mostra se existe uma correlação positiva entre as horas estudadas e as notas. 
# Uma tendência ascendente indica que, à medida que os alunos estudam mais, suas notas aumentam.
# A linha de tendência (em vermelho) reforça essa correlação positiva.

# Gerando dados de exemplo para dois grupos de profissionais de TI ####
set.seed(123)  # Para reprodutibilidade

grupo_A <- rnorm(100, mean = 7000, sd = 1500)  # Grupo A com média salarial de 7000 e desvio padrão de 1500
grupo_B <- rnorm(100, mean = 8000, sd = 2000)  # Grupo B com média salarial de 8000 e desvio padrão de 2000

# Criando um dataframe para os dados
dados <- data.frame(
  salario = c(grupo_A, grupo_B),
  grupo = factor(rep(c("Grupo A", "Grupo B"), each =100))
)

# Gerando o boxplot

ggplot(dados, aes(x= grupo, y= salario, fill= grupo)) +
  geom_boxplot() +
  labs(title = "Boxplot de Salários de Dois Grupos de Profissionais de TI",
       x= "Grupo",
       y= "Salario") +
  theme_minimal()

# Gerando dados de exemplo para duas populações ####
set.seed(123)  # Para reprodutibilidade

# Dados de IMC para jovens adultos (18-25 anos)
jovens_adultos <- rnorm(100, mean = 24, sd = 3)  # Média IMC de 24 com desvio padrão de 3

# Dados de IMC para adultos de meia-idade (45-60 anos)
meia_idade <- rnorm(100, mean = 27, sd = 4)  # Média IMC de 27 com desvio padrão de 4

# Criando um dataframe para os dados
dados <- data.frame(
imc = c(jovens_adultos, meia_idade),
grupo = factor(rep(c("Jovens Adultos", "Meia Idade"), each = 100)) 
  )

# Gerando o boxplot
ggplot(dados, aes(x = grupo, y = imc, fill = grupo)) +
geom_boxplot() +
labs(title = "Boxplot do IMC de Jovens Adultos e Adultos de Meia-Idade",
     x = "Grupo Etário", 
     y = "Índice de Massa Corporal (IMC)") +
  theme_minimal()

# A média do IMC dos adultos de meia-idade é maior (em torno de 27) comparada à dos jovens adultos (em torno de 24).
# A dispersão do IMC é maior entre os adultos de meia-idade, indicada pela maior distância entre o primeiro e o terceiro quartil.
# Os jovens adultos têm uma dispersão de IMC menor e mais concentrada.
# Ambos os grupos podem ter presença de outliers, indicando valores de IMC extremamente altos ou baixos em comparação com a maioria dos dados.