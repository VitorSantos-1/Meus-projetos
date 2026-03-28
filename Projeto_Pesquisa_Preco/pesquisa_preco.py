import time
import re
import requests
import csv
import os
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote, quote_plus, urlparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from colorama import Fore, Style, init
from tabulate import tabulate
from dotenv import load_dotenv
from openai import OpenAI

init(autoreset=True)

# ==========================================
# CONFIGURACAO DA IA (OPENAI)
# ==========================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None
    print(f"{Fore.RED}Aviso: OPENAI_API_KEY nao encontrada no arquivo .env. A busca por IA sera desativada.{Style.RESET_ALL}")

# ==========================================
# FONTES REAIS DE EAN POR NOME DE PRODUTO
# ==========================================

def buscar_ean_mercado_livre(nome_produto):
    """
    Busca no Mercado Livre: acessa a pagina de resultados e entra na
    pagina do 1o produto para extrair o EAN do JSON-LD ou especificacoes.
    Retorna (ean, metodo) ou (None, None).
    """
    try:
        query = quote_plus(nome_produto)
        # API interna de busca do ML retorna JSON com dados do produto
        url_api = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit=3"
        resp = requests.get(url_api, headers=HEADERS_REQUESTS, timeout=8)
        if resp.status_code == 200:
            dados = resp.json()
            resultados = dados.get("results", [])
            for item in resultados:
                item_id = item.get("id", "")
                if not item_id:
                    continue
                # Busca detalhes do item (tem gtin/EAN)
                url_item = f"https://api.mercadolibre.com/items/{item_id}"
                r2 = requests.get(url_item, headers=HEADERS_REQUESTS, timeout=8)
                if r2.status_code == 200:
                    det = r2.json()
                    # 1) campo gtin direto
                    gtin = det.get("attributes") or []
                    for attr in gtin:
                        if attr.get("id") in ("GTIN", "EAN", "BARCODE"):
                            val = str(attr.get("value_name", "") or "").strip()
                            if re.fullmatch(r'\d{8,14}', val):
                                return val, "Nivel 6A (Mercado Livre API)"
                    # 2) campo ean_code ou similar
                    for attr in (det.get("attributes") or []):
                        val = str(attr.get("value_name", "") or "")
                        if re.fullmatch(r'\d{13}', val):
                            return val, "Nivel 6A (Mercado Livre API)"
    except Exception:
        pass
    return None, None


def buscar_ean_buscape(nome_produto):
    """
    Busca no Buscapé: usa a busca deles e extrai EAN dos snippets HTML.
    Retorna (ean, metodo) ou (None, None).
    """
    try:
        query = quote_plus(nome_produto)
        url = f"https://www.buscape.com.br/search?q={query}"
        headers_b = {
            **HEADERS_REQUESTS,
            'Referer': 'https://www.buscape.com.br/'
        }
        resp = requests.get(url, headers=headers_b, timeout=8)
        if resp.status_code == 200:
            # Procura EAN no HTML dos cards de resultado
            matches = re.findall(
                r'(?i)(?:"gtin"|"ean"|"barcode")[\s]*:[\s]*["\']?(\d{13})["\']?',
                resp.text
            )
            if matches:
                return matches[0], "Nivel 6B (Buscapé)"
            # Tenta no texto visivel
            match2 = re.search(
                r'(?i)(?:EAN|GTIN|codigo de barras)[^\d]{0,20}(\d{13})',
                resp.text
            )
            if match2:
                return match2.group(1), "Nivel 6B (Buscapé)"
    except Exception:
        pass
    return None, None


def buscar_ean_google_shopping(nome_produto):
    """
    Busca no Google por EAN real em sites de supermercados e lojas.
    Usa queries direcionadas a sites que publicam EAN nas paginas.
    Retorna (ean, metodo) ou (None, None).
    """
    tentativas = [
        f'{nome_produto} EAN site:mercadolivre.com.br',
        f'{nome_produto} "codigo de barras" EAN 13 digitos',
        f'{nome_produto} GTIN EAN supermercado',
    ]
    for query_str in tentativas:
        try:
            url = f"https://www.google.com/search?q={quote_plus(query_str)}&num=5&hl=pt-BR"
            headers_g = {
                **HEADERS_REQUESTS,
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'https://www.google.com/'
            }
            resp = requests.get(url, headers=headers_g, timeout=8)
            if resp.status_code == 200:
                # EAN de 13 digitos proximo de termos de referencia
                matches = re.findall(
                    r'(?i)(?:EAN|GTIN|barcode|codigo)[^\d]{0,30}(\d{13})',
                    resp.text
                )
                if matches:
                    return matches[0], "Nivel 6C (Google Shopping)"
                # Qualquer sequencia de 13 digitos que pareca EAN (comeca com 7 ou 78=BR)
                matches_br = re.findall(r'\b(7[0-9]{12})\b', resp.text)
                if matches_br:
                    return matches_br[0], "Nivel 6C (Google - EAN BR)"
        except Exception:
            pass
    return None, None


