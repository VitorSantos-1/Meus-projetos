###################################################################################################################################

# importando as bibliotecas
library(dplyr)
library(ggplot2)
library(scales)
library(ggtext)
library(showtext)
###################################################################################################################################

# importando os dados de um aquivo csv, e organizando.
dados <- read.csv("D:/Meus/Codigos/Alguns exemplo com R/datatran2024.csv",
                  sep = ";",                            # sep = separador, diz pro R que as colunas são divididas por ponto e vírgula.
                  dec = ",",                            # dec = decimais, diz pro R que números decimais usam vírgula e não ponto.
                  fileEncoding = "UTF-8",               # fileEncoding, Corrige os acentos bugados, os caracteres estranhos como SÃ£o Paulo.
                  fill = TRUE,                          # fill ele garante que linhas incompletas não travem
                  check.names = FALSE)                  # check.names mantém os nomes originais das colunas
# Visualizando
head(dados)
glimpse(dados)
summary(dados)

###################################################################################################################################

# 1° Pergunta do trabalho: " Qual foi o estado com o maior número de acidentes? "
estado <- dados %>%                                     # Pegue a tabela original 'dados'
  count(uf) %>%                                         # Conte quantas vezes cada 'uf' aparece, isso cria uma coluna nova chamada 'n' com a contagem
  arrange(desc(n))                                      # Organize a tabela baseada na coluna 'n', o 'desc' significa 'Decrescente'
head(estado, 10)                                        # Mostre o meu Top 10

###################################################################################################################################

# 2° Pergunta do trabalho: " Qual a probabilidade de um acidente ocorrer em condições climáticas claras? "
prob_climatica <- dados %>%
  summarise(                                            # serve para resumir a tabela inteira em um único número ou linha de resultados.
    total_acidente = n(),               # (n) = conte quantas linhas existem, e salve o resultado dessa contagem em uma nova coluna chamada total_acidente
    acend_claros = sum(condicao_metereologica == "Céu Claro",
                        na.rm = TRUE),                             # Se na coluna tiver a linha com Céu claro ele conta 1, se houver linha em branco nao conta
    probabilidade_real = (acend_claros / total_acidente) * 100)
print(prob_climatica)

###################################################################################################################################

# 3° Pergunta do trabalho:" Como a fase do dia afeta a ocorrência de acidentes? "
ac_fase_dia <- dados %>%                                                        # criando a tabela de contagem
  group_by(fase_dia) %>%                                                        # agrupa os dados por fase (Dia, Noite, etc)
  summarise(total_fase_dia = n()) %>%                                           # conta quantos acidentes tem em cada fase
  mutate(porcentagem = round(
    (total_fase_dia / sum(total_fase_dia)) * 100, 2)) %>%                       # criando uma coluna porcentagem
                                                                                # usando o calculo total / soma do total* 100
  arrange(desc(total_fase_dia))                                                 # ordenando do maior para o menor
print(ac_fase_dia)

# grafico
font_add_google("Montserrat", "montserrat")
showtext_auto()
# I. Engenharia de Dados Visuais
dados_grafico <- ac_fase_dia %>%
  arrange(total_fase_dia) %>% 
  mutate(
    fase_dia = factor(fase_dia, levels = fase_dia),
    
    # Mantive apenas o texto limpo para evitar os "quadradinhos" no seu eixo Y
    fase_com_icone = factor(fase_dia, levels = fase_dia),
    
    # CORREÇÃO AQUI: Trocando os '**' do Markdown pelas tags '<b>' e '</b>' do HTML
    label_html = paste0(
      "<span style='color:#FFFFFF; font-size:15pt;'><b>", 
      format(total_fase_dia, big.mark = ".", decimal.mark = ","), 
      "</b>  </span>  <span style='color:#00E5FF; font-size:10pt;'> ", 
      round(porcentagem, 0), "% </span>"
    )
  )
# Define o limite máximo da tela para a "trilha" de fundo das barras
max_val <- max(dados_grafico$total_fase_dia) * 1.25

# II. Construção do Gráfico Dark Dashboard
ggplot(dados_grafico, aes(y = fase_com_icone, x = total_fase_dia)) +
  
  # A: "Trilha" de fundo escura (Efeito de barra de progresso)
  geom_col(aes(x = max_val), fill = "#1E293B", width = 0.35) +
  
  # B: A Barra de Dados principal (Neon Moderno)
  geom_col(fill = "#00E5FF", width = 0.35, alpha = 0.95) +
  
  # C: Rótulos voando à direita da barra (nunca mais serão cortados)
  geom_richtext(
    aes(label = label_html),
    hjust = -0.05,        # Descola o texto levemente do fim da barra
    fill = NA,            # Fundo transparente
    label.color = NA,     # Sem bordas
    family = "montserrat"
  ) +
  
  # D: Títulos com peso de fonte contrastante
  labs(
    title = "**ACIDENTES POR FASE DO DIA**",
    subtitle = "Análise de criticidade baseada nas ocorrências de 2024",
    caption = "**Base:** DataTran 2024"
  ) +
  
  # E: O Tema UI/UX Dark Mode
  theme_void(base_family = "montserrat") +
  theme(
    # Cor de fundo: "Midnight Blue" ultra escuro
    plot.background = element_rect(fill = "#0B1120", color = NA),
    panel.background = element_rect(fill = "#0B1120", color = NA),
    plot.margin = margin(t = 40, r = 50, b = 30, l = 40),
    
    # Estilização dos textos
    plot.title = element_markdown(color = "#FFFFFF", size = 22, margin = margin(b = 6), hjust = 0),
    plot.subtitle = element_text(color = "#94A3B8", size = 13, margin = margin(b = 40), hjust = 0),
    plot.caption = element_markdown(color = "#475569", size = 10, margin = margin(t = 30), hjust = 1),
    
    # Eixo Y agora funciona como os títulos de cada barra
    axis.text.y = element_text(
      color = "#F8FAFC", 
      size = 14, 
      face = "bold", 
      hjust = 1, 
      margin = margin(r = 15)
    )
  )
