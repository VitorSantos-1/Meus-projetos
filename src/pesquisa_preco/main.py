import time
import re
from urllib.parse import quote, quote_plus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

# ==========================================
# CONFIGURAÇÃO DOS CONCORRENTES
# ==========================================
CONCORRENTES = {
    "diniz": {
        "nome": "Diniz Supermercados",
        "url_busca": "https://www.dinizsupermercados.com.br/busca?termo={produto}",
        "encoder": quote
    },
    "saoluiz": {
        "nome": "Mercadinhos São Luiz",
        "url_busca": "https://mercadinhossaoluiz.com.br/loja/355?origin=searching&search={produto}",
        "encoder": quote_plus
    }
}

# ==========================================
# EXTRATOR DE CATÁLOGO (VARREDURA COMPLETA)
# ==========================================
def extrair_dados_do_texto(texto_card: str) -> dict:
    linhas = [l.strip() for l in texto_card.split('\n') if l.strip()]
    
    precos = []
    candidatos_nome = []
    
    for linha in linhas:
        match_preco = re.search(r'R\$\s*\d+[.,]\d{2}', linha, re.IGNORECASE)
        if match_preco:
            precos.append(match_preco.group())
            continue
            
        linha_lower = linha.lower()
        if linha_lower in ["adicionar", "comprar", "esgotado", "ver detalhes", "un"]:
            continue
            
        if len(linha) > 4 and "%" not in linha:
            candidatos_nome.append(linha)

    if not precos or not candidatos_nome:
        return None
        
    nome_encontrado = candidatos_nome[0]
    
    if "oferta" in nome_encontrado.lower() or "leve" in nome_encontrado.lower():
        if len(candidatos_nome) > 1:
            nome_encontrado = candidatos_nome[1]
            
    # ==========================================
    # CORREÇÃO DA LÓGICA DE PREÇOS
    # ==========================================
    if len(precos) > 1:
        # Função interna para converter "R$ 4,99" em 4.99 para o Python calcular
        def _para_float(p):
            try:
                return float(re.sub(r"[^\d,.]", "", p).replace(",", "."))
            except Exception:
                return 0.0

        val1 = _para_float(precos[0])
        val2 = _para_float(precos[1])

        # O maior valor obrigatoriamente é o Normal, o menor é a Oferta
        if val1 > val2:
            preco_normal = precos[0]
            preco_oferta = precos[1]
        else:
            preco_normal = precos[1]
            preco_oferta = precos[0]
    else:
        # Se só tem 1 preço no card
        preco_normal = precos[0]
        preco_oferta = "—"
    
    return {
        "produto_encontrado": nome_encontrado,
        "preco_normal": preco_normal,
        "preco_oferta": preco_oferta
    }

