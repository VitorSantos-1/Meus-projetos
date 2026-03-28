# CARREGANDO E VISUALIZANDO OS DADOS ####
# I. Carregando os dados
url <- "https://raw.githubusercontent.com/AndersonSalata/projeto-integrado-ciencia-de-dados/main/datatran2024.csv"

# II. Bases de acidentes
dados <- read.csv2(url,
                   fileEncoding = "latin1")

# III. Análise exploratória básica
summary(dados)                                     # Estatistica basica, analisando.
# Contando "table" quantas vezes cada clima(condicao_metereologica) apareceu dentro($) da variavel(dados)
table(dados$condicao_metereologica)

# TESTES ESTATÍSTICOS ####

# I. Teste Qui-Quadrado
# Criando uma variavel com os dados (clima) em linhas e (tipo de acidente) em colunas fazendo a contagem cruzada entre elas[ex: quantos colisões teve com chuva].
tabela_comparativa <- table(dados$condicao_metereologica,
                    dados$tipo_acidente)
print(tabela_comparativa)

# II. Peguei a tabela(tabela_c) que acabamos de criar e apliquei a fórmula estatística "Qui-Quadrado".
# Aqui calculamos matematicamente se a diferença de acidentes entre um clima e outro é pura obra do acaso ou se existe um padrão real.
teste_qq <- chisq.test(tabela_comparativa)
print(teste_qq)

# III. Intervalo de Confiança para a média de veiculos
# Peguei a coluna que diz quantos veiculos se envolveram em acidentes(dados$veiculos) e calculei a média e apliquei a margem de erro(conf.level = 95% = 0,95) com t.test.
teste_ic <- t.test(dados$veiculos,
                   conf.level = 0.95)
print(teste_ic$conf.int)

# IVS. Correlação entre 'veiculos' e 'feridos'
# > Usei o 'complete.obs' para ignorar linhas vazias (NA)
# Comparando as colunas veiculos e feridos, linha por linha, para ver se elas crescem ou diminuem juntas. O (use = "complete.obs") diz para o programa ignorar linhas que estejam em branco ou com erro.
correlacao <- cor(dados$veiculos,
                  dados$feridos,
                  use = "complete.obs")
print(correlacao)


# GERANDO OS GRÁFICOS PARA O RELATÓRIO ####
# Para os gráficos ficarem com as margens ajustadas (para os nomes não cortarem)
par(mar=c(10, 4, 4, 2)) 

# 1. Gráfico de Condições Meteorológicas
tabela_clima <- table(dados$condicao_metereologica)
# Ordenando do maior para o menor para ficar mais profissional
tabela_clima_ordenada <- sort(tabela_clima, decreasing = TRUE)

barplot(tabela_clima_ordenada, 
        main = "Distribuição de Acidentes por Condição Meteorológica", 
        col = "steelblue", 
        las = 3,                                # Vira o texto na vertical para caber
        cex.names = 0.7,                        # Diminui um pouco o tamanho da fonte
        ylab = "Número de Acidentes")


# 2. Gráfico de Tipos de Acidente
tabela_tipo <- table(dados$tipo_acidente)
# Pegando apenas os 10 mais frequentes para o gráfico não ficar uma bagunça
tabela_tipo_top10 <- head(sort(tabela_tipo, decreasing = TRUE), 10)

barplot(tabela_tipo_top10, 
        main = "Top 10 - Tipos de Acidentes Mais Frequentes", 
        col = "darkorange", 
        las = 3, 
        cex.names = 0.7,
        ylab = "Número de Acidentes")