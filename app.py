import os
from pathlib import Path

import streamlit as st
from groq import Groq
from PIL import Image
from dotenv import load_dotenv


# ==========================================
# CONFIGURACAO
# ==========================================

PASTA_PROJETO = Path(__file__).parent

load_dotenv(PASTA_PROJETO / ".env")

st.set_page_config(
    page_title="VedRol - Assistente de Rolamentos",
    page_icon="⚙️",
    layout="wide"
)


# ==========================================
# ESTILO VISUAL VEDROL
# ==========================================

st.markdown("""
<style>
    :root {
        --vedrol-fundo: #171c22;
        --vedrol-painel: #222a33;
        --vedrol-dourado: #c5ad76;
        --vedrol-texto: #f0f2f5;
        --vedrol-borda: #46515e;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 50% 35%,
                #26394a 0%,
                #1b242d 48%,
                #171b20 100%
            );
        color: var(--vedrol-texto);
    }

    [data-testid="stHeader"] {
        background: rgba(23, 28, 34, 0.96);
        border-bottom: 1px solid #343d47;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    h1, h2, h3, p, label {
        color: var(--vedrol-texto);
    }

    h1 {
        font-size: clamp(1.8rem, 3vw, 2.8rem) !important;
        font-weight: 750 !important;
        letter-spacing: -0.8px;
    }

    [data-testid="stCaptionContainer"] {
        color: #c6ccd3;
    }

    [data-testid="stImage"] img {
        border-radius: 8px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(28, 35, 43, 0.88);
        border: 1px solid rgba(95, 111, 127, 0.25);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stChatInput"] {
        background: transparent;
    }

    [data-testid="stChatInput"] > div {
        background: #303943;
        border: 1px solid var(--vedrol-dourado);
        border-radius: 10px;
        box-shadow: 0 0 12px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stChatInput"] textarea {
        color: white !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #b9c0c9 !important;
    }

    [data-testid="stChatInput"] button {
        background: var(--vedrol-dourado) !important;
        color: #1b2026 !important;
        border-radius: 8px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #343e49, #28313b);
        color: #f4f5f7;
        border: 1px solid #485462;
        border-radius: 8px;
        min-height: 40px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: var(--vedrol-dourado);
        color: #ffffff;
        background: #3a4652;
    }

    hr {
        border-color: #46515e;
        opacity: 0.7;
    }

    [data-testid="stSpinner"] {
        color: var(--vedrol-dourado);
    }

    footer {
        visibility: hidden;
    }

    @media (max-width: 900px) {
        .block-container {
            padding: 1rem 0.8rem;
        }

        h1 {
            font-size: 1.8rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# CAMINHO DO LOGOTIPO
# ==========================================

CAMINHO_LOGO = PASTA_PROJETO / "assets" / "vedrol.jpg"


# ==========================================
# CABECALHO VEDROL
# ==========================================

cabecalho_logo, cabecalho_menu = st.columns(
    [2, 3],
    vertical_alignment="center"
)

with cabecalho_logo:
    if CAMINHO_LOGO.exists():
        try:
            with Image.open(CAMINHO_LOGO) as imagem:
                imagem.load()
                st.image(imagem.copy(), width=220)

        except Exception as erro:
            st.warning(f"Não foi possível abrir o logo: {erro}")
    else:
        st.markdown("## ⚙️ VedRol")


with cabecalho_menu:
    menu1, menu2, menu3, menu4, menu5 = st.columns(5)

    with menu1:
        st.button(
            "Início",
            key="menu_inicio",
            use_container_width=True
        )

    with menu2:
        st.button(
            "Produtos",
            key="menu_produtos",
            use_container_width=True
        )

    with menu3:
        st.button(
            "Técnico",
            key="menu_tecnico",
            use_container_width=True
        )

    with menu4:
        st.button(
            "Blog",
            key="menu_blog",
            use_container_width=True
        )

    with menu5:
        st.button(
            "Contato",
            key="menu_contato",
            use_container_width=True
        )

st.divider()


# ==========================================
# TITULO E ATALHOS
# ==========================================

col_titulo, col_atalhos = st.columns(
    [2.3, 1],
    gap="large",
    vertical_alignment="center"
)

with col_titulo:
    st.title("VedRol - Especialista em Rolamentos")

    st.markdown(
        "Assistente técnico para identificação de rolamentos, "
        "vedações e componentes de transmissão industrial."
    )

with col_atalhos:
    st.button(
        "▦  Consultar Catálogo",
        key="atalho_catalogo",
        use_container_width=True
    )

    st.button(
        "♧  Solicitar Orçamento",
        key="atalho_orcamento",
        use_container_width=True
    )

    st.button(
        "▤  Ver Manuais",
        key="atalho_manuais",
        use_container_width=True
    )

    st.button(
        "?  Perguntas Frequentes (FAQ)",
        key="atalho_faq",
        use_container_width=True
    )

st.divider()


# ==========================================
# CONEXAO COM A GROQ
# ==========================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "Chave da Groq não encontrada. Verifique o arquivo .env."
    )
    st.stop()

client = Groq(api_key=api_key)


# ==========================================
# INSTRUCOES DA INTELIGENCIA ARTIFICIAL
# ==========================================

INSTRUCOES = """
Você é o assistente técnico da VedRol, especializado em
rolamentos industriais, vedações e transmissão mecânica.

Seu objetivo é ajudar compradores, vendedores, mecânicos,
técnicos de manutenção e profissionais da indústria.

Responda sempre em português brasileiro.
Seja profissional, claro, didático e objetivo.

CONHECIMENTO SOBRE ROLAMENTOS

1. ROLAMENTOS DE ESFERAS
- Rígidos de esferas.
- Séries 6000, 6200, 6300 e outras.
- Contato angular.
- Autocompensadores de esferas.
- Axiais de esferas.
- Quatro pontos de contato.
- Miniatura e instrumentação.
- Alta precisão.
- Seção fina.
- Híbridos com elementos cerâmicos.
- Abertos, blindados e vedados.

2. ROLAMENTOS DE ROLOS CILÍNDRICOS
- Uma ou várias carreiras.
- Tipos NU, NJ, N, NUP e variantes.
- Aplicações com cargas radiais elevadas.
- Aplicações industriais e motores.

3. ROLAMENTOS DE ROLOS CÔNICOS
- Uma carreira.
- Duas carreiras.
- Quatro carreiras.
- Montados em pares.
- Aplicações automotivas e industriais.

4. AUTOCOMPENSADORES DE ROLOS
- Séries 22200, 22300, 23000, 23100 e outras.
- Versões abertas e vedadas.
- Aplicações com cargas elevadas.
- Equipamentos sujeitos a desalinhamento e vibração.
- Peneiras vibratórias.

5. ROLAMENTOS DE AGULHAS
- Com e sem anel interno.
- Gaiolas de agulhas.
- Buchas de agulhas.
- Axiais de agulhas.
- Conjuntos combinados.
- Séries HK, BK e outras famílias.

6. ROLAMENTOS AXIAIS
- De esferas.
- De rolos cilíndricos.
- De rolos cônicos.
- De rolos esféricos.
- De agulhas.
- De simples ou dupla direção.

7. ROLAMENTOS ESPECIAIS
- Alta temperatura.
- Resistentes à corrosão.
- Isolados eletricamente.
- Alta velocidade.
- Alta precisão.
- Híbridos ou cerâmicos.
- Grandes dimensões.
- Divididos.
- Para ambientes agressivos.
- Para aplicações industriais específicas.

8. MANCAIS E ACESSÓRIOS
- Mancais de pedestal.
- Mancais flangeados.
- Mancais tensores.
- Unidades de rolamentos montados.
- Mancais bipartidos.
- Buchas de fixação e desmontagem.
- Porcas e arruelas.
- Acessórios de montagem.

9. PRODUTOS RELACIONADOS
- Retentores.
- Vedações.
- Buchas.
- Graxas e lubrificantes.
- Sistemas de lubrificação.
- Componentes de transmissão mecânica.

IDENTIFICAÇÃO DE CÓDIGOS

Quando receber códigos como 6203, 6203-2RS, 6203-ZZ,
6305, 22210, NU205, 7205, 30205 ou HK1010:

- Identifique a família provável.
- Explique as características conhecidas.
- Interprete os sufixos quando houver segurança.
- Solicite fabricante ou medidas quando necessário.
- Não invente dimensões, cargas ou rotações.
- Não afirme que um código não existe sem confirmação.

Alguns significados frequentes:
- 2RS: geralmente vedações nos dois lados.
- ZZ ou 2Z: geralmente blindagens metálicas nos dois lados.
- C3 e C4: classes de folga interna em diversas séries.
- P5 e P6: classes de precisão em nomenclaturas comuns.
- NU, NJ, N e NUP: designações de famílias de rolos cilíndricos.
- HK e BK: designações encontradas em famílias de agulhas.

A nomenclatura varia por fabricante e família.
Confirme a interpretação no catálogo técnico correspondente.

APLICAÇÕES INDUSTRIAIS

Considere:
- Motores elétricos e geradores.
- Bombas e compressores.
- Ventiladores e exaustores.
- Redutores e caixas de transmissão.
- Esteiras transportadoras.
- Máquinas agrícolas.
- Máquinas CNC.
- Mineração e britagem.
- Siderurgia e cimenteiras.
- Indústria alimentícia.
- Máquinas têxteis.
- Equipamentos de construção.
- Peneiras vibratórias.
- Aplicações automotivas.
- Sistemas de movimentação de materiais.

ORIENTAÇÃO TÉCNICA

Ao ajudar a selecionar um rolamento, considere:
- Cargas radiais e axiais.
- Velocidade de rotação.
- Temperatura.
- Vibração e choques.
- Desalinhamento.
- Contaminação.
- Lubrificação.
- Espaço disponível.
- Precisão.
- Montagem e manutenção.
- Vida útil esperada.

Faça perguntas quando faltarem dados importantes.
Não recomende um componente para aplicações críticas
sem dados suficientes e validação técnica.

REGRAS COMERCIAIS DA VEDROL

Você não recebeu automaticamente o catálogo comercial
da VedRol.

Portanto:
- Não invente preços ou estoque.
- Não invente prazos de entrega.
- Não afirme quais marcas a empresa comercializa sem confirmação.
- Diferencie conhecimento geral de dados comerciais.
- Oriente o cliente a confirmar informações comerciais
  com a equipe da VedRol.

FORMATO DAS RESPOSTAS

Quando adequado, informe:
- Família do rolamento.
- Identificação provável.
- Características.
- Aplicações comuns.
- Informações que precisam ser confirmadas.

Se não souber, explique a limitação e peça o código completo,
fabricante, medidas ou uma fotografia do produto.
"""


# ==========================================
# HISTORICO DA CONVERSA
# ==========================================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


# ==========================================
# AREA DO CHAT
# ==========================================

col_chat, col_limpar = st.columns(
    [5, 1],
    vertical_alignment="center"
)

with col_chat:
    st.markdown("### ⚙️ Assistente técnico")

with col_limpar:
    if st.button(
        "Limpar conversa",
        key="limpar_conversa",
        use_container_width=True
    ):
        st.session_state.mensagens = []
        st.rerun()


# Exibe as mensagens anteriores
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])


# ==========================================
# ENTRADA DO USUARIO
# ==========================================

pergunta = st.chat_input(
    "Digite um código ou pergunte sobre rolamentos..."
)

if pergunta:

    st.session_state.mensagens.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):

        with st.spinner("Consultando o assistente técnico..."):

            try:
                mensagens_api = [
                    {
                        "role": "system",
                        "content": INSTRUCOES
                    }
                ]

                # Mantém as últimas mensagens para dar contexto
                mensagens_api.extend(
                    st.session_state.mensagens[-12:]
                )

                resposta = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=mensagens_api,
                    temperature=0.2,
                    max_completion_tokens=1500
                )

                texto_resposta = (
                    resposta.choices[0].message.content
                    or "Não foi possível gerar uma resposta."
                )

                st.markdown(texto_resposta)

                st.session_state.mensagens.append({
                    "role": "assistant",
                    "content": texto_resposta
                })

            except Exception as erro:
                st.error(
                    f"Erro ao comunicar com a API da Groq: {erro}"
                )


# ==========================================
# RODAPE
# ==========================================

st.divider()

rodape1, rodape2 = st.columns(2)

with rodape1:
    st.caption(
        "Início  |  Produtos  |  Técnico  |  Blog  |  Contato"
    )

with rodape2:
    st.caption(
        "© 2026 VedRol. Todos os direitos reservados."
    )
