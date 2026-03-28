library(dplyr)
library(ggplot2)

# Criando um conjunto de dados simulado
dados <- data.frame(
  produto = c("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"), # CRIANDO UM VETOR COM NOME DO PRODUTO
  quantidade = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), # CRIANDO UM VETOR COM A QUANTIDADE DO PRODUTO
  vendas = c(100, 200, 300, 400, 500, 600, 700, 800, 900, 1000), # CRIANDO UM VETOR COM VENDAS DO PRODUTO
  data = as.Date(c("2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", "2022-01-07", "2022-01-08", "2022-01-09", "2022-01-10")) # CRIANDO UM VETOR COM DATA DO PRODUTO
)
# imprimindo os dados
print(dados)

# Selecionando apenas as colunas produto e vendas
dados_vendas <- dados %>%
  select(produto, vendas)

# Filtrando vendas com valor superior a 150
dados_vendas <- dados %>%
  filter(vendas > 150)

# Criando uma nova coluna de preço médio por item
dados_vendas %>%
  mutate(preco_medio = vendas / quantidade)

# Ordenando vendas por receita (decrescente)
dados_vendas %>%
  arrange(desc(vendas))

# Calculando a receita total
dados_vendas %>%
  summarise(vendas = sum(vendas))

# Criando um grafico de linha de vendas por data
ggplot(dados_vendas, aes(x = produto, y = quantidade)) +
  geom_bar(stat = "identity") +
  labs(title = "Receita por produto", x = "Produto", y = "Quantidade")

modelo <- lm(vendas ~ quantidade, data = dados_vendas)
summary(modelo)