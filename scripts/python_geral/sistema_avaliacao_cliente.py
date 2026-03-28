import streamlit as st
from transformers import pipeline


# Configuração da página
st.set_page_config(page_title="Analisador de Sentimentos", page_icon="🎭")


# ----------------------------------------------------------------
# Função para carregar o modelo
# ----------------------------------------------------------------
@st.cache_resource
def carregar_modelo():
    """Carrega a pipeline de análise de sentimentos."""
    return pipeline(
        "sentiment-analysis",
        model="lipaoMai/BERT-sentiment-analysis-portuguese"
    )


# ----------------------------------------------------------------
# Interface do Usuário
# ----------------------------------------------------------------
st.title("🎭 Análise de Satisfação do Cliente")
st.markdown(
    "Insira o feedback do cliente abaixo para identificar o "
    "sentimento predominante."
)

# Carregamento do modelo com feedback visual
with st.spinner("Preparando o motor de IA..."):
    analisador_sentimento = carregar_modelo()

# Campo de entrada
placeholder_txt = "Ex: O suporte foi excelente e resolveu meu problema rápido!"
texto_do_usuario = st.text_area(
    "Por favor, avalie o atendimento:",
    placeholder=placeholder_txt
)
if st.button("Analisar Sentimento") and texto_do_usuario:
    # Execução da análise
    with st.spinner("Analisando..."):
        resultado = analisador_sentimento(texto_do_usuario)[0]
        label = resultado['label']
        score = resultado['score']

    # ----------------------------------------------------------------
    # Lógica de Exibição Corrigida
    # ----------------------------------------------------------------
    st.divider()

    # Mapeamento ajustado para modelos de 3 classes (padrão comum em PT)
    # LABEL_0 -> Negativo | LABEL_1 -> Neutro | LABEL_2 -> Positivo
    if "LABEL_2" in label or "Pos" in label:
        st.success("### Sentimento: Positivo 😄")
    elif "LABEL_0" in label or "Neg" in label:
        st.error("### Sentimento: Negativo 😟")
    else:
        # Captura LABEL_1 e outros como Neutro
        st.info("### Sentimento: Neutro 😐")

    # Exibe a confiança e o label técnico para você conferir
    st.write(f"**Confiança da IA:** {score:.2%} (ID: {label})")
    st.progress(score)
