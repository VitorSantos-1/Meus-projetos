<h1 align="center">🏠 Meus Projetos</h1>

<p align="center">
  <em>Meu lar de criatividade — um repositório com meus estudos e projetos em Análise de Dados, Python, R e Machine Learning.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=r&logoColor=white" alt="R"/>
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas"/>
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=flat-square&logo=selenium&logoColor=white" alt="Selenium"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black" alt="Hugging Face"/>
</p>

---

## 📖 Sobre este repositório

Este repositório reúne diversos projetos, scripts e exercícios que fui criando ao longo dos meus estudos — de raspagem de dados e análise estatística a modelos de Machine Learning e aplicações web. A estrutura foi organizada por **domínio** para facilitar a navegação.

---

## 🗂️ Estrutura do projeto

| Pasta | Descrição |
|-------|-----------|
| 📁 [`src/pesquisa_preco/`](src/pesquisa_preco/) | **Pesquisa de Preços** — robô de web scraping (Selenium) que compara preços de produtos entre supermercados e gera relatórios. |
| 📁 [`src/R_exemplos/`](src/R_exemplos/) | Exercícios e trabalhos em **R** — estatística, manipulação e visualização de dados. |
| 📁 [`scripts/python_geral/`](scripts/python_geral/) | Scripts variados em **Python**, incluindo um analisador de sentimentos com Streamlit + BERT. |
| 📁 [`data/`](data/) | Bases de dados e artefatos usados nos projetos (CSVs, imagens, `.RData`). |
| 📁 [`config/`](config/) | Arquivos de configuração e dependências (`requirements`, `.env.example`). |
| 📁 [`docs/`](docs/) | Documentação auxiliar e anotações. |
| 📁 `tests/` | Espaço reservado para testes automatizados. |
| 📄 [`reorganizar.py`](reorganizar.py) | Utilitário que reorganiza a árvore do repositório usando `git mv`. |

---

## 🚀 Projetos em destaque

### 🛒 Pesquisa de Preços (`src/pesquisa_preco/`)
Robô que automatiza a **comparação de preços** entre supermercados concorrentes. Faz varredura de catálogo com **Selenium**, trata os dados e apresenta os resultados de forma organizada no terminal (com `colorama` e `tabulate`).

```bash
# Instalar dependências
pip install -r config/pesquisa_preco/reqs.txt

# Configurar variáveis de ambiente (veja o exemplo)
cp config/pesquisa_preco/.env.example .env

# Executar
python src/pesquisa_preco/main.py
```

### 🎭 Analisador de Sentimentos (`scripts/python_geral/sistema_avaliacao_cliente.py`)
Aplicação web em **Streamlit** que classifica o sentimento de avaliações de clientes em português, usando um modelo **BERT** da Hugging Face.

```bash
pip install streamlit transformers torch
streamlit run scripts/python_geral/sistema_avaliacao_cliente.py
```

### 📊 Análises em R (`src/R_exemplos/`)
Coleção de exercícios e trabalhos acadêmicos em R, cobrindo estatística descritiva, manipulação e visualização de dados (incluindo uma análise de acidentes de trânsito de 2024).

---

## 🛠️ Tecnologias utilizadas

- **Linguagens:** Python, R
- **Dados & ML:** pandas, NumPy, scikit-learn, Matplotlib, Seaborn, Plotly
- **Web scraping:** Selenium, BeautifulSoup
- **NLP / IA:** Hugging Face Transformers (BERT)
- **Apps:** Streamlit
- **Ferramentas:** Git, Jupyter, n8n

---

## 👤 Autor

**Vitor Santos** · [@VitorSantos-1](https://github.com/VitorSantos-1)

<p align="center"><sub>✨ Feito com curiosidade e vontade de aprender.</sub></p>
