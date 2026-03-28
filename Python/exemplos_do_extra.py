import pandas as pd
import numpy as np  # noqa: F401
import matplotlib.pyplot as plt  # noqa: F401
import seaborn as sns  # noqa: F401
# importar as bibliotecas pandas, numpy, matplotlib.pyplot e seaborn
# com apelidos pd, np, plt e sns respectivamente

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv#
# ALGUNS EXEMPLOS DE PREENCHIMENTO DE VALORES NULOS FORA DA BASE DE DADOS
# :::::::::::::::::::::::::::::::::::::::::::::::::#

# EXEMPLO_1 DE PREENCHIMENTO DE VALORES NULOS

tabela_salarios = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'Carlos', 'Daniela', 'Val'],
    'salario': [4000, np.nan, 5000, np.nan, 100000]
})
# criando um DataFrame de exemplo com valores nulos na coluna 'salario'
tabela_salarios['salario_media'] = tabela_salarios['salario'].fillna(
    tabela_salarios['salario'].mean().round(2))
# preenchendo os valores nulos na coluna 'salario' com a média dos salários
tabela_salarios['salario_mediana'] = tabela_salarios['salario'].fillna(
    tabela_salarios['salario'].median())
# preenchendo os valores nulos na coluna 'salario' com a mediana dos salários

tabela_salarios
# mostrando a tabela de salários no console/terminal

# FIM DO EXEMPLO_1 DE PREENCHIMENTO DE VALORES NULOS
# #######################################################################################################

# EXEMPLO_2 DE PREENCHIMENTO DE VALORES NULOS

df_temperaturas = pd.DataFrame({
    "Dia": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    "Temperatura": [30, np.nan, np.nan, 28, 27]
})
# Criação do DataFrame de exemplo com valores nulos na coluna 'Temperatura'
df_temperaturas["preenchido_ffill"] = df_temperaturas["Temperatura"].ffill()
# Aplicação do método ffill()
df_temperaturas["preenchido_bfill"] = df_temperaturas["Temperatura"].bfill()
# Aplicação do método bfill()
df_temperaturas
# mostrando a tabela de temperaturas no console/terminal

# FIM DO EXEMPLO_2 DE PREENCHIMENTO DE VALORES NULOS
# #######################################################################################################

# EXEMPLO_3 DE PREENCHIMENTO DE VALORES NULOS

df_cidades = pd.DataFrame({
    'nome': ["Ana", "Bruno", "Carlos", "Daniele", "Val"],
    'cidade': ["São Paulo", np.nan, "Curitiba", np.nan, "Belém"]
})
# Criação do DataFrame de exemplo com valores nulos na coluna 'cidade'
df_cidades['cidade_preenchida'] = df_cidades["cidade"].fillna("Não informado")
# Aplicação do método fillna()
df_cidades
# mostrando a tabela de cidades no console/terminal

# FIM DO EXEMPLO_3 DE PREENCHIMENTO DE VALORES NULOS
# #######################################################################################################

# FIM DO CÓDIGO DE EXEMPLOS DE PREENCHIMENTO DE VALORES NULOS
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
