library(dplyr)
library(ggplot2)
library(scales)
library(ggrepel)
# Criando um conjunto de dados ####
  
notas <- c(70, 80, 80, 100, 85)

media <- mean(notas)
print(paste("Média: ",media))

mediana <- median(notas)
print(paste("Mediana: ",mediana))

moda <- names(table(notas))[which.max(table(notas))]
print(paste("Moda: ",moda))

# ADICIONANDO O 30 NO CONJUNTO DAS NOTAS ####

notas_1 <- c(70, 80, 80, 100, 85, 30)

media_1 <- mean(notas_1)
print(paste("Media 2: ",media_1))

mediana_1 <- median(notas_1)
print(paste("Mediana 2: ",mediana_1))

moda_1 <- names(table(notas_1))[which.max(table(notas_1))]
print(paste("Moda 2: ",moda_1))

# Observe que a presença de um número que podemos chamar de “outlier” (numeros com diferença descrepante) 
# fez cair a nota em quase 10 pontos, sendo assim, em alguns casos, 
# a média pode não representar corretamente o comportamento médio do conjunto.
# enquanto a mediana com os “outlier” (numeros com diferença descrepante) apresenta um calculo mais estavel e confiavel.

# Com graficos agora 1 ####

notas_alunos <- c(70, 80, 90, 100, 85, 75, 95, 88, 92, 78, 84, 91, 87, 93, 77, 89, 86, 94, 79, 96)
df_notas <- data.frame(notas = notas_alunos)

media_notas   <- mean(df_notas$notas)
mediana_notas <- median(df_notas$notas)

ggplot(df_notas, aes(x = notas)) +
  geom_histogram(bins = 10, fill = "steelblue", color = "white", alpha = 0.9) +
  geom_vline(aes(xintercept = media_notas,   color = "Média"),   linetype = "dashed", linewidth = 1) +
  geom_vline(aes(xintercept = mediana_notas, color = "Mediana"), linetype = "dotted", linewidth = 1) +
  annotate("label",
           x     = media_notas,
           y     = Inf,
           vjust = 1.5,
           hjust = 1.1,
           label = paste0("Média\n", round(media_notas, 1)),
           color = "red",
           fill  = "white",
           size  = 3.5,
           fontface = "bold") +
  annotate("label",
           x     = mediana_notas,
           y     = Inf,
           vjust = 1.5,
           hjust = -0.1,
           label = paste0("Mediana\n", round(mediana_notas, 1)),
           color = "orange3",
           fill  = "white",
           size  = 3.5,
           fontface = "bold") +
  scale_color_manual(name = "Estatísticas", values = c("Média" = "red", "Mediana" = "orange3")) +
  theme_minimal() +
  labs(title    = "Distribuição de Notas dos Alunos",
       subtitle = paste0("Média: ", round(media_notas, 1), " | Mediana: ", round(mediana_notas, 1)),
       x = "Notas Obtidas",
       y = "Frequência") +
  theme(legend.position    = "top",
        plot.title         = element_text(face = "bold", size = 14),
        plot.subtitle      = element_text(color = "gray40"))

# - Interpretação: O histograma ilustra o desempenho da turma, que é sólido e consistente.
# - Média vs Mediana: A Média e a Mediana estão praticamente sobrepostas no centro.
# - Conclusão: Isso indica uma distribuição simétrica, sem a presença de notas extremamente
#   baixas ou altas (outliers) que pudessem distorcer o resultado geral do grupo.

# Com graficos agora 2 ####

# 2. Dados
salarios <- c(
  30000, 35000, 40000, 45000, 50000, 100000,
  32000, 37000, 42000, 47000, 52000, 105000,
  31000, 36000, 41000, 46000, 51000, 110000
)

df_salarios <- data.frame(salarios = salarios)

# 3. Cálculos Básicos

# Formatação em Reais
brl <- function(x) dollar(x, prefix = "R$ ", big.mark = ".", decimal.mark = ",")

