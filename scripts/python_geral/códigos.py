import subprocess
import sys
import os
# A lista bruta que você enviou
raw_list = """
numpy pandas polars matplotlib seaborn plotly bokeh scikit-learn scipy statsmodels tensorflow torch torchvision torchaudio keras transformers xgboost lightgbm catboost nltk spacy gensim langchain opencv-python pillow scikit-image beautifulsoup4 requests scrapy selenium playwright sqlalchemy psycopg2-binary pyspark dask ray mlflow wandb streamlit dash fastapi uvicorn pydantic jupyterlab notebook ipython pyarrow python-dotenv openpyxl autogpt crewai agno boto3 urllib3 setuptools django flask guidance pandasai marvin mediapipe openai-whisper faiss-cpu huggingface_hub pytube langgraph poetry openai anthropic google-generativeai llama-index pyautogen phidata dspy-ai instructor litellm chromadb pinecone-client qdrant-client weaviate-client tiktoken diffusers datasets accelerate bitsandbytes peft sentence-transformers vllm gradio haystack-ai mem0ai celery redis pymongo docker ansible pytest rich tqdm typer loguru httpx optuna shap networkx numba cython joblib einops onnx onnxruntime gunicorn pre-commit cookiecutter jinja2 pydub sympy aiohttp websockets tenacity apache-airflow kafka-python pypdf pdfplumber pytesseract albumentations librosa moviepy imageio folium geopandas altair panel holoviews textblob thefuzz psutil schedule watchdog cryptography pyjwt bcrypt alembic peewee motor marshmallow s3fs google-cloud-storage azure-storage-blob bentoml click colorama lxml html5lib pytz python-dateutil arrow pika black flake8 mypy isort ujson"""
# Limpeza da lista
libraries = sorted(list(set(raw_list.split())))
installed = []
failed = []
print(f"--- Iniciando Instalação de {len(libraries)} Pacotes ---")
print(f"Versão do Python: {sys.version}")
for lib in libraries:
    print(f"[{len(installed) + len(failed) + 1}/{len(libraries)}] Instalando: {lib}...",
          end=" ", flush=True)
    try:
        # Tenta instalar. Timeout de 300s para pacotes grandes como tensorflow/torch
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", lib],
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode == 0:
            print("✅")
            installed.append(lib)
        else:
            print("❌")
            # Captura o stderr completo para um log mais detalhado
            failed.append((lib, result.stderr))
    except Exception as e:
        print("⚠️ Erro de execução")
        failed.append((lib, str(e)))
# Criar relatório de falhas
with open("falhas_instalacao.log", "w", encoding="utf-8") as f:
    f.write("RELATÓRIO DE FALHAS NA INSTALAÇÃO DE BIBLIOTECAS\n")
    f.write("="*60 + "\n")
    for lib, error in failed:
        f.write(f"--- Falha ao instalar: {lib} ---\n")
        f.write(error)
        f.write("\n" + "="*60 + "\n")
print("\n" + "="*40)
print("CONCLUÍDO!")
print(f"Sucessos: {len(installed)}")
print(f"Falhas: {len(failed)} (detalhes em 'falhas_instalacao.log')")
print("="*40)
