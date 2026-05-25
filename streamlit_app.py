import streamlit as st
import pandas as pd
import altair as alt
import snowflake.connector

st.set_page_config(page_title="Dashboard de Vendas - Mirai", layout="wide", initial_sidebar_state="expanded")

DEPT_MAP = {
    'Pamela Antunes': 'Inside Sales', 'Debora Paes': 'Inside Sales',
    'Katia Santana': 'Inside Sales', 'Gabrielly Simoes': 'Inside Sales',
    'Brenda Assis': 'Inside Sales', 'Kamylly Sgarbi': 'Inside Sales',
    'Maria Alcantara': 'Inside Sales', 'Jacqueline Helen': 'Inside Sales',
    'Richard William': 'Inside Sales', 'Natália Martins': 'Inside Sales',
    'Richard Trindade': 'Inside Sales', 'Pablo Gonçalves': 'Inside Sales',
    'Tabata Godoi': 'Inside Sales', 'Vania Ferreira': 'Inside Sales',
    'Bianca Moreira': 'Inside Sales',
    'Carlos Henrique': 'Gestão Adriana', 'Adriana da Silva': 'Gestão Adriana',
    'Fernando Doria': 'Gestão Adriana', 'Fabio Gonçalves': 'Gestão Adriana',
    'Gilberto Ferreira': 'Gestão Adriana', 'Joselaine Riberio': 'Gestão Adriana',
    'Roger Moraes': 'Gestão Adriana', 'Joyce': 'Gestão Adriana',
    'Marcela HM': 'Gestão Adriana', 'Marcilio Chaves Brasileiro': 'Gestão Adriana',
    'Camila Ribeiro': 'Gestão Adriana', 'Vagner Previdi': 'Gestão Adriana',
    'Leonardo Lafiandra': 'Gestão Adriana', 'Patricia Maciel': 'Gestão Adriana',
    'Tatiana Oliveira': 'Gestão Adriana', 'Felipe Policarpo': 'Gestão Adriana',
    'Fabricio Lima': 'Gestão Adriana', 'Ludmilla Gregorio': 'Gestão Adriana',
    'ROBSON Costa': 'Gestão Adriana', 'NEOVALE TELEFONIA': 'Gestão Adriana',
    'MARIA ELENICE SANTOS PALLONE': 'Gestão Adriana', 'Andre Yocida': 'Gestão Adriana',
    'GUSTAVO EKLUND': 'Gestão Adriana', 'Rosmar Gomes': 'Gestão Adriana',
    'FABIO BRANCO MENDES Fama': 'Gestão Adriana',
    'Giovanny Barbosa': 'Gestão de Parceiros Giovany',
    'Ana Paula Silva': 'Gestão de Parceiros Giovany',
    'Isabela Mundo 2': 'Gestão de Parceiros Giovany',
    'Stefanie Miranda': 'Gestão de Parceiros Giovany',
    'Mario Pini': 'Gestão de Parceiros Giovany',
    'Renato Campos': 'Gestão de Parceiros Giovany',
    'Eliane Santiago': 'Gestão de Parceiros Giovany',
    'Rinaldo Rodrigues': 'Gestão de Parceiros Giovany',
    'Felipe Silva': 'Gestão de Parceiros Giovany',
    'DOUGLAS TEISEN': 'Gestão de Parceiros Giovany',
    'Julio Galvão': 'Gestão de Parceiros Giovany',
    'Messias Marcondes': 'Gestão de Parceiros Giovany',
    'Rodrigo Morello': 'Gestão de Parceiros Giovany',
    'Afonso Reuter Filho': 'Gestão de Parceiros Giovany',
    'Haiza Santos': 'Gestão de Parceiros Giovany',
    'Eduardo Francisco Guimarães': 'Gestão de Parceiros Giovany',
    'Jessica Neves': 'Time Jéssica', 'Milena Mohallem do Prado': 'Time Jéssica',
    'Kelli Bressan': 'Time Jéssica', 'Leandro Cremonese': 'Time Jéssica',
    'Michelle Soares': 'Time Jéssica', 'Guilherme Trovo': 'Time Jéssica',
    'DARIO DE OLIVEIRA': 'Time Jéssica', 'ANA CAROLINE CONTEL': 'Time Jéssica',
    'Adriana Campos': 'Time Jéssica', 'Paulo Felix': 'Time Jéssica',
    'Marcelo Ferreira': 'Time Jéssica', 'Danilo Soares': 'Time Jéssica',
    'Eliana Barbosa': 'Time Jéssica', 'Paulo Roberto': 'Time Jéssica',
    'Elias Polinario': 'Time Jéssica', 'maria cristina duarte': 'Time Jéssica',
    'Beto Prado': 'Gerência Beto', 'RONALD MARTINS': 'Gerência Beto',
    'Thiago Calister': 'Gerência Beto', 'Jefferson Lucena': 'Gerência Beto',
    'Luiz Fernando Castro Figueiredo': 'Gerência Beto',
    'Gustavo Oliveira': 'Gerência Beto', 'Gabriel Prado': 'Gerência Beto',
    'Giane Dantas': 'Gerência Beto',
    'Pedro Arantes': 'Time Pedro Tech',
    'Pedro Henrique': 'Time Pedro de Paula', 'ANTONIO DURLIN': 'Time Pedro de Paula',
    'Luan Alves': 'Time Luan', 'Gisleine Palmeiras': 'Time Luan',
    'Adriana Santana': 'Time Luan', 'Adriana Pereira': 'Time Luan',
    'Rodrigo Farias': 'Time Xiscatti', 'Thamer Camelo': 'Time Xiscatti',
    'Fernando Xiscatti': 'Time Xiscatti', 'Xiscatti Liberty Consulting': 'Time Xiscatti',
    'Raquel Macedo': 'Calister', 'Luciene de Oliveira Ferreira': 'Calister',
    'Deisy Ponte': 'Calister',
    'Luis Lopes': 'Time de Tramitação', 'Stela Maira': 'Time de Tramitação',
    'Beatriz Lima': 'Time de Tramitação', 'Bruna Salatiel': 'Time de Tramitação',
    'Evelin Araújo': 'Time de Tramitação', 'Ivete Lemos': 'Time de Tramitação',
}

