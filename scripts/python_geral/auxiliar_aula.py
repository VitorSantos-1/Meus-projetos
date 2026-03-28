import pyautogui
import time

# código para descobrir a posição do mouse na tela
time.sleep(5)  # esperar 5 segundos para garantir que a página carregou
print(pyautogui.position())  # descobrir a posição do mouse na tela
