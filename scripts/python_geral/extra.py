import pandas as pd
import numpy as np  # noqa: F401
import matplotlib.pyplot as plt  # noqa: F401
import seaborn as sns  # noqa: F401
# importar as bibliotecas pandas, numpy, matplotlib.pyplot e seaborn
# com apelidos pd, np, plt e sns respectivamente

# #######################################################################################################
# INICIO DA EXPLORAÇÃO DOS DADOS
# :::::::::::::::::::::::::::::::::::::::#

dados = "https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv"  # noqa: E501
# Carregando o link do arquivo csv em uma variável chamada dados

tabela = pd.read_csv(dados)
# Pedi para o pandas ler o arquivo csv em uma variável chamada tabela
tabela.head()
# mostrando as primeiras linhas da tabela no console/terminal
tabela.info()
# mostrando as informações sobre a tabela no console/terminal
tabela.describe()
# mostrando as informações estatísticas da tabela no console/terminal
tabela.shape
# mostrando a quantidade de linhas e colunas da tabela no console/terminal
linhas, colunas = tabela.shape[0], tabela.shape[1]
# armazenando a quantidade de linhas e colunas em variáveis separadas
# usando shape começamos do zero
# por isso colocamos [0] para linhas e [1] para colunas, já que é um índice

print(f"A tabela possui {linhas} linhas e {colunas} colunas.")
# imprimindo a quantidade de linhas e colunas da tabela no console/terminal
tabela.columns
# mostrando os nomes das colunas da tabela no console/terminal

# ########################
# INICIO DAS TRADUÇÕES
# ::::::::::::::::::::::::#
tabela.rename(columns={
    'work_year': 'ano',
    'experience_level': 'senioridade',
    'employment_type': 'contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'salario_usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remoto',
    'company_location': 'empresa',
    'company_size': 'tamanho_empresa'
}, inplace=True  # para salvar as alterações
)
# traduzindo os nomes das colunas para português usando rename

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mapa_senioridade = {
    'EN': 'Junior',
    'MI': 'Pleno',
    'SE': 'Senior',
    'EX': 'Executivo'
}
# Traduzindo as categorias da coluna 'senioridade' para português usando map
tabela['senioridade'] = tabela['senioridade'].map(mapa_senioridade)
# aplicando o mapeamento para traduzir os valores da coluna 'senioridade'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mapa_contrato = {
    'FT': 'Tempo Integral',
    'PT': 'Meio Período',
    'CT': 'Contrato',
    'FL': 'Freelance'
}
# Traduzindo as categorias da coluna 'contrato'
tabela['contrato'] = tabela['contrato'].map(mapa_contrato)
# aplicando o mapeamento para traduzir os valores da coluna 'contrato

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mapa_tamanho = {
    'S': 'Pequena',
    'M': 'Media',
    'L': 'Grande'
}
# Traduzindo as categorias da coluna 'tamanho_empresa'
tabela['tamanho_empresa'] = tabela['tamanho_empresa'].map(mapa_tamanho)
# Traduzindo as categorias da coluna 'tamanho_empresa'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

mapa_remoto = {
    0: 'Presencial',
    50: 'Híbrido',
    100: 'Remoto'
}
# Traduzindo as categorias da coluna 'remoto'
tabela['remoto'] = tabela['remoto'].map(mapa_remoto)
# aplicando o mapeamento para traduzir os valores da coluna 'remoto'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# FIM DAS TRADUÇÕES
# ::::::::::::::::::::::::#
# #############################

# INICIO DAS ANÁLISES EXPLORATÓRIAS INICIAIS
# ::::::::::::::::::::::::::::::::::::::#
# ##############################################

tabela["senioridade"]. value_counts()
# calculando a frequencia/quantidade de cargos por nível de experiência
tabela["contrato"].value_counts()
# calculando a frequencia/quantidade de cargos por tipo de emprego
tabela['tamanho_empresa'].value_counts()
# calculando a frequencia/quantidade de cargos por tamanho da empresa
tabela["remoto"].value_counts()
# calculando a frequencia/quantidade de cargos por nível de trabalho remoto
tabela.head()
# mostrando as primeiras linhas da tabela no console/terminal
tabela.describe(include='object')
# mostrando as informações estatísticas da tabela para colunas categóricas

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# FIM DAS ANÁLISES EXPLORATÓRIAS INICIAIS
# ::::::::::::::::::::::::#
# ###########################################
# #######################################################################################################

# INICIO DA PREPARAÇÃO E LIMPEZA DOS DADOS
# :::::::::::::::::::::::::::::::::::::::::::
# #############################################

tabela.head()
# mostrando as primeiras linhas da tabela no console/terminal
tabela.isnull()
# verificando a existência de valores nulos na tabela, retornando True ou False
# se houver valores nulos, retornará True, caso contrário, False
tabela.isnull().sum()
# somando a quantidade de valores nulos por coluna na tabela
tabela['ano'].unique()
# verificando os valores únicos da coluna 'ano' na tabela
tabela[tabela.isnull().any(axis=1)]
# mostrando as linhas que possuem valores nulos na tabela

tabela_limpa = tabela.dropna()
# removendo as linhas que possuem valores nulos na tabela
tabela_limpa.isnull().sum()
# verificando novamente a existência de valores nulos
tabela_limpa.head()
# mostrando as primeiras linhas da tabela limpa
tabela_limpa.info()
# mostrando as informações sobre a tabela limpa
tabela_limpa = tabela_limpa.assign(
    ano=tabela_limpa['ano'].astype('int64'),
    salario_usd=tabela_limpa['salario_usd'].astype('float64'),
    salario=tabela_limpa['salario'].astype('float64')
    )
# convertendo a coluna 'ano' para o tipo inteiro na tabela limpa
tabela_limpa.info()
# mostrando as informações sobre a tabela limpa
tabela_limpa.head()
# mostrando as primeiras linhas da tabela limpa

# FIM DA PREPARAÇÃO E LIMPEZA DOS DADOS
# :::::::::::::::::::::::::::::::::::::::::::#
# ############################################
# #######################################################################################################