P = '#7B2FF7'
P2 = '#9D4EDD'
PA = '#5A189A'
BG = '#0f0a1a'
CARD_BG = 'rgba(20, 14, 40, 0.85)'
CARD_BORDER = 'rgba(123, 47, 247, 0.25)'
TEXT = '#e8e0f7'
TEXT_DIM = '#a89cc8'

BG_IMAGE_URL = "https://raw.githubusercontent.com/juanvtr/st_mirai/main/mir.png"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {{
        background: linear-gradient(180deg, #0f0a1a 0%, #0a0620 50%, #12052b 100%);
        font-family: 'Inter', sans-serif;
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('{BG_IMAGE_URL}') center/cover no-repeat;
        opacity: 0.08;
        pointer-events: none;
        z-index: 0;
    }}
    .main .block-container {{ position: relative; z-index: 1; }}

    .metric-card {{
        background: {CARD_BG};
        backdrop-filter: blur(12px);
        border: 1px solid {CARD_BORDER};
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        margin-bottom: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        border-color: {P};
        box-shadow: 0 8px 32px rgba(123, 47, 247, 0.2), 0 0 16px rgba(123, 47, 247, 0.1);
    }}
    .metric-card-accent {{
        background: linear-gradient(135deg, rgba(123,47,247,0.15), rgba(157,78,221,0.1));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(123, 47, 247, 0.4);
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        margin-bottom: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .metric-card-accent:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(123, 47, 247, 0.3), 0 0 20px rgba(157, 78, 221, 0.15);
    }}
    .card-title {{ color: {TEXT_DIM}; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}
    .card-value {{ color: #ffffff; font-size: 24px; font-weight: 700; margin: 8px 0 4px; }}
    .card-sub {{ color: {P2}; font-size: 11px; font-weight: 500; }}
    .card-indicator {{ font-size: 13px; font-weight: 600; margin-top: 4px; }}
    .indicator-up {{ color: #4CAF50; }}
    .indicator-down {{ color: #ef5350; }}
    .indicator-neutral {{ color: {TEXT_DIM}; }}

    h1, h2, h3, h4 {{ color: #ffffff !important; font-family: 'Inter', sans-serif !important; }}
    p, span, div {{ color: {TEXT}; }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0a0518 0%, #0f0825 100%) !important;
        border-right: 1px solid {CARD_BORDER};
    }}
    section[data-testid="stSidebar"] .stMarkdown {{ color: {TEXT} !important; }}

    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(10, 5, 24, 0.95);
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
        border: 1px solid {CARD_BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {TEXT_DIM} !important;
        border-radius: 8px;
        font-weight: 500;
        font-size: 13px;
    }}
    .stTabs [aria-selected="true"] {{
        color: white !important;
        background: linear-gradient(135deg, {P}, {P2}) !important;
        border-radius: 8px;
    }}

    .stSelectbox > div > div, .stMultiSelect > div > div {{
        background-color: rgba(20, 14, 40, 0.9) !important;
        border: 1px solid {CARD_BORDER} !important;
        border-radius: 10px !important;
        color: {TEXT} !important;
    }}
    .stSelectbox label, .stMultiSelect label {{
        color: {TEXT_DIM} !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}
    .stMultiSelect span[data-baseweb="tag"] {{
        background-color: {P} !important;
        color: white !important;
        border-radius: 6px !important;
    }}

    .stDataFrame {{ border-radius: 12px; overflow: hidden; }}
    .stMarkdown hr {{ border-color: rgba(123, 47, 247, 0.15) !important; }}
    .stTextInput > div > div {{ background-color: rgba(20, 14, 40, 0.9) !important; border: 1px solid {CARD_BORDER} !important; border-radius: 10px !important; color: white !important; }}
    .stTextInput label {{ color: {TEXT_DIM} !important; }}
</style>
""", unsafe_allow_html=True)

def get_connection():
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
    )

@st.cache_data(ttl=300)
def load_data():
    conn = get_connection()
    df = conn.cursor().execute("SELECT * FROM MIRAI.PUBLIC.RELATORIO_HISTORICO").fetch_pandas_all()
    conn.close()
    df['DEPARTAMENTO'] = df['RESPONSAVEL'].map(DEPT_MAP).fillna('Outros')
    df['VALOR_PRODUTO'] = pd.to_numeric(df['VALOR_PRODUTO'], errors='coerce').fillna(0)
    df['LINHAS'] = pd.to_numeric(df['LINHAS'], errors='coerce').fillna(0)
    df['MES'] = pd.to_datetime(df['CONCLUSAO_VIVO'], format='%d/%m/%Y', errors='coerce').dt.to_period('M').astype(str)
    df['DATA_CARGA'] = pd.to_datetime(df['DATA_CARGA']).dt.date
    return df

@st.cache_data(ttl=300)
def load_metas():
    conn = get_connection()
    try:
        df = conn.cursor().execute("SELECT * FROM MIRAI.PUBLIC.METAS_DEPARTAMENTO").fetch_pandas_all()
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df

@st.cache_data(ttl=300)
def load_tramitando():
    conn = get_connection()
    df = conn.cursor().execute("SELECT * FROM MIRAI.PUBLIC.TRAMITANDO").fetch_pandas_all()
    conn.close()
    df['VALOR_PRODUTO'] = pd.to_numeric(df['VALOR_PRODUTO'], errors='coerce').fillna(0)
    df['LINHAS'] = pd.to_numeric(df['LINHAS'], errors='coerce').fillna(0)
    df['DEPARTAMENTO'] = df['RESPONSAVEL'].map(DEPT_MAP).fillna('Outros')
    return df

@st.cache_data(ttl=300)
def load_produtos():
    conn = get_connection()
    df = conn.cursor().execute("SELECT DISTINCT NOME_COMERCIAL, VALOR_10X, VALOR_24X, FABRICANTE, GAMA FROM MIRAI.PUBLIC.PRODUTOS_VIVO WHERE TIPO_MATERIAL = 'Aparelho'").fetch_pandas_all()
    conn.close()
    return df

df = load_data()
df_metas = load_metas()
df_tram_raw = load_tramitando()
df_produtos = load_produtos()
has_metas = len(df_metas) > 0

def card(title, value, sub="", accent=False, indicator=None):
    cls = "metric-card-accent" if accent else "metric-card"
    ind_html = ""
    if indicator == "up":
        ind_html = '<div class="card-indicator indicator-up">&#9650; crescendo</div>'
    elif indicator == "down":
        ind_html = '<div class="card-indicator indicator-down">&#9660; caindo</div>'
    elif indicator == "neutral":
        ind_html = '<div class="card-indicator indicator-neutral">&#9654; estável</div>'
    return f'<div class="{cls}"><div class="card-title">{title}</div><div class="card-value">{value}</div><div class="card-sub">{sub}</div>{ind_html}</div>'

def count_linhas(dataframe):
    if len(dataframe) == 0:
        return 0
    return int(dataframe.groupby('NOME_NEGOCIO')['LINHAS'].max().clip(lower=1).sum())

with st.sidebar:
    st.markdown(f'<div style="text-align:center;padding:14px 0 18px;"><h2 style="margin:0;background:linear-gradient(135deg,{P},{P2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:20px;">Mirai Telecom</h2><p style="color:{TEXT_DIM};font-size:11px;margin:4px 0 0;">Parceira Vivo Empresas</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    cargas = sorted(df['DATA_CARGA'].dropna().unique(), reverse=True)
    carga_labels = [str(c) for c in cargas]
    carga_sel = st.selectbox("Snapshot", carga_labels, index=0)
    meses = sorted(df['MES'].dropna().unique(), reverse=True)
    mes_sel = st.selectbox("Mês", ["Todos"] + list(meses))
    depts = sorted(df['DEPARTAMENTO'].unique())
    dept_sel = st.multiselect("Departamento", depts, default=[], placeholder="Todos os departamentos")
    torres = sorted(set(df['TORRE'].unique()) | set(df_tram_raw['TORRE'].dropna().unique()))
    torre_sel = st.multiselect("Torre", torres, default=[], placeholder="Todas as torres")
    tipos = ['MIGRAÇÃO', 'NOVO']
    tipo_sel = st.multiselect("Tipo de Venda", tipos, default=[], placeholder="Todos os tipos")
    st.markdown(f'<p style="color:{TEXT_DIM};font-size:10px;margin-top:8px;">Selecione para filtrar. Vazio = todos.</p>', unsafe_allow_html=True)

df_f = df[df['DATA_CARGA'] == pd.to_datetime(carga_sel).date()].copy()
if mes_sel != "Todos":
    df_f = df_f[df_f['MES'] == mes_sel]
if dept_sel:
    df_f = df_f[df_f['DEPARTAMENTO'].isin(dept_sel)]
if torre_sel:
    df_f = df_f[df_f['TORRE'].isin(torre_sel)]
if tipo_sel:
    df_f = df_f[df_f['TIPO_VENDA'].isin(tipo_sel)]

df_tram = df_tram_raw.copy()
if dept_sel:
    df_tram = df_tram[df_tram['DEPARTAMENTO'].isin(dept_sel)]
if torre_sel:
    df_tram = df_tram[df_tram['TORRE'].isin(torre_sel)]
if tipo_sel:
    df_tram = df_tram[df_tram['TIPO_VENDA'].isin(tipo_sel)]

total_novo = df_f[df_f['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()
total_geral = df_f['VALOR_PRODUTO'].sum()
taxa_novo = (total_novo / total_geral * 100) if total_geral > 0 else 0

tram_novo = df_tram[df_tram['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()
tram_total_val = df_tram['VALOR_PRODUTO'].sum()
taxa_novo_tram = (tram_novo / tram_total_val * 100) if tram_total_val > 0 else 0
taxa_novo_combinada = ((total_novo + tram_novo) / (total_geral + tram_total_val) * 100) if (total_geral + tram_total_val) > 0 else 0

if taxa_novo >= 50:
    novo_indicator = "up"
elif taxa_novo >= 30:
    novo_indicator = "neutral"
else:
    novo_indicator = "down"

tab1, tab2, tab5, tab6, tab3, tab4, tab7 = st.tabs(["Visão Geral", "Produtos", "Metas", "Tramitando", "Buscar Pedido", "Dados", "Sobre"])

with tab1:
    st.markdown("## Visão Geral")
    total = df_f['VALOR_PRODUTO'].sum()
    mig = df_f[df_f['TIPO_VENDA'] == 'MIGRAÇÃO']['VALOR_PRODUTO'].sum()
    novo = df_f[df_f['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(card("Total Geral", f"R${total:,.2f}", f"{count_linhas(df_f)} linhas"), unsafe_allow_html=True)
    with c2:
        st.markdown(card("Migração", f"R${mig:,.2f}", f"{count_linhas(df_f[df_f['TIPO_VENDA']=='MIGRAÇÃO'])} linhas"), unsafe_allow_html=True)
    with c3:
        st.markdown(card("Novo", f"R${novo:,.2f}", f"{count_linhas(df_f[df_f['TIPO_VENDA']=='NOVO'])} linhas", accent=True), unsafe_allow_html=True)
    with c4:
        st.markdown(card("Taxa de Novo", f"{taxa_novo:.1f}%", f"Meta: >50%", accent=True, indicator=novo_indicator), unsafe_allow_html=True)

    for torre_nome in sorted(df_f['TORRE'].unique()):
        torre_data = df_f[df_f['TORRE'] == torre_nome]
        t_mig = torre_data[torre_data['TIPO_VENDA'] == 'MIGRAÇÃO']['VALOR_PRODUTO'].sum()
        t_nov = torre_data[torre_data['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()
        t_mig_linhas = count_linhas(torre_data[torre_data['TIPO_VENDA'] == 'MIGRAÇÃO'])
        t_nov_linhas = count_linhas(torre_data[torre_data['TIPO_VENDA'] == 'NOVO'])
        if t_mig + t_nov == 0:
            continue
        st.markdown(f"#### {torre_nome}")
        ct1, ct2, ct3 = st.columns(3)
        with ct1: st.markdown(card(f"{torre_nome} Total", f"R${t_mig+t_nov:,.2f}", f"{t_mig_linhas+t_nov_linhas} linhas"), unsafe_allow_html=True)
        with ct2: st.markdown(card(f"Mig. {torre_nome}", f"R${t_mig:,.2f}", f"{t_mig_linhas} linhas"), unsafe_allow_html=True)
        with ct3: st.markdown(card(f"Novo {torre_nome}", f"R${t_nov:,.2f}", f"{t_nov_linhas} linhas", accent=True), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📱 Aparelhos")
    aparelhos_kw = ['IPHONE', 'SMARTPHONE', 'GALAXY', 'MOTOROLA', 'SAMSUNG', 'XIAOMI', 'REDMI', 'TABLET', 'RELÓGIO', 'WATCH', 'ROTEADOR']
    df_aparelhos = df_f[df_f['PRODUTO'].str.upper().apply(lambda x: any(kw in x for kw in aparelhos_kw))]
    aparelhos_qtd = len(df_aparelhos)
    if aparelhos_qtd > 0:
        df_aparelhos = df_aparelhos.copy()
        df_aparelhos['PRODUTO_UPPER'] = df_aparelhos['PRODUTO'].str.upper().str.strip()
        df_preco = df_produtos[['NOME_COMERCIAL', 'VALOR_10X']].drop_duplicates(subset='NOME_COMERCIAL')
        df_preco['PRODUTO_UPPER'] = df_preco['NOME_COMERCIAL'].str.upper().str.strip()
        df_preco['PRECO'] = pd.to_numeric(df_preco['VALOR_10X'], errors='coerce').fillna(0)
        df_aparelhos = df_aparelhos.merge(df_preco[['PRODUTO_UPPER', 'PRECO']], on='PRODUTO_UPPER', how='left')
        df_aparelhos['PRECO'] = df_aparelhos['PRECO'].fillna(0)
        aparelhos_valor = df_aparelhos['PRECO'].sum()
        ca1, ca2, ca3 = st.columns(3)
        with ca1: st.markdown(card("Valor Aparelhos (10x)", f"R${aparelhos_valor:,.2f}", f"{aparelhos_qtd} unidades"), unsafe_allow_html=True)
        with ca2:
            aparelhos_top = df_aparelhos['PRODUTO'].value_counts().head(3)
            top_str = " | ".join([f"{p.split('(')[0].strip()}: {c}" for p, c in aparelhos_top.items()])
            st.markdown(card("Top Aparelhos", f"{aparelhos_qtd} un.", top_str), unsafe_allow_html=True)
        with ca3:
            sem_preco = df_aparelhos[df_aparelhos['PRECO'] == 0]
            if len(sem_preco) > 0:
                st.markdown(card("⚠ Sem preço tabela", f"{len(sem_preco)} un.", "Verificar cadastro"), unsafe_allow_html=True)
            else:
                st.markdown(card("✓ Todos com preço", f"{aparelhos_qtd} un.", "Tabela Vivo Tech"), unsafe_allow_html=True)
    else:
        st.info("Nenhum aparelho encontrado neste filtro.")

    st.markdown("---")
    st.markdown("#### Ranking por Departamento")
    dept_resumo = df_f.groupby('DEPARTAMENTO')['VALOR_PRODUTO'].sum().sort_values(ascending=False).reset_index()
    for _, row in dept_resumo.iterrows():
        pct = (row['VALOR_PRODUTO']/total*100) if total > 0 else 0
        bar_width = min(pct * 2, 100)
        st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid rgba(123,47,247,0.1);"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;"><span style="color:#fff;font-size:13px;font-weight:500;">{row["DEPARTAMENTO"]}</span><span style="color:{P};font-weight:700;font-size:13px;">R${row["VALOR_PRODUTO"]:,.2f} <span style="color:{TEXT_DIM};font-size:11px;">({pct:.1f}%)</span></span></div><div style="background:rgba(123,47,247,0.1);border-radius:4px;height:6px;"><div style="background:linear-gradient(90deg,{P},{P2});border-radius:4px;height:6px;width:{bar_width}%;transition:width 0.5s;"></div></div></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("## Produtos Mais Vendidos")
    torre_prod = st.selectbox("Filtrar por Torre", ["Todas"] + list(torres), key="torre_prod")
    df_prod = df_f if torre_prod == "Todas" else df_f[df_f['TORRE'] == torre_prod]
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### Top Produtos - Migração")
        for i, (prod, row) in enumerate(df_prod[df_prod['TIPO_VENDA'] == 'MIGRAÇÃO'].groupby('PRODUTO').agg(VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')).sort_values('VALOR', ascending=False).head(15).iterrows(), 1):
            st.markdown(f'<div style="display:flex;align-items:center;padding:10px 0;border-bottom:1px solid rgba(123,47,247,0.1);"><div style="color:{P};font-weight:700;width:28px;font-size:14px;">{i}</div><div style="flex:1;color:{TEXT};font-size:12px;">{prod}</div><div style="color:{TEXT_DIM};font-size:11px;margin-right:14px;">{int(row["QTD"])}x</div><div style="color:{P};font-weight:700;font-size:13px;">R${row["VALOR"]:,.2f}</div></div>', unsafe_allow_html=True)
    with col_p2:
        st.markdown("#### Top Produtos - Novo")
        for i, (prod, row) in enumerate(df_prod[df_prod['TIPO_VENDA'] == 'NOVO'].groupby('PRODUTO').agg(VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')).sort_values('VALOR', ascending=False).head(15).iterrows(), 1):
            st.markdown(f'<div style="display:flex;align-items:center;padding:10px 0;border-bottom:1px solid rgba(123,47,247,0.1);"><div style="color:{P2};font-weight:700;width:28px;font-size:14px;">{i}</div><div style="flex:1;color:{TEXT};font-size:12px;">{prod}</div><div style="color:{TEXT_DIM};font-size:11px;margin-right:14px;">{int(row["QTD"])}x</div><div style="color:{P2};font-weight:700;font-size:13px;">R${row["VALOR"]:,.2f}</div></div>', unsafe_allow_html=True)

with tab5:
    st.markdown("## Metas vs Realizado")
    if not has_metas:
        st.warning("Tabela METAS_DEPARTAMENTO não encontrada. Cadastre as metas para ver o progresso.")
    else:
        realizado_list = []
        for dept, grp in df_f.groupby('DEPARTAMENTO'):
            aparelhos = grp[grp['PRODUTO'].str.upper().str.contains('IPHONE|SMARTPHONE', na=False)]
            realizado_list.append({'DEPARTAMENTO': dept, 'REAL_MIG_MOVEL': grp[(grp['TORRE'] == 'Móvel') & (grp['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum(), 'REAL_MIG_FIXA': grp[(grp['TORRE'] == 'Fixa PJ') & (grp['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum(), 'REAL_NOVO': grp[grp['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum(), 'REAL_MIG': grp[grp['TIPO_VENDA'] == 'MIGRAÇÃO']['VALOR_PRODUTO'].sum(), 'REAL_TOTAL': grp['VALOR_PRODUTO'].sum(), 'REAL_MIG_MOVEL_QTD': count_linhas(grp[(grp['TORRE'] == 'Móvel') & (grp['TIPO_VENDA'] == 'MIGRAÇÃO')]), 'REAL_MIG_FIXA_QTD': count_linhas(grp[(grp['TORRE'] == 'Fixa PJ') & (grp['TIPO_VENDA'] == 'MIGRAÇÃO')]), 'REAL_APARELHOS_QTD': count_linhas(aparelhos) if len(aparelhos) > 0 else 0})
        realizado = pd.DataFrame(realizado_list)
        merged = df_metas.merge(realizado, on='DEPARTAMENTO', how='left').fillna(0)
        def pct_bar(real, meta, label_r, label_m):
            pct = (real / meta * 100) if meta > 0 else 0
            if pct >= 100: color = '#4CAF50'
            elif pct >= 75: color = P
            elif pct >= 50: color = P2
            elif pct >= 25: color = '#C77DFF'
            else: color = '#E0AAFF'
            width = min(pct, 100)
            return f'<div style="margin:4px 0;"><div style="display:flex;justify-content:space-between;font-size:11px;color:{TEXT_DIM};"><span>{label_r}: <b style="color:#fff">R${real:,.2f}</b></span><span>Meta: <b>R${meta:,.2f}</b></span></div><div style="background:rgba(123,47,247,0.15);border-radius:6px;height:14px;margin:3px 0;"><div style="background:{color};border-radius:6px;height:14px;width:{width}%;min-width:2px;"></div></div><div style="text-align:right;font-size:10px;color:{color};font-weight:bold;">{pct:.1f}%</div></div>'
        for _, row in merged.iterrows():
            dept = row['DEPARTAMENTO']; meta_novo = float(row['META_NOVO_TOTAL']); meta_mig = float(row['META_MIGRACAO_TOTAL'])
            real_novo = float(row['REAL_NOVO']); real_mig = float(row['REAL_MIG']); meta_total = meta_novo + meta_mig; real_total = float(row['REAL_TOTAL'])
            pct_total = (real_total / meta_total * 100) if meta_total > 0 else 0
            badge_color = '#4CAF50' if pct_total >= 100 else P if pct_total >= 50 else P2
            st.markdown(f'<div style="background:{CARD_BG};border:1px solid {CARD_BORDER};border-radius:14px;padding:18px;margin:12px 0;border-left:4px solid {badge_color};"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="color:#fff;font-size:16px;font-weight:700;">{dept}</div><div style="background:{badge_color};color:white;padding:5px 14px;border-radius:20px;font-size:12px;font-weight:bold;">{pct_total:.0f}%</div></div></div>', unsafe_allow_html=True)
            real_ap_qtd = int(row['REAL_APARELHOS_QTD']); meta_ap_qtd = int(row['META_APARELHOS_QTD'])
            ca1, ca2, ca3 = st.columns(3)
            with ca1: st.markdown(pct_bar(real_novo, meta_novo, "Novo", "Meta"), unsafe_allow_html=True)
            with ca2: st.markdown(pct_bar(real_mig, meta_mig, "Migração", "Meta"), unsafe_allow_html=True)
            with ca3:
                pct_ap = (real_ap_qtd / meta_ap_qtd * 100) if meta_ap_qtd > 0 else 0
                color_ap = '#4CAF50' if pct_ap >= 100 else P if pct_ap >= 50 else P2
                width_ap = min(pct_ap, 100)
                st.markdown(f'<div style="margin:4px 0;"><div style="display:flex;justify-content:space-between;font-size:11px;color:{TEXT_DIM};"><span>Aparelhos: <b style="color:#fff">{real_ap_qtd}</b></span><span>Meta: <b>{meta_ap_qtd}</b></span></div><div style="background:rgba(123,47,247,0.15);border-radius:6px;height:14px;margin:3px 0;"><div style="background:{color_ap};border-radius:6px;height:14px;width:{width_ap}%;min-width:2px;"></div></div><div style="text-align:right;font-size:10px;color:{color_ap};font-weight:bold;">{pct_ap:.0f}% ({real_ap_qtd}/{meta_ap_qtd})</div></div>', unsafe_allow_html=True)
            st.markdown("---")

with tab6:
    st.markdown("## Tramitando - Previsão")
    st.markdown(f'<p style="color:{TEXT_DIM};">Pedidos em andamento filtrados pelos mesmos critérios da visão geral.</p>', unsafe_allow_html=True)
    tram_total = df_tram['VALOR_PRODUTO'].sum()
    tram_regs = len(df_tram)
    resultado_total = df_f['VALOR_PRODUTO'].sum()
    estimativa_otimista = resultado_total + tram_total
    estimativa_realista = resultado_total + (tram_total * 0.70)

    tram_novo_val = df_tram[df_tram['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()
    tram_taxa_novo = (tram_novo_val / tram_total * 100) if tram_total > 0 else 0
    tram_indicator = "up" if tram_taxa_novo >= 50 else ("neutral" if tram_taxa_novo >= 30 else "down")

    ct1, ct2, ct3, ct4, ct5 = st.columns(5)
    with ct1: st.markdown(card("Concluído", f"R${resultado_total:,.2f}", f"{len(df_f)} registros"), unsafe_allow_html=True)
    with ct2: st.markdown(card("Em Tramitação", f"R${tram_total:,.2f}", f"{tram_regs} pedidos", accent=True), unsafe_allow_html=True)
    with ct3: st.markdown(card("Est. Otimista", f"R${estimativa_otimista:,.2f}", "100% concluir"), unsafe_allow_html=True)
    with ct4: st.markdown(card("Est. Realista", f"R${estimativa_realista:,.2f}", "70% (-30%)", accent=True, indicator="up" if estimativa_realista > resultado_total * 1.5 else "neutral"), unsafe_allow_html=True)
    with ct5: st.markdown(card("Taxa Novo (Tram)", f"{tram_taxa_novo:.1f}%", "nos pedidos em tramitação", indicator=tram_indicator), unsafe_allow_html=True)

    st.markdown(f'<div style="background:rgba(255,152,0,0.08);border:1px solid rgba(255,152,0,0.3);border-radius:10px;padding:14px;margin:12px 0;"><b style="color:#ffb74d;">Atenção:</b> <span style="color:{TEXT_DIM};">~30% dos pedidos em tramitação podem não ser concluídos. A estimativa realista já considera esse corte.</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Visão Hierárquica: Pipeline > Fase")
    pipeline_data = df_tram.groupby('PIPELINE').agg(QTD=('VALOR_PRODUTO', 'count'), VALOR=('VALOR_PRODUTO', 'sum')).sort_values('VALOR', ascending=False).reset_index()
    for _, pipe_row in pipeline_data.iterrows():
        pipe_name = pipe_row['PIPELINE']
        pipe_valor = pipe_row['VALOR']
        pipe_qtd = int(pipe_row['QTD'])
        pipe_pct = (pipe_valor / tram_total * 100) if tram_total > 0 else 0
        st.markdown(f'''<div style="background:{CARD_BG};border:1px solid {CARD_BORDER};border-radius:14px;padding:18px;margin:14px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:4px;height:28px;background:linear-gradient(180deg,{P},{P2});border-radius:4px;"></div>
                    <div><div style="color:#fff;font-size:15px;font-weight:700;">{pipe_name}</div>
                    <div style="color:{TEXT_DIM};font-size:11px;">{pipe_qtd} pedidos</div></div>
                </div>
                <div style="text-align:right;">
                    <div style="color:{P};font-size:18px;font-weight:700;">R${pipe_valor:,.2f}</div>
                    <div style="color:{TEXT_DIM};font-size:10px;">{pipe_pct:.1f}% do total</div>
                </div>
            </div>
            <div style="background:rgba(123,47,247,0.08);border-radius:8px;padding:10px 14px;">''', unsafe_allow_html=True)
        fases_pipe = df_tram[df_tram['PIPELINE'] == pipe_name].groupby('FASE').agg(QTD=('VALOR_PRODUTO', 'count'), VALOR=('VALOR_PRODUTO', 'sum')).sort_values('VALOR', ascending=False).reset_index()
        for _, fase_row in fases_pipe.iterrows():
            fase_pct = (fase_row['VALOR'] / pipe_valor * 100) if pipe_valor > 0 else 0
            bar_w = min(fase_pct, 100)
            st.markdown(f'''<div style="display:flex;align-items:center;padding:6px 0;border-bottom:1px solid rgba(123,47,247,0.06);">
                <div style="width:6px;height:6px;background:{P2};border-radius:50%;margin-right:10px;flex-shrink:0;"></div>
                <div style="flex:1;color:{TEXT};font-size:12px;">{fase_row["FASE"]}</div>
                <div style="color:{TEXT_DIM};font-size:11px;margin-right:10px;">{int(fase_row["QTD"])}x</div>
                <div style="width:60px;background:rgba(123,47,247,0.15);border-radius:3px;height:6px;margin-right:10px;"><div style="background:{P2};border-radius:3px;height:6px;width:{bar_w}%;"></div></div>
                <div style="color:{P2};font-weight:600;font-size:12px;min-width:90px;text-align:right;">R${fase_row["VALOR"]:,.2f}</div>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Detalhamento")
    cols_tram = ['NOME_NEGOCIO', 'RESPONSAVEL', 'PRODUTO', 'TORRE', 'TIPO_VENDA', 'VALOR_PRODUTO', 'PIPELINE', 'FASE']
    available_tram = [c for c in cols_tram if c in df_tram.columns]
    st.dataframe(df_tram[available_tram].sort_values('VALOR_PRODUTO', ascending=False), use_container_width=True, height=400)

with tab3:
    st.markdown("## Buscar Pedido")
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1: busca_nome = st.text_input("Buscar por Nome / Cliente")
    with col_b2: busca_resp = st.selectbox("Responsável", ["Todos"] + sorted(df['RESPONSAVEL'].unique().tolist()), key="busca_resp")
    with col_b3: busca_fonte = st.selectbox("Fonte", ["Todos", "Concluídos", "Tramitando"], key="busca_fonte")
    if busca_fonte == "Concluídos":
        df_busca = df_f.copy()
    elif busca_fonte == "Tramitando":
        df_busca = df_tram.copy()
    else:
        df_busca_result = df_f.copy()
        df_busca_result['_FONTE'] = 'Concluído'
        df_busca_tram = df_tram.copy()
        df_busca_tram['_FONTE'] = 'Tramitando'
        df_busca = pd.concat([df_busca_result, df_busca_tram], ignore_index=True)
    if busca_nome: df_busca = df_busca[df_busca['NOME_NEGOCIO'].str.contains(busca_nome, case=False, na=False)]
    if busca_resp != "Todos": df_busca = df_busca[df_busca['RESPONSAVEL'] == busca_resp]
    st.markdown(f'<p style="color:{TEXT_DIM};font-size:13px;"><b style="color:#fff;">{len(df_busca)}</b> resultado(s)</p>', unsafe_allow_html=True)
    for _, row in df_busca.head(50).iterrows():
        fonte_label = row.get('_FONTE', '')
        fonte_badge = f'<span style="background:rgba(123,47,247,0.2);color:{P2};font-size:9px;padding:2px 6px;border-radius:4px;margin-left:8px;">{fonte_label}</span>' if fonte_label else ''
        fase_info = f' | {row.get("FASE", "")}' if 'FASE' in row.index and row.get('_FONTE', '') == 'Tramitando' else ''
        st.markdown(f'<div style="background:{CARD_BG};border:1px solid {CARD_BORDER};border-radius:12px;padding:14px;margin:8px 0;border-left:3px solid {P};transition:all 0.2s;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="color:#fff;font-size:13px;font-weight:600;">{row.get("NOME_NEGOCIO","")}{fonte_badge}</div><div style="color:{TEXT_DIM};font-size:11px;margin-top:4px;">{row.get("RESPONSAVEL","")} | {row.get("TORRE","")} | {row.get("TIPO_VENDA","")}{fase_info}</div></div><div style="text-align:right;"><div style="color:{P};font-size:20px;font-weight:700;">R${row.get("VALOR_PRODUTO",0):,.2f}</div></div></div></div>', unsafe_allow_html=True)

with tab4:
    st.markdown("## Dados Completos")
    st.markdown(f'<p style="color:{TEXT_DIM};"><b style="color:#fff;">{len(df_f)}</b> registros</p>', unsafe_allow_html=True)
    cols_show = ['NOME_NEGOCIO', 'RESPONSAVEL', 'PRODUTO', 'TORRE', 'TIPO_VENDA', 'VALOR_PRODUTO', 'LINHAS', 'CONCLUSAO_VIVO', 'PIPELINE', 'FASE', 'DEPARTAMENTO']
    available_cols = [c for c in cols_show if c in df_f.columns]
    st.dataframe(df_f[available_cols].sort_values('VALOR_PRODUTO', ascending=False), use_container_width=True, height=600)

with tab7:
    st.markdown("## Sobre o Dashboard")
    st.markdown(f"""
<div style="background:{CARD_BG};border:1px solid {CARD_BORDER};border-radius:16px;padding:28px;margin:10px 0;">

<h3 style="color:#fff !important;">O que são os Resultados?</h3>
<p>Pedidos <b>concluídos</b> no mês:</p>
<ul style="color:{TEXT};">
<li><b>Logística</b>: todas as fases (pedido vendido, em entrega/ativação)</li>
<li><b>Fixa Básica / Avançados / Digitais(TI)</b>: apenas fase "Pedido Concluído"</li>
</ul>
<p><b>Não contam</b>: DOWN, TT, Troca Pura, cancelados.</p>

<hr style="border-color:rgba(123,47,247,0.2);">

<h3 style="color:#fff !important;">O que está Tramitando?</h3>
<p>Pedidos <b>em andamento</b> nos pipelines Pré Vendas, Inserção, Quality, Fixa Básica, Avançados, Digitais(TI).</p>
<p><b>Excluídos</b>: Cancelado, Perda de Vendas, Crédito Reprovado/Negado, Cancelamento Comercial.</p>

<hr style="border-color:rgba(123,47,247,0.2);">

<h3 style="color:#fff !important;">Taxa de Novo</h3>
<p>Percentual do valor total que veio de vendas <b>NOVO</b> (Alta, Portabilidade). Indicador verde = acima de 50%, amarelo = 30-50%, vermelho = abaixo de 30%.</p>

<hr style="border-color:rgba(123,47,247,0.2);">

<h3 style="color:#fff !important;">Estimativa do Mês</h3>
<p><b>Concluído + 70% Tramitando = Estimativa Realista</b></p>

<hr style="border-color:rgba(123,47,247,0.2);">

<h3 style="color:#fff !important;">Classificação</h3>
<ul style="color:{TEXT};">
<li><b>Torre</b>: Smart Empresas/Ilimitado = Móvel</li>
<li><b>Tipo Venda</b>: produto "| NOVO" ou Alta/Portabilidade = NOVO</li>
<li><b>Linhas</b>: MAX por pedido, mínimo 1</li>
</ul>

</div>
""", unsafe_allow_html=True)
