import base64, pathlib
import streamlit as st

ASSETS = pathlib.Path(__file__).parent / "assets"

def _b64(name):
    return base64.b64encode((ASSETS / name).read_bytes()).decode()

def aplicar_estilo():
    bg = _b64("bg_xadrez.png")
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Comic+Neue:wght@400;700&display=swap');

    .stApp {{
        background: url("data:image/png;base64,{bg}") repeat;
        font-family: 'Comic Neue', 'Comic Sans MS', cursive;
    }}
    /* texto sempre legível */
    .stApp, .stApp p, .stApp label, .stApp span, .stApp li,
    .stApp h1, .stApp h2, .stApp h3, [data-testid="stMarkdownContainer"] {{
        color: #5a0f2e !important;
    }}
    h1, h2, h3 {{
        font-family: 'Pacifico', cursive !important;
        color: #d81b60 !important;
        text-shadow: 2px 2px 0 #ffd1e0;
    }}
    /* "janela" central estilo blog */
    .block-container {{
        max-width: 1000px;
        background: #fff5fa;
        border: 4px solid #7a0030;
        border-radius: 14px;
        box-shadow: 8px 8px 0 #c2185b;
        padding: 0 1.5rem 2rem 1.5rem !important;
        margin-top: 1.5rem;
    }}
    /* abas */
    button[data-baseweb="tab"] {{
        background: #ffc2d9; border: 2px solid #7a0030;
        border-radius: 10px 10px 0 0; margin-right: 6px;
        font-weight: 700;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{ background: #e91e63; }}
    button[data-baseweb="tab"][aria-selected="true"] p {{ color: #fff !important; }}
    /* campos */
    .stTextInput input, .stTextArea textarea, [data-baseweb="input"] input {{
        background: #fff !important; color: #5a0f2e !important;
        border: 2px dashed #e91e63 !important; border-radius: 8px;
    }}
    [data-baseweb="input"], [data-baseweb="textarea"] {{ background: #fff !important; }}
    [data-testid="stFileUploaderDropzone"] {{
        background: #ffe0ec !important; border: 3px dotted #c2185b !important;
        border-radius: 12px;
    }}
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] span {{ color: #7a0030 !important; }}
    [data-testid="stFileUploaderDropzone"] button {{
        background: #e91e63 !important; color: #fff !important; border: 2px solid #7a0030 !important;
    }}
    [data-testid="stFileUploaderDropzone"] button * {{ color: #fff !important; }}
    /* botão principal */
    .stButton > button, .stFormSubmitButton > button {{
        width: 100%;
        background: linear-gradient(#ff5c8d, #d81b60) !important;
        color: #fff !important; font-weight: 700; font-size: 1.1rem;
        border: 3px solid #7a0030 !important; border-radius: 12px;
        box-shadow: 4px 4px 0 #7a0030;
    }}
    .stButton > button:hover, .stFormSubmitButton > button:hover {{
        transform: translate(2px,2px); box-shadow: 2px 2px 0 #7a0030;
    }}
    .stButton > button *, .stFormSubmitButton > button * {{ color: #fff !important; }}
    /* barra do topo do Streamlit transparente */
    header[data-testid="stHeader"] {{ background: transparent; }}
    /* fotos da galeria estilo polaroid */
    [data-testid="stImage"] img {{
        background: #fff; padding: 8px 8px 22px 8px;
        border: 2px solid #7a0030; border-radius: 4px;
        box-shadow: 4px 4px 0 #e91e63;
    }}
    [data-testid="stCaptionContainer"] {{ color: #8a3a58 !important; }}
    hr {{ border-top: 3px dotted #e91e63 !important; }}
    [data-testid="stAlert"] {{ border-radius: 10px; border: 2px dashed #c2185b; }}
    /* abas (seletores do Streamlit atual) */
    .stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 3px solid #7a0030; }}
    .stTabs [data-baseweb="tab"] {{
        background: #ffc2d9 !important; border: 2px solid #7a0030; border-bottom: none;
        border-radius: 10px 10px 0 0; padding: 6px 14px; height: auto;
    }}
    .stTabs [data-baseweb="tab"] p {{ font-weight: 700; color: #7a0030 !important; }}
    .stTabs [aria-selected="true"] {{ background: #e91e63 !important; }}
    .stTabs [aria-selected="true"] p {{ color: #fff !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ background: transparent !important; }}
    .stTabs [data-baseweb="tab-border"] {{ background: transparent !important; }}
    /* campo de senha (olhinho) e placeholders legíveis */
    [data-baseweb="input"] > div, [data-baseweb="base-input"] {{ background: #fff !important; }}
    [data-baseweb="input"] button, [data-baseweb="input"] button svg {{
        background: #fff !important; color: #c2185b !important; fill: #c2185b !important;
    }}
    input::placeholder, textarea::placeholder {{ color: #b0527a !important; opacity: 1 !important; }}
    /* arquivo escolhido no uploader */
    [data-testid="stFileUploaderFile"] {{ background: #fff; border: 2px solid #c2185b; border-radius: 8px; padding: 2px 8px; }}
    [data-testid="stFileUploaderFile"] * {{ color: #5a0f2e !important; }}
    [data-testid="stFileUploaderFile"] button {{ background: transparent !important; border: none !important; box-shadow: none !important; }}
    [data-testid="stFileUploaderDropzone"] button[kind="secondary"] {{ width: auto; }}
    /* legendas pequenas mais legíveis */
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{ color: #8a2a52 !important; }}
    .rodape {{
        text-align:center; margin-top:2rem; padding-top:.6rem;
        border-top: 3px dotted #e91e63; font-size:.95rem;
    }}
    </style>
    """, unsafe_allow_html=True)

def banner():
    st.image(str(ASSETS / "banner.png"), use_container_width=True)

def rodape():
    st.markdown('<div class="rodape">✿ Feito pra aproveitar ao máximo o momento ✿</div>',
                unsafe_allow_html=True)