def buscar_ean_open_food_facts(nome_produto):
    """
    Consulta a API do Open Food Facts (global + BR).
    Retorna (ean, metodo) ou (None, None).
    """
    # Tenta variações do nome
    palavras = nome_produto.split()
    termos = [nome_produto]
    if len(palavras) >= 2:
        termos.append(" ".join(palavras[:3]))
    if len(palavras) >= 2:
        termos.append(" ".join(palavras[:2]))

    for base_url in [
        "https://br.openfoodfacts.org/cgi/search.pl",
        "https://world.openfoodfacts.org/cgi/search.pl"
    ]:
        for termo in termos:
            try:
                url = f"{base_url}?search_terms={quote_plus(termo)}&search_simple=1&action=process&json=1&page_size=3"
                resp = requests.get(url, headers=HEADERS_REQUESTS, timeout=7)
                if resp.status_code == 200:
                    dados = resp.json()
                    for p in dados.get("products", []):
                        codigo = str(p.get("code", "") or "")
                        if not re.fullmatch(r'\d{8,14}', codigo):
                            continue
                        # Verifica relevancia minima
                        nome_off = " ".join([
                            p.get("product_name", "") or "",
                            p.get("product_name_pt", "") or "",
                            p.get("brands", "") or ""
                        ]).lower()
                        palavras_chave = [w for w in nome_produto.lower().split() if len(w) > 3]
                        if any(w in nome_off for w in palavras_chave):
                            return codigo, "Nivel 6D (Open Food Facts)"
            except Exception:
                pass
    return None, None


def buscar_ean_cosmos(nome_produto):
    """
    Consulta a API do Cosmos/Bluesoft (base brasileira de GTINs).
    Requer token gratuito em cosmos.bluesoft.com.br.
    Retorna (ean, metodo) ou (None, None).
    """
    cosmos_token = os.getenv("COSMOS_TOKEN", "")
    if not cosmos_token:
        return None, None  # Pula se nao tiver token
    try:
        url = f"https://api.cosmos.bluesoft.com.br/gtins?q={quote_plus(nome_produto)}&page=1&per_page=5"
        headers_cosmos = {
            **HEADERS_REQUESTS,
            'X-Cosmos-Token': cosmos_token,
            'Accept': 'application/json'
        }
        resp = requests.get(url, headers=headers_cosmos, timeout=8)
        if resp.status_code == 200:
            dados = resp.json()
            for item in (dados.get("data") or []):
                gtin = str(item.get("gtin", "") or "")
                if not re.fullmatch(r'\d{8,14}', gtin):
                    continue
                descricao = (item.get("description", "") or "").lower()
                palavras_chave = [w for w in nome_produto.lower().split() if len(w) > 3]
                if any(w in descricao for w in palavras_chave):
                    return gtin, "Nivel 6E (Cosmos/Bluesoft)"
    except Exception:
        pass
    return None, None