###################################################################################################################################

# 4° Pergunta do trabalho:" que insights podem ser gerados sobre os tipos de acidentes predominantes e suas causas? "

# I. Saber qual tipo de acidente acontece mais, Colisão? Saída de pista?
top_tipos <- dados %>%                                     # Pega a tabela 'dados' E ENTÃO " %>% "...
  count(tipo_acidente, sort = TRUE) %>%                    # Conta quantas vezes cada 'tipo' aparece
                                                           # e ja ordena do maior para o menor com o sort(TRUE)
  slice(1:10)                                              # ele divide/fatia a tabela e joga fora tudo o que estiver
                                                           # abaixo de 10 ou a qnt que vc colocar, o famoso "TOPX"
print(top_tipos)                                           # mostra a tabela resumida que criamos agora

# II.Saber o motivo principal, Falta de atenção? Velocidade?

top_causas <- dados %>%                                    # Pega a tabela 'dados' E ENTÃO " %>% "...
  count(causa_acidente, sort = TRUE) %>%                   # Conta quantas vezes cada 'causa' aparece'
                                                           # e ja ordena do maior para o menor com o sort(TRUE)
  mutate(porcentagem =
           round(
             (n / sum(n)) * 100, 1)) %>%                   # Cria a coluna %
    slice(1:10)                                            # ele divide/fatia a tabela e joga fora tudo o que estiver depois
                                                           # abaixo de 10 ou a qnt que vc colocar, o famoso "TOPX"
print(top_causas)

# 1. Carregando a fonte moderna
font_add_google("Montserrat", "montserrat")
showtext_auto()

# 2. Engenharia de Dados Visuais
# Preparando os rótulos e organizando os dados
dados_causas <- top_causas %>%
  mutate(
    # Ordena as causas baseadas no volume (n)
    causa_acidente = reorder(causa_acidente, n),
    
    # Criação do Rótulo Rich-Text (Número em branco negrito + Porcentagem inteira em vermelho neon)
    label_html = paste0(
      "<span style='color:#FFFFFF; font-size:15pt;'><b>", 
      format(n, big.mark = ".", decimal.mark = ","), 
      "</b>  </span>  <span style='color:#FF3366; font-size:10pt;'> ", 
      round(porcentagem, 0), "% </span>"
    )
  )

# Define o limite máximo da tela para a "trilha" de fundo das barras
max_val_causas <- max(dados_causas$n) * 1.25

# 3. Construção do Gráfico Dark Dashboard (Alarme)
ggplot(dados_causas, aes(y = causa_acidente, x = n)) +
  
  # A: "Trilha" de fundo escura (Efeito de barra de progresso)
  geom_col(aes(x = max_val_causas), fill = "#1E293B", width = 0.35) +
  
  # B: A Barra de Dados principal (Vermelho Alarme Neon)
  geom_col(fill = "#FF3366", width = 0.35, alpha = 0.95) +
  
  # C: Rótulos voando à direita da barra (sem cortes)
  geom_richtext(
    aes(label = label_html),
    hjust = -0.05,        # Descola o texto levemente do fim da barra
    fill = NA,            # Fundo transparente
    label.color = NA,     # Sem bordas
    family = "montserrat"
  ) +
  
  # D: Títulos impactantes com peso de fonte contrastante
  labs(
    title = "**PRINCIPAIS CAUSAS DE ACIDENTES**",
    subtitle = "Análise volumétrica dos principais fatores de risco mapeados",
    caption = "**Base de Dados:** Processamento Analítico"
  ) +
  
  # E: O Tema UI/UX Dark Mode
  theme_void(base_family = "montserrat") +
  theme(
    # Cor de fundo: "Midnight Blue" ultra escuro
    plot.background = element_rect(fill = "#0B1120", color = NA),
    panel.background = element_rect(fill = "#0B1120", color = NA),
    plot.margin = margin(t = 40, r = 50, b = 30, l = 40),
    
    # Estilização dos textos
    plot.title = element_markdown(color = "#FFFFFF", size = 22, margin = margin(b = 6), hjust = 0),
    plot.subtitle = element_text(color = "#94A3B8", size = 13, margin = margin(b = 40), hjust = 0),
    plot.caption = element_markdown(color = "#475569", size = 10, margin = margin(t = 30), hjust = 1),
    
    # Eixo Y com os nomes das causas
    axis.text.y = element_text(
      color = "#F8FAFC", 
      size = 13, 
      face = "bold", 
      hjust = 1, 
      margin = margin(r = 15)
    )
  )