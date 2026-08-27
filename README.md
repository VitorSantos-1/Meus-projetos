# Meus Projetos — Estudos e Experimentos em Dados

Repositório que reúne estudos, scripts e experimentos em Análise de Dados, Python, R e Machine
Learning, organizados por domínio. Funciona como um laboratório pessoal: da raspagem de dados e
análise estatística a modelos de Machine Learning e aplicações web, mostrando a amplitude técnica por
trás dos projetos de portfólio.

> **Nota de confidencialidade:** os dados presentes neste repositório são fictícios ou públicos,
> usados apenas para estudo e demonstração. Nenhum dado real, credencial ou informação de terceiros
> foi incluído aqui.

---

## Sobre este Repositório

Este repositório concentra o trabalho exploratório que sustenta os projetos mais acabados do
portfólio. A estrutura é organizada por domínio para facilitar a navegação — dos experimentos de
raspagem e estatística aos protótipos de Machine Learning e às aplicações.

## Estrutura do Projeto

| Pasta | Descrição |
|-------|-----------|
| `src/pesquisa_preco/` | Pesquisa de Preços — robô de web scraping (Selenium) que compara preços entre supermercados e gera relatórios. |
| `src/R_exemplos/` | Exercícios e trabalhos em R — estatística, manipulação e visualização de dados. |
| `scripts/python_geral/` | Scripts variados em Python, incluindo um analisador de sentimentos com Streamlit e BERT. |
| `data/` | Bases e artefatos usados nos projetos (CSVs, imagens, `.RData`). |
| `config/` | Configuração e dependências (`requirements`, `.env.example`). |
| `docs/` | Documentação auxiliar e anotações. |
| `reorganizar.py` | Utilitário que reorganiza a árvore do repositório com `git mv`. |

## Projetos em Destaque

### Pesquisa de Preços (`src/pesquisa_preco/`)
Robô que automatiza a comparação de preços entre supermercados concorrentes. Faz varredura de catálogo
com Selenium, trata os dados e apresenta os resultados de forma organizada no terminal.

```bash
pip install -r config/pesquisa_preco/reqs.txt
cp config/pesquisa_preco/.env.example .env
python src/pesquisa_preco/main.py
```

### Analisador de Sentimentos (`scripts/python_geral/`)
Aplicação web em Streamlit que classifica o sentimento de avaliações de clientes em português, usando
um modelo BERT da Hugging Face.

```bash
pip install streamlit transformers torch
streamlit run scripts/python_geral/sistema_avaliacao_cliente.py
```

### Análises em R (`src/R_exemplos/`)
Exercícios e trabalhos em R cobrindo estatística descritiva, manipulação e visualização de dados.

## Stack

Python - R - pandas - NumPy - scikit-learn - Matplotlib - seaborn - Plotly - Selenium -
BeautifulSoup - Hugging Face Transformers (BERT) - Streamlit - Git - Jupyter.

## Autor

José Vitor Santos Pinheiro — Análise de Dados e Inteligência Comercial (Varejo e Supply Chain).
Contato: vytorsantt@gmail.com