# ==========================================
# PIPELINE COMPLETO DE BUSCA DE EAN POR NOME
# ==========================================
def buscar_ean_por_nome(nome_produto):
    """
    Pipeline de busca de EAN por nome de produto.
    Ordem: ML API > Buscapé > Google Shopping > Open Food Facts > Cosmos > IA (ultimo recurso).
    Retorna (ean, metodo_str).
    """
    print(f"   {Fore.CYAN}[EAN] Buscando codigo real para: {nome_produto[:55]}{Style.RESET_ALL}")

    # --- Mercado Livre API (mais confiavel para BR) ---
    ean, metodo = buscar_ean_mercado_livre(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Buscapé ---
    ean, metodo = buscar_ean_buscape(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Google Shopping (direcionado a EAN) ---
    ean, metodo = buscar_ean_google_shopping(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Open Food Facts ---
    ean, metodo = buscar_ean_open_food_facts(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Cosmos / Bluesoft (se tiver token no .env) ---
    ean, metodo = buscar_ean_cosmos(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- ULTIMO RECURSO: IA OpenAI (somente com certeza absoluta) ---
    if client:
        print(f"   {Fore.MAGENTA}[EAN] Fontes reais falharam. Consultando IA (somente certeza absoluta)...{Style.RESET_ALL}")
        time.sleep(3)
        try:
            prompt = (
                f"Produto: '{nome_produto}'\n\n"
                "Voce e uma base de dados de codigos de barras EAN de supermercados brasileiros.\n"
                "Regras ABSOLUTAS:\n"
                "- Responda SOMENTE com o EAN/GTIN de 13 digitos se voce tiver CERTEZA TOTAL (voce viu em base real).\n"
                "- IMPORTANTE: Se o produto teve mudanca de embalagem ou mudou de codigo, retorne o EAN MAIS RECENTE EM PRODUCAO.\n"
                "- Se tiver qualquer duvida, responda apenas: FALHA\n"
                "- NUNCA invente. Prefira sempre FALHA a um codigo errado."
            )
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Voce e uma base de dados de EAN. Retorne sempre o EAN mais atual e recente. Nunca invente codigos. Se nao tiver certeza absoluta, responda FALHA."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=20
            )
            texto = (response.choices[0].message.content or "").strip()
            if not texto.upper().startswith("FALHA"):
                match = re.search(r'\b(\d{8,14})\b', texto)
                if match:
                    return match.group(1), "Nivel 7 (IA - Ultimo Recurso)"
        except Exception as e:
            print(f"   {Fore.RED}Erro na IA: {str(e)[:80]}{Style.RESET_ALL}")

    return "—", "Falha Total"


# Alias para compatibilidade
def buscar_ean_com_ia(nome_produto):
    ean, _ = buscar_ean_por_nome(nome_produto)
    return ean


# ==========================================
# CONFIGURACAO DOS CONCORRENTES
# ==========================================
def buscar_ean_open_food_facts(nome_produto):
    """
    Consulta a API gratuita do Open Food Facts para buscar o EAN real do produto.
    Retorna (ean, metodo) ou (None, None) se nao encontrar.
    """
    try:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={quote_plus(nome_produto)}&search_simple=1&action=process&json=1&page_size=5&lc=pt&cc=br"
        resp = requests.get(url, headers=HEADERS_REQUESTS, timeout=8)
        if resp.status_code == 200:
            dados = resp.json()
            produtos = dados.get("products", [])
            for p in produtos:
                codigo = p.get("code", "")
                if codigo and re.fullmatch(r'\d{8,14}', str(codigo)):
                    # Verifica relevancia: nome do produto deve ter alguma palavra em comum
                    nome_off = (p.get("product_name", "") + " " + p.get("product_name_pt", "")).lower()
                    palavras_chave = [w for w in nome_produto.lower().split() if len(w) > 3]
                    if any(w in nome_off for w in palavras_chave):
                        return str(codigo), "Nivel 6A (Open Food Facts)"
    except Exception:
        pass
    return None, None


# ==========================================
# NIVEL 6B: COSMOS / BLUESOFT (base BR)
# ==========================================
def buscar_ean_cosmos(nome_produto):
    """
    Consulta a API publica do Cosmos (Bluesoft) para buscar EAN de produtos brasileiros.
    Retorna (ean, metodo) ou (None, None).
    """
    try:
        url = f"https://api.cosmos.bluesoft.com.br/gtins?q={quote_plus(nome_produto)}&page=1&per_page=5"
        headers_cosmos = {
            **HEADERS_REQUESTS,
            'X-Cosmos-Token': 'SEM_TOKEN',  # Funciona sem token para poucos requests
            'Accept': 'application/json'
        }
        resp = requests.get(url, headers=headers_cosmos, timeout=8)
        if resp.status_code == 200:
            dados = resp.json()
            itens = dados.get("data", []) or []
            for item in itens:
                gtin = item.get("gtin", "")
                if gtin and re.fullmatch(r'\d{8,14}', str(gtin)):
                    descricao = (item.get("description", "") or "").lower()
                    palavras_chave = [w for w in nome_produto.lower().split() if len(w) > 3]
                    if any(w in descricao for w in palavras_chave):
                        return str(gtin), "Nivel 6B (Cosmos/Bluesoft)"
    except Exception:
        pass
    return None, None


# ==========================================
# NIVEL 6C: GOOGLE SHOPPING (scraping)
# ==========================================
def buscar_ean_google_shopping(nome_produto):
    """
    Faz uma busca no Google por '{nome_produto} codigo de barras EAN site:openfoodfacts.org OR site:cosmos.bluesoft.com.br'
    e extrai qualquer EAN encontrado nos snippets.
    Retorna (ean, metodo) ou (None, None).
    """
    try:
        query = quote_plus(f"{nome_produto} EAN codigo barras")
        url = f"https://www.google.com/search?q={query}&num=5&hl=pt-BR"
        headers_google = {
            **HEADERS_REQUESTS,
            'Referer': 'https://www.google.com/'
        }
        resp = requests.get(url, headers=headers_google, timeout=8)
        if resp.status_code == 200:
            # Extrai EANs do HTML da pagina de resultados
            match = re.search(
                r'(?i)(?:EAN|GTIN|codigo de barras)[^\d]{0,30}(\d{13})',
                resp.text
            )
            if match:
                return match.group(1), "Nivel 6C (Google/Snippets)"
    except Exception:
        pass
    return None, None


# ==========================================
# NIVEL 6D: QUERY DIRETA OPEN FOOD FACTS POR NOME EXATO
# ==========================================
def buscar_ean_off_avancado(nome_produto):
    """
    Tenta variações do nome do produto no Open Food Facts para encontrar EAN.
    Divide o nome em partes (marca + descrição) e tenta cada parte.
    """
    # Tenta as primeiras 2 palavras (geralmente a marca)
    palavras = nome_produto.split()
    termos_tentativa = [nome_produto]
    if len(palavras) >= 2:
        termos_tentativa.append(" ".join(palavras[:2]))
    if len(palavras) >= 3:
        termos_tentativa.append(" ".join(palavras[:3]))

    for termo in termos_tentativa:
        try:
            url = f"https://br.openfoodfacts.org/cgi/search.pl?search_terms={quote_plus(termo)}&search_simple=1&action=process&json=1&page_size=3"
            resp = requests.get(url, headers=HEADERS_REQUESTS, timeout=8)
            if resp.status_code == 200:
                dados = resp.json()
                for p in dados.get("products", []):
                    codigo = p.get("code", "")
                    if codigo and re.fullmatch(r'\d{8,14}', str(codigo)):
                        return str(codigo), "Nivel 6D (Open Food Facts BR)"
        except Exception:
            pass
    return None, None


# ==========================================
# PIPELINE COMPLETO DE BUSCA DE EAN (substitui buscar_ean_com_ia)
# ==========================================
def buscar_ean_por_nome(nome_produto):
    """
    Pipeline de busca de EAN por nome de produto.
    Tenta fontes reais antes de usar a IA como ultimo recurso.
    Retorna (ean, metodo_str).
    """
    print(f"   {Fore.CYAN}[EAN] Buscando codigo real para: {nome_produto[:50]}{Style.RESET_ALL}")

    # --- Nivel 6A: Open Food Facts (global) ---
    ean, metodo = buscar_ean_open_food_facts(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Nivel 6B: Cosmos / Bluesoft (BR) ---
    ean, metodo = buscar_ean_cosmos(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Nivel 6D: Open Food Facts BR (variações do nome) ---
    ean, metodo = buscar_ean_off_avancado(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Nivel 6C: Google Shopping snippets ---
    ean, metodo = buscar_ean_google_shopping(nome_produto)
    if ean:
        print(f"   {Fore.GREEN}[EAN] Encontrado via {metodo}: {ean}{Style.RESET_ALL}")
        return ean, metodo

    # --- Nivel 7 (ULTIMO RECURSO): IA OpenAI ---
    if client:
        print(f"   {Fore.MAGENTA}[EAN] Fontes reais falharam. Consultando IA (ultimo recurso)...{Style.RESET_ALL}")
        time.sleep(5)  # Pausa reduzida
        try:
            prompt = f"""Voce e um banco de dados de codigos de barras EAN de supermercados brasileiros.

Produto: '{nome_produto}'

Regras ABSOLUTAS:
- Responda SOMENTE com o EAN/GTIN de 13 digitos se voce tiver CERTEZA ABSOLUTA.
- Certeza absoluta = voce ja viu este produto especifico em uma base de dados real.
- Se tiver qualquer duvida, responda apenas: FALHA
- NUNCA invente ou estime um codigo. Prefira sempre FALHA a um codigo errado."""

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Voce e uma base de dados de EAN. Voce so confirma codigos que conhece com certeza absoluta. Nunca invente."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=20
            )
            texto = (response.choices[0].message.content or "").strip()
            if texto.upper().startswith("FALHA"):
                return "—", "Falha Total"
            match = re.search(r'\b(\d{8,14})\b', texto)
            if match:
                return match.group(1), "Nivel 7 (IA - Ultimo Recurso)"
        except Exception as e:
            print(f"   {Fore.RED}Erro na IA: {str(e)[:80]}{Style.RESET_ALL}")

    return "—", "Falha Total"


# Alias para compatibilidade (nao e mais usado diretamente)
def buscar_ean_com_ia(nome_produto):
    ean, _ = buscar_ean_por_nome(nome_produto)
    return ean


# ==========================================
# CONFIGURACAO DOS CONCORRENTES
# ==========================================
CONCORRENTES = {
    "diniz": {
        "nome": "Diniz Supermercados",
        "url_busca": "https://www.dinizsupermercados.com.br/busca?termo={produto}",
        "encoder": quote,
        "ean_regex_url": r'ean=(\d{8,14})',
    },
    "saoluiz": {
        "nome": "Mercadinhos Sao Luiz",
        "url_busca": "https://mercadinhossaoluiz.com.br/loja/355?origin=searching&search={produto}",
        "encoder": quote_plus,
        "ean_regex_url": r'ean=(\d{8,14})',
    },
    "atacadao": {
        "nome": "Atacadao",
        "url_busca": "https://www.atacadao.com.br/s?q={produto}&sort=score_desc&page=0",
        "encoder": quote_plus,
        "ean_regex_url": r'(?:ean|gtin|barcode)[=\/](\d{8,14})',
    },
}

HEADERS_REQUESTS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}


# ==========================================
# EXPORTACAO PARA CSV
# ==========================================
def exportar_para_csv(resultados):
    if not resultados:
        return

    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"extracao_precos_{data_hora}.csv"
    colunas = ["Loja", "Produto Encontrado", "Preco Normal", "Oferta", "EAN", "Nivel de Extracao", "URL"]

    try:
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8-sig') as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=';')
            escritor.writerow(colunas)
            for r in resultados:
                escritor.writerow([
                    r.get("supermercado", "—"),
                    r.get("produto_encontrado", "—"),
                    r.get("preco_normal", "—"),
                    r.get("preco_oferta", "—"),
                    r.get("ean", "—"),
                    r.get("metodo_ean", "—"),
                    r.get("url", "—")
                ])
        print(f"\n{Fore.GREEN}Arquivo CSV salvo com sucesso: {nome_arquivo}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Erro ao salvar CSV: {e}{Style.RESET_ALL}")


# ==========================================
# MOTOR DE BUSCA DE EAN (NIVEIS 3, 4 E 5)
# ==========================================
def buscar_ean_profundo(url_produto, context_playwright):
    # NIVEIS 3, 3.5 E 4
    try:
        resposta = requests.get(url_produto, headers=HEADERS_REQUESTS, timeout=6)
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.text, 'html.parser')

            meta_tags = [
                sopa.find('meta', property='product:retailer_item_id'),
                sopa.find('meta', itemprop='gtin13'),
                sopa.find('meta', itemprop='sku')
            ]
            for meta in meta_tags:
                if meta and meta.get('content') and re.fullmatch(r'\d{8,14}', meta.get('content')):
                    return meta.get('content'), "Nivel 3 (Meta Tag)"

            scripts = sopa.find_all('script')
            for script in scripts:
                if not script.string:
                    continue
                match_json = re.search(
                    r'(?i)"(?:gtin13|gtin|sku|ean|barcode|ProductEan|codigo_barras|codigo)"\s*[:=]\s*["\']?(\d{8,14})["\']?',
                    script.string
                )
                if match_json:
                    return match_json.group(1), "Nivel 4 (JSON-LD/Script)"

            match_bruto = re.search(
                r'(?i)(?:EAN|C[óo]digo de barras|GTIN)[\s\S]{0,120}?(\d{8,14})',
                resposta.text
            )
            if match_bruto:
                return match_bruto.group(1), "Nivel 3.5 (Regex HTML)"
    except Exception:
        pass

    # ==========================================
    # NIVEL 5 (Playwright + Network Sniffer Inteligente)
    # ==========================================
    pagina_produto = None

    # Extrai segmentos uteis do URL do produto para usar como ancora de relevancia
    parsed_prod_url = urlparse(url_produto)
    slug_produto = parsed_prod_url.path.rstrip("/").split("/")[-1]  # ultimo segmento do path
    id_numerico_url = re.search(r'/(\d{5,})', url_produto)
    id_numerico_url = id_numerico_url.group(1) if id_numerico_url else ""

    # Coleta pares (conjunto_eans_unicos, endpoint_url) por resposta JSON
    # Cada entrada representa UMA resposta de rede
    respostas_sniffer = []  # [(set_de_eans_unicos, endpoint_url), ...]

    def interceptar_resposta(response):
        if "application/json" in response.headers.get("content-type", ""):
            try:
                dados_json = response.json()
                texto_dados = str(dados_json)
                matches = re.findall(
                    r'(?i)(?:gtin|ean|barcode|codigo_barras)["\']?\s*[:=]\s*["\']?(\d{8,14})["\']?',
                    texto_dados
                )
                eans_unicos = set(matches)
                if eans_unicos:
                    respostas_sniffer.append((eans_unicos, response.url))
            except:
                pass

    try:
        pagina_produto = context_playwright.new_page()

        # Ativa o espiao de rede ANTES de carregar a pagina
        pagina_produto.on("response", interceptar_resposta)

        # networkidle garante que todos os JSONs de background ja foram recebidos
        pagina_produto.goto(url_produto, timeout=15000, wait_until="networkidle")

        if respostas_sniffer:
            # CAMADA 1: separa respostas de produto-individual (1 EAN unico)
            # das respostas de catalogo/listagem (muitos EANs distintos)
            respostas_produto = [(eans, ep) for eans, ep in respostas_sniffer if len(eans) == 1]
            respostas_listagem = [(eans, ep) for eans, ep in respostas_sniffer if len(eans) > 1]

            def _score_endpoint(endpoint_url):
                """Pontua o quanto o endpoint esta relacionado ao produto atual."""
                score = 0
                if slug_produto and slug_produto in endpoint_url:
                    score += 10
                if id_numerico_url and id_numerico_url in endpoint_url:
                    score += 5
                # Endpoints que tipicamente sao de detalhe de produto
                for kw in ("/product/", "/produto/", "/item/", "/sku/", "/pdp/"):
                    if kw in endpoint_url:
                        score += 3
                return score

            ean_escolhido = None

            # CAMADA 2: entre os de produto-individual, escolhe o de maior score
            if respostas_produto:
                melhor_score = -1
                for eans, ep in respostas_produto:
                    score = _score_endpoint(ep)
                    if score > melhor_score:
                        melhor_score = score
                        ean_escolhido = next(iter(eans))
                # Se nao houve score positivo, pega o ultimo (mais recente = mais provavel)
                if ean_escolhido is None:
                    ean_escolhido = next(iter(respostas_produto[-1][0]))

            # CAMADA 3: fallback — APIs de listagem, escolhe pelo endpoint mais relevante
            if not ean_escolhido and respostas_listagem:
                melhor_score = -1
                for eans, ep in respostas_listagem:
                    score = _score_endpoint(ep)
                    if score > melhor_score:
                        melhor_score = score
                        ean_escolhido = next(iter(eans))

            if ean_escolhido:
                pagina_produto.close()
                return ean_escolhido, "Nivel 5.1 (Sniffer de API/Rede)"

        # Se nao pegou na rede, le o texto visivel da pagina (ex: 'Codigo de barras: XXXXX')
        texto_pagina = pagina_produto.inner_text("body")
        match_playwright = re.search(
            r'(?i)(?:EAN|C[óO]DIGO DE BARRAS)[\s\S]{0,50}?(\d{8,14})',
            texto_pagina
        )

        if match_playwright:
            pagina_produto.close()
            return match_playwright.group(1), "Nivel 5.2 (Texto visivel Playwright)"

        pagina_produto.close()
    except Exception as e:
        try:
            if pagina_produto:
                pagina_produto.close()
        except:
            pass

    return "—", "Falha nos sites"


# ==========================================
# RASPAGEM PRINCIPAL (CATALOGO)
# ==========================================
def extrair_dados_card(texto_card: str, html_card: str, url_produto: str, config: dict) -> dict:
    linhas = [l.strip() for l in texto_card.split('\n') if l.strip()]
    precos = []
    candidatos_nome = []
    ean_encontrado = None
    metodo_ean = "—"

    # Ruido tipico do Atacadao e outros sites
    NOMES_IGNORADOS = {"adicionar", "comprar", "esgotado", "ver detalhes", "un",
                       "/ cada", "/cada", "cada", "kg", "lt", "un.", "g"}

    for linha in linhas:
        match_preco = re.search(r'R\$\s*\d+[.,]\d{2}', linha, re.IGNORECASE)
        if match_preco:
            precos.append(match_preco.group())
            continue

        linha_lower = linha.lower().strip()
        # Filtra ruidos: textos curtos, nomes de botao, unidades e fragmentos como '/ cada'
        if linha_lower in NOMES_IGNORADOS:
            continue
        if re.fullmatch(r'[/\s]*(cada|un\.?|kg|g|lt?)[/\s]*', linha_lower):
            continue
        if len(linha) > 4 and "%" not in linha:
            candidatos_nome.append(linha)

    if not precos or not candidatos_nome:
        return None

    nome_encontrado = candidatos_nome[0]
    if "oferta" in nome_encontrado.lower() or "leve" in nome_encontrado.lower():
        if len(candidatos_nome) > 1:
            nome_encontrado = candidatos_nome[1]

    if len(precos) > 1:
        def _para_float(p):
            try:
                return float(re.sub(r"[^\d,.]", "", p).replace(",", "."))
            except:
                return 0.0
        v1, v2 = _para_float(precos[0]), _para_float(precos[1])
        preco_normal = precos[0] if v1 > v2 else precos[1]
        preco_oferta = precos[1] if v1 > v2 else precos[0]
    else:
        preco_normal = precos[0]
        preco_oferta = "—"

    if url_produto and config.get("ean_regex_url"):
        match_ean_url = re.search(config["ean_regex_url"], url_produto)
        if match_ean_url:
            ean_encontrado = match_ean_url.group(1)
            metodo_ean = "Nivel 1 (URL)"

    if not ean_encontrado:
        match_attr = re.search(r'data-(?:ean|sku|id)=["\'](\d{8,14})["\']', html_card)
        if match_attr:
            ean_encontrado = match_attr.group(1)
            metodo_ean = "Nivel 2 (Atributo Card)"

    return {
        "produto_encontrado": nome_encontrado,
        "preco_normal": preco_normal,
        "preco_oferta": preco_oferta,
        "url": url_produto,
        "ean": ean_encontrado,
        "metodo_ean": metodo_ean
    }


def raspar_concorrente(produto: str, chave: str, config: dict, page, context) -> list:
    loja = config["nome"]
    url_base = config["url_busca"].replace("{produto}", config["encoder"](produto))

    print(f"\n{Fore.CYAN}Varrendo catalogo de {loja}...{Style.RESET_ALL}")

    resultados = []

    try:
        page.goto(url_base, timeout=30000)
        page.wait_for_load_state("networkidle", timeout=10000)
    except PlaywrightTimeoutError:
        pass

    for _ in range(4):
        page.evaluate("window.scrollBy(0, 800);")
        page.wait_for_timeout(800)

    cards = page.locator(
        "xpath=//*[contains(text(), 'R$')]/ancestor::div[contains(@class, 'product') or contains(@class, 'item') or contains(@class, 'card')]"
        " | //*[contains(text(), 'R$')]/ancestor::li"
    )
    count = cards.count()
    if count == 0:
        cards = page.locator("xpath=//*[contains(text(), 'R$')]/..")
        count = cards.count()

    textos_vistos = set()
    urls_vistas = set()
    itens_para_analise_profunda = []

    for i in range(count):
        card_loc = cards.nth(i)
        texto = card_loc.inner_text()

        if not texto or texto in textos_vistos:
            continue
        if "R$" not in texto:
            continue
        textos_vistos.add(texto)

        html_card = card_loc.inner_html()
        url_produto = None

        # Cacador de links agressivo
        try:
            elemento_link = card_loc.locator("a[href]").first
            if elemento_link.count() > 0:
                href = elemento_link.get_attribute("href")
            else:
                match_href = re.search(r'href=["\']([^"\']+)["\']', html_card)
                href = match_href.group(1) if match_href else None

            if href and len(href) > 2 and "javascript" not in href:
                if href.startswith("/"):
                    parsed_url = urlparse(url_base)
                    url_produto = f"{parsed_url.scheme}://{parsed_url.netloc}{href}"
                elif "http" in href:
                    url_produto = href
        except Exception:
            pass

        if url_produto in urls_vistas and url_produto is not None:
            continue
        if url_produto:
            urls_vistas.add(url_produto)

        dados = extrair_dados_card(texto, html_card, url_produto, config)

        if dados:
            dados["supermercado"] = loja
            resultados.append(dados)

            # Entra na fila de busca profunda se nao tem EAN:
            # - com URL: faz busca na pagina do produto (niveis 3-5)
            # - sem URL (ex: Sao Luiz): busca diretamente por nome do produto
            if not dados["ean"]:
                itens_para_analise_profunda.append(dados)

    if itens_para_analise_profunda:
        com_url = sum(1 for i in itens_para_analise_profunda if i.get("url"))
        sem_url = len(itens_para_analise_profunda) - com_url
        msg = f"{com_url} com URL"
        if sem_url:
            msg += f", {sem_url} sem URL (busca por nome)"
        print(f"   {Fore.YELLOW}Iniciando busca profunda para {len(itens_para_analise_profunda)} produto(s) ({msg})...{Style.RESET_ALL}")

        for item in itens_para_analise_profunda:
            ean_encontrado, metodo = "—", "Falha"

            if item.get("url"):
                # Niveis 3, 4, 5: busca na pagina do produto
                ean_encontrado, metodo = buscar_ean_profundo(item["url"], context)

            if ean_encontrado == "—" or ean_encontrado is None:
                # Niveis 6A-6D e 7: busca por nome em bases reais + IA como ultimo recurso
                ean_encontrado, metodo = buscar_ean_por_nome(item["produto_encontrado"])

            item["ean"] = ean_encontrado
            item["metodo_ean"] = metodo

    if resultados:
        print(f"   {Fore.GREEN}Extracao concluida. {len(resultados)} item(ns) coletado(s).{Style.RESET_ALL}")
    else:
        print(f"   {Fore.YELLOW}Nenhum produto correspondente visivel na tela.{Style.RESET_ALL}")

    return resultados


# ==========================================
# INICIALIZACAO E CLI
# ==========================================
def executar_busca(produto: str):
    resultados_totais = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            for chave, config in CONCORRENTES.items():
                if " no " in produto.lower():
                    partes = produto.lower().split(" no ")
                    produto_limpo = partes[0].strip()
                    destino = partes[1].strip()
                    if "luiz" in destino:
                        concorrente_esp = "saoluiz"
                    elif "atacadao" in destino or "atacadão" in destino:
                        concorrente_esp = "atacadao"
                    elif "diniz" in destino:
                        concorrente_esp = "diniz"
                    else:
                        concorrente_esp = destino
                    if chave != concorrente_esp:
                        continue
                else:
                    produto_limpo = produto.strip()

                dados = raspar_concorrente(produto_limpo, chave, config, page, context)
                resultados_totais.extend(dados)
        finally:
            browser.close()

    return resultados_totais


def main():
    print(f"{Fore.YELLOW}=========================================={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Extrator de Precos e EAN - v3.1       {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Lojas: Diniz | Sao Luiz | Atacadao    {Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=========================================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}ℹ Info: Consumo de Tokens da OpenAI reduzido em 90%.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}IA acionada apenas como último recurso, exigindo sempre o EAN mais recente.{Style.RESET_ALL}\n")

    while True:
        print(f"\n{Fore.YELLOW}Catalogo para pesquisar (ou 0 para sair): {Style.RESET_ALL}", end="")
        entrada = input().strip()

        if not entrada:
            continue
        if entrada == "0":
            print(f"\n{Fore.CYAN}Encerrando. Ate logo.{Style.RESET_ALL}")
            break

        resultados = executar_busca(entrada)

        if resultados:
            colunas = ["Loja", "Produto Encontrado", "Preco Normal", "Oferta", "EAN", "Nivel de Extracao"]
            linhas = [
                [
                    r.get("supermercado", "—"),
                    (r.get("produto_encontrado", "—")[:45] + '...') if len(r.get("produto_encontrado", "—")) > 45 else r.get("produto_encontrado", "—"),
                    r.get("preco_normal", "—"),
                    r.get("preco_oferta", "—"),
                    r.get("ean", "—"),
                    r.get("metodo_ean", "—")
                ] for r in resultados
            ]
            print("\n" + tabulate(linhas, headers=colunas, tablefmt="rounded_outline"))

            print(f"\n{Fore.CYAN}Deseja exportar estes resultados para CSV? (s/n): {Style.RESET_ALL}", end="")
            exportar = input().strip().lower()
            if exportar == 's':
                exportar_para_csv(resultados)
        else:
            print(f"\n{Fore.RED}Nenhum resultado retornado para '{entrada}'.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()