# ==========================================
# SCRAPER: SELENIUM WEBDRIVER (COM PAGINAÇÃO)
# ==========================================
def raspar_concorrente(produto: str, chave: str, config: dict, driver) -> list:
    loja = config["nome"]
    produto_url = config["encoder"](produto)
    url = config["url_busca"].replace("{produto}", produto_url)
    
    print(f"\n{Fore.CYAN}🔎 Varrendo catálogo de {loja}...{Style.RESET_ALL}")
    print(f"   Link: {Fore.BLACK}{Style.DIM}{url}{Style.RESET_ALL}")
    
    try:
        driver.get(url)
        time.sleep(5)
        
        resultados = []
        textos_processados = set()
        
        # LOOP DE PAGINAÇÃO (MÁXIMO DE 5 PÁGINAS)
        limite_paginas = 5
        
        for pagina_atual in range(1, limite_paginas + 1):
            
            # Rola a página atual para forçar carregamento das imagens e preços
            for _ in range(4):
                driver.execute_script("window.scrollBy(0, 600);")
                time.sleep(1)
                
            # Extrai os cards que estão visíveis nesta página
            elementos = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]/ancestor::div[contains(@class, 'product') or contains(@class, 'item') or contains(@class, 'card')] | //*[contains(text(), 'R$')]/ancestor::li")
            if not elementos:
                elementos = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]/..")
                
            itens_nesta_pagina = 0
            for el in elementos:
                texto = el.text
                if not texto or texto in textos_processados:
                    continue
                    
                if "R$" in texto:
                    textos_processados.add(texto)
                    dados = extrair_dados_do_texto(texto)
                    if dados:
                        dados["supermercado"] = loja
                        resultados.append(dados)
                        itens_nesta_pagina += 1
            
            # Rola até o final absoluto da página para ver se tem botão de "Próxima"
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            
            # TENTA ACHAR O BOTÃO DE PRÓXIMA PÁGINA OU CARREGAR MAIS
            try:
                # Procura por botões com as palavras "Carregar mais", "Mostrar mais" ou botões de seta/próxima
                xpaths_paginacao = [
                    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'carregar mais')]",
                    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mostrar mais')]",
                    "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÓ', 'abcdefghijklmnopqrstuvwxyzo'), 'próxima')]",
                    "//a[contains(@class, 'next') or contains(@class, 'proxima') or contains(@class, 'page-link-next')]",
                    "//button[contains(@class, 'load-more')]"
                ]
                
                clicou_proxima = False
                for xpath in xpaths_paginacao:
                    botoes = driver.find_elements(By.XPATH, xpath)
                    for btn in botoes:
                        if btn.is_displayed() and btn.is_enabled():
                            driver.execute_script("arguments[0].click();", btn)
                            print(f"   {Fore.MAGENTA}➡ Mudando para a página {pagina_atual + 1}...{Style.RESET_ALL}")
                            time.sleep(4) # Espera a nova página carregar
                            clicou_proxima = True
                            break
                    if clicou_proxima:
                        break # Sai do loop de xpaths se já achou o botão
                
                # Se vasculhou a página inteira e não achou botão de próxima, encerra a paginação
                if not clicou_proxima:
                    break
                    
            except Exception:
                # Se der algum erro ao tentar procurar a páginação, assume que é a última página
                break
                    
        if resultados:
            print(f"   {Fore.GREEN}✔ Extração concluída. {len(resultados)} iten(s) coletado(s).{Style.RESET_ALL}")
        else:
            print(f"   {Fore.YELLOW}⚠ Nenhum produto correspondente visível na tela.{Style.RESET_ALL}")
            
        return resultados

    except Exception as e:
        print(f"   {Fore.RED}✘ Falha na raspagem: {e}{Style.RESET_ALL}")
        return []

def executar_busca(produto: str):
    resultados_totais = []
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    
    print(f"{Fore.MAGENTA}Iniciando o navegador...{Style.RESET_ALL}")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        for chave, config in CONCORRENTES.items():
            if "no " in produto.lower() and chave not in produto.lower().replace("são luiz", "saoluiz"):
                continue
                
            produto_limpo = produto.lower().split(" no ")[0].strip()
            dados = raspar_concorrente(produto_limpo, chave, config, driver)
            resultados_totais.extend(dados)
    finally:
        driver.quit()
        
    return resultados_totais

# ==========================================
# INTERFACE CLI
# ==========================================
def main():
    while True:
        print(f"\n{Fore.YELLOW}Catálogo para pesquisar (ou 0 para sair): {Style.RESET_ALL}", end="")
        entrada = input().strip()
        
        if not entrada: continue
        if entrada == "0": break
        
        resultados = executar_busca(entrada)
        
        if resultados:
            colunas = ["Loja", "Produto Encontrado", "Preço Normal", "Oferta"]
            linhas = [
                [
                    r.get("supermercado", "—"), 
                    r.get("produto_encontrado", "—")[:55], 
                    r.get("preco_normal", "—"),
                    r.get("preco_oferta", "—")
                ] for r in resultados
            ]
            print("\n" + tabulate(linhas, headers=colunas, tablefmt="rounded_outline"))
        else:
            print(f"\n{Fore.RED}Nenhum resultado retornado.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
