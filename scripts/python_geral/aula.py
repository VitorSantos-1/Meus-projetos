# lógica, criando uma automação passo a passo para o seu sistema
import pandas as pd
import pyautogui
import time
# ______________________________________________________________________________________#

# > variaveis
link_do_sistema = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"
usuario = "pythonimpressionador@gmail.com"
senha = "sua senha muito muito muito dificilima"
# ______________________________________________________________________________________#

# > passo 1: entrar no sistema
# determinar um tempo para cada comando
pyautogui.PAUSE = 1
# abrir o menu iniciar, press = apertar uma tecla
pyautogui.press("win")
# escrever o nome do programa que quero abrir, write = escreve texto
pyautogui.write("Chrome")
# apertar enter para abrir o programa, press = apertar uma tecla
pyautogui.press("enter")
# escrever o link/sistema que quero abrir, write = escreve texto
pyautogui.write(link_do_sistema)
# apertar enter para abrir o programa, press = apertar uma tecla
pyautogui.press("enter")

# = agora com o sistema aberto, vou esperar 5 segundos para a página carregar
# esperar 5 segundos, o time.sleep pausa o código por um tempo determinado
time.sleep(3)

# _______________________________________________________________________________________#

# > passo 2: fazer o login

# clicar na posição do campo de email, obtida com o auxiliar_aula.py
pyautogui.click(x=696, y=423)
# escrever o usuário no campo de email, write = escreve texto
pyautogui.write(usuario)
# usar o tab para ir para o campo de senha, press = apertar uma tecla
pyautogui.press("tab")
# escrever a senha no campo de senha, write = escreve texto
pyautogui.write(senha)
# usar o tab para ir para o botão entrar/logar, press = apertar uma tecla
pyautogui.press("tab")
# apertar enter para fazer o login, press = apertar uma tecla
pyautogui.press("enter")
# esperar 5 segundos para garantir que a página carregou
time.sleep(5)

# _______________________________________________________________________________________#

# > passo 3: abrir a base de dados

# importar a base de dados
tabela = pd.read_csv("produtos.csv")  # ler a base de dados, usando o pandas
print(tabela)  # mostrar a base de dados, para conferência no console/terminal

# _______________________________________________________________________________________#

# repita o passo 4 (por linhas[index] da tabela de produtos)
# para cada linha na tabela de produtos, repita até acabar.

for linha in tabela.index:
    # > passo 4: cadastrar produto
    # > passo 5: repetir o passo 4 até acabar a lista de produtos
    # clicar no campo nome do produto, posição obtida com o auxiliar_aula.py
    pyautogui.click(x=686, y=289)
    # -----------------------------------------------------------------#
    # pegar o codigo do produto por linha
    codigo = str(tabela.loc[linha, "codigo"])
    # .codigo
    pyautogui.write(codigo)
    # usar o tab para ir para o próximo campo, press = apertar uma tecla
    pyautogui.press("tab")
    # -----------------------------------------------------------------#
    # pegar a marca do produto por linha
    marca = str(tabela.loc[linha, "marca"])
    # .marca
    pyautogui.write(marca)
    # usar o tab para ir para o próximo campo, press = apertar uma tecla
    pyautogui.press("tab")
    # -----------------------------------------------------------------#
    # pegar o tipo do produto por linha
    tipo = str(tabela.loc[linha, "tipo"])
    # .tipo
    pyautogui.write(tipo)
    # usar o tab para ir para o próximo campo, press = apertar uma tecla
    pyautogui.press("tab")
    # -----------------------------------------------------------------#
    # pegar a categoria do produto por linha
    categoria = str(tabela.loc[linha, "categoria"])
    # .categoria
    pyautogui.write(categoria)
    # usar o tab para ir para o próximo campo, press = apertar uma tecla
    pyautogui.press("tab")
    # -----------------------------------------------------------------#
    # pegar o preco do produto por linha
    preco = str(tabela.loc[linha, "preco_unitario"])
    # .preco
    pyautogui.write(preco)
    # usar o tab para ir para o próximo campo, press = apertar uma tecla
    pyautogui.press("tab")
    # -----------------------------------------------------------------#
    # pegar o custo do produto por linha
    custo = str(tabela.loc[linha, "custo"])
    # .custo
    pyautogui.write(custo)
    # usar o tab para ir para o próximo campo, press = apertar uma tecla
    pyautogui.press("tab")
    # -----------------------------------------------------------------#
    # pegar as obs do produto por linha
    obs = str(tabela.loc[linha, "obs"])
    # ele verifica se tem obs, se tiver ele escreve, se nao ele deixa vazio
    if obs != "nan":
        # .obs
        pyautogui.write(obs)
    # usar o tab para ir para o botão salvar, press = apertar uma tecla
    pyautogui.press("tab")
    # -----------------------------------------------------------------#
    # .salvar o produto
    pyautogui.press("enter")
    # -----------------------------------------------------------------#
    # voltar ao inicio para cadastrar o próximo produto
    pyautogui.scroll(5000)  # rolar a tela para cima
    # -----------------------------------------------------------------#

# _______________________________________________________________________________________#
# > fim: finalização do código
print("Fim do programa")