# Estatísticas principais
media_sal   <- mean(df_salarios$salarios)
mediana_sal <- median(df_salarios$salarios)
q1_sal      <- quantile(df_salarios$salarios, 0.25)
q3_sal      <- quantile(df_salarios$salarios, 0.75)
iqr_sal     <- IQR(df_salarios$salarios)

# Identificar apenas os outliers para rotular
outliers_df <- df_salarios %>%
  filter(salarios < (q1_sal - 1.5 * iqr_sal) | salarios > (q3_sal + 1.5 * iqr_sal)) %>%
  mutate(rotulo = brl(salarios))

# Subtítulo dinâmico com as informações mais importantes
texto_subtitulo <- paste0(
  "Total de funcionários (n) = ", nrow(df_salarios), 
  "   |   Mediana: ", brl(mediana_sal), 
  "   |   Média: ", brl(media_sal)
)

# 4. Gráfico Simplificado
ggplot(df_salarios, aes(x = 1, y = salarios)) +
  
  # Fundo do violino (suave)
  geom_violin(fill = "#BFE6C9", color = NA, alpha = 0.4, width = 0.5) +
  
  # Pontos dispersos (mais claros para não poluir)
  geom_jitter(width = 0.04, size = 2, alpha = 0.3, color = "black") +
  
  # Boxplot limpo e destacado
  geom_boxplot(
    width = 0.15, fill = "#7BC96F", color = "#1B5E20", 
    linewidth = 0.8, outlier.shape = NA
  ) +
  
  # Ponto da média gigante e chamativo
  stat_summary(fun = mean, geom = "point", shape = 21, size = 5, 
               fill = "red3", color = "white", stroke = 1.2) +
  
  # Rótulos para os Outliers
  geom_point(data = outliers_df, aes(x = 1, y = salarios), color = "red3", size = 3) +
  geom_text_repel(
    data          = outliers_df,
    aes(x = 1, y = salarios, label = rotulo),
    nudge_x       = 0.15,
    direction     = "y",
    hjust         = 0,
    segment.color = "red3",
    size          = 4.5,            # Fonte grande
    fontface      = "bold",
    color         = "red4"
  ) +
  
  # Textos indicativos simples ao lado da caixa
  annotate("text", x = 1.12, y = media_sal, label = "Média", color = "red3", size = 4.5, fontface = "italic", hjust = 0) +
  annotate("text", x = 1.12, y = mediana_sal, label = "Mediana", color = "#1B5E20", size = 4.5, fontface = "italic", hjust = 0) +
  
# Limpeza visual (Escalas e Tema)
scale_y_continuous(labels = label_dollar(prefix = "R$ ", big.mark = ".", decimal.mark = ",")) +
  scale_x_continuous(NULL, breaks = NULL, limits = c(0.6, 1.4)) + # Espaço ideal para os rótulos
  
  labs(
    title    = "Distribuição dos Salários da Empresa",
    subtitle = texto_subtitulo,
    y        = "Salário (R$)",
    caption  = "Pontos vermelhos indicam salários atípicos (outliers)."
  ) +
  
  theme_minimal(base_size = 14) + # Tamanho base da fonte maior para facilitar a leitura
  theme(
    plot.title       = element_text(face = "bold", size = 18),
    plot.subtitle    = element_text(color = "gray20", size = 12, margin = margin(b = 15)),
    plot.caption     = element_text(color = "gray40", size = 10, face = "italic"),
    axis.title.y     = element_text(face = "bold", margin = margin(r = 10)),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank() # Remove linha vertical no meio
  )

# - Interpretação: O boxplot demonstra a dispersão salarial da empresa, evidenciando uma
#   forte assimetria à direita.
# - Média vs Mediana: A Média foi "puxada" para cima, ficando consideravelmente maior que
#   a Mediana. Isso ocorre devido à alta sensibilidade da média aos valores atípicos.
# - Os Outliers: Os pontos isolados acima da "caixa" principal representam salários
#   discrepantes (ex: alto escalão/diretoria, acima de R$ 100 mil).
# - Conclusão Prática: Neste cenário de forte desigualdade, a Mediana é a métrica mais
#   indicada para representar o "salário típico" ou o padrão real do funcionário comum.