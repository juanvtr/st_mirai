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
PL = '#E0AAFF'
BG = '#ffffff'
CARD = '#f8f6ff'

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    .card {{
        background: {CARD};
        border: 1px solid #e8e0f7;
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        margin-bottom: 10px;
        border-left: 4px solid {P};
        box-shadow: 0 2px 8px rgba(123,47,247,0.06);
    }}
    .card-accent {{
        background: linear-gradient(135deg, #f3e8ff, #ede0ff);
        border: 1px solid #d4b8ff;
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        margin-bottom: 10px;
        border-left: 4px solid {P2};
        box-shadow: 0 2px 8px rgba(157,78,221,0.1);
    }}
    .card-title {{ color: #666; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
    .card-value {{ color: #1a1a2e; font-size: 22px; font-weight: 700; margin: 6px 0; }}
    .card-sub {{ color: {P}; font-size: 10px; }}
    h1, h2, h3 {{ color: #1a1a2e !important; }}
    .stSelectbox label, .stMultiSelect label, .stTextInput label {{ color: #333 !important; }}
    .stMultiSelect span[data-baseweb="tag"] {{
        background-color: {P} !important;
        color: white !important;
    }}
    div[data-baseweb="popover"] li:hover {{ background-color: #f3e8ff !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #f3f0fa; border-radius: 8px; }}
    .stTabs [data-baseweb="tab"] {{ color: #666 !important; }}
    .stTabs [aria-selected="true"] {{ color: white !important; background-color: {P} !important; border-radius: 6px; }}
    .stMarkdown hr {{ border-color: #e8e0f7 !important; }}
    section[data-testid="stSidebar"] {{ background-color: #f9f7fe !important; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    conn = snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM MIRAI.PUBLIC.RELATORIO_COMPLETO")
    df = cur.fetch_pandas_all()
    conn.close()
    df['DEPARTAMENTO'] = df['RESPONSAVEL'].map(DEPT_MAP).fillna('Outros')
    df['VALOR_PRODUTO'] = pd.to_numeric(df['VALOR_PRODUTO'], errors='coerce').fillna(0)
    df['LINHAS'] = pd.to_numeric(df['LINHAS'], errors='coerce').fillna(0)
    df['MES'] = pd.to_datetime(df['CONCLUSAO_VIVO'], format='%d/%m/%Y', errors='coerce').dt.to_period('M').astype(str)
    return df

df = load_data()

def card(title, value, sub="", accent=False):
    cls = "card-accent" if accent else "card"
    return f'<div class="{cls}"><div class="card-title">{title}</div><div class="card-value">{value}</div><div class="card-sub">{sub}</div></div>'

with st.sidebar:
    st.markdown("### Filtros")
    meses = sorted(df['MES'].dropna().unique(), reverse=True)
    mes_sel = st.selectbox("Mes", ["Todos"] + list(meses))
    depts = sorted(df['DEPARTAMENTO'].unique())
    dept_sel = st.multiselect("Departamento", depts, default=depts)
    torres = sorted(df['TORRE'].unique())
    torre_sel = st.multiselect("Torre", torres, default=torres)
    tipos = ['MIGRAÇÃO', 'NOVO']
    tipo_sel = st.multiselect("Tipo de Venda", tipos, default=tipos)

df_f = df.copy()
if mes_sel != "Todos":
    df_f = df_f[df_f['MES'] == mes_sel]
df_f = df_f[df_f['DEPARTAMENTO'].isin(dept_sel)]
df_f = df_f[df_f['TORRE'].isin(torre_sel)]
df_f = df_f[df_f['TIPO_VENDA'].isin(tipo_sel)]

tab1, tab2, tab3, tab4 = st.tabs(["Visao Geral", "Produtos", "Buscar Pedido", "Dados"])

with tab1:
    st.markdown("## Visao Geral")
    total = df_f['VALOR_PRODUTO'].sum()
    mig = df_f[df_f['TIPO_VENDA'] == 'MIGRAÇÃO']['VALOR_PRODUTO'].sum()
    novo = df_f[df_f['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()
    regs = len(df_f)
    mov_mig = df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum()
    mov_nov = df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum()
    fix_mig = df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum()
    fix_nov = df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum()
    avanc = df_f[df_f['TORRE'] == 'Avançados']['VALOR_PRODUTO'].sum()
    ti = df_f[df_f['TORRE'] == 'TI']['VALOR_PRODUTO'].sum()
    mov_mig_reg = len(df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')])
    mov_nov_reg = len(df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'NOVO')])
    fix_mig_reg = len(df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')])
    fix_nov_reg = len(df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'NOVO')])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(card("Total Geral", f"R${total:,.2f}", f"{regs} registros"), unsafe_allow_html=True)
    with c2:
        st.markdown(card("Total Migracao", f"R${mig:,.2f}", f"{len(df_f[df_f['TIPO_VENDA']=='MIGRAÇÃO'])} reg"), unsafe_allow_html=True)
    with c3:
        st.markdown(card("Total Novo", f"R${novo:,.2f}", f"{len(df_f[df_f['TIPO_VENDA']=='NOVO'])} reg", accent=True), unsafe_allow_html=True)

    st.markdown("#### Movel")
    cm1, cm2, cm3 = st.columns(3)
    with cm1:
        st.markdown(card("Movel Total", f"R${mov_mig+mov_nov:,.2f}", f"{mov_mig_reg+mov_nov_reg} reg"), unsafe_allow_html=True)
    with cm2:
        st.markdown(card("Mig. Movel", f"R${mov_mig:,.2f}", f"{mov_mig_reg} reg"), unsafe_allow_html=True)
    with cm3:
        st.markdown(card("Novo Movel", f"R${mov_nov:,.2f}", f"{mov_nov_reg} reg", accent=True), unsafe_allow_html=True)

    st.markdown("#### Fixa PJ")
    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        st.markdown(card("Fixa Total", f"R${fix_mig+fix_nov:,.2f}", f"{fix_mig_reg+fix_nov_reg} reg"), unsafe_allow_html=True)
    with cf2:
        st.markdown(card("Mig. Fixa", f"R${fix_mig:,.2f}", f"{fix_mig_reg} reg"), unsafe_allow_html=True)
    with cf3:
        st.markdown(card("Novo Fixa", f"R${fix_nov:,.2f}", f"{fix_nov_reg} reg", accent=True), unsafe_allow_html=True)

    st.markdown("#### Avancados & TI")
    ca1, ca2 = st.columns(2)
    with ca1:
        avanc_reg = len(df_f[df_f['TORRE'] == 'Avançados'])
        st.markdown(card("Avancados", f"R${avanc:,.2f}", f"{avanc_reg} reg"), unsafe_allow_html=True)
        if avanc_reg > 0:
            av_prods = df_f[df_f['TORRE'] == 'Avançados'].groupby('PRODUTO')['VALOR_PRODUTO'].sum().sort_values(ascending=False).head(5)
            for prod, val in av_prods.items():
                st.markdown(f"<div style='color:#555;font-size:12px;padding:2px 12px;'>- {prod}: <b style=\"color:{P}\">R${val:,.2f}</b></div>", unsafe_allow_html=True)
    with ca2:
        ti_reg = len(df_f[df_f['TORRE'] == 'TI'])
        st.markdown(card("TI / Digitais", f"R${ti:,.2f}", f"{ti_reg} reg"), unsafe_allow_html=True)
        if ti_reg > 0:
            ti_prods = df_f[df_f['TORRE'] == 'TI'].groupby('PRODUTO')['VALOR_PRODUTO'].sum().sort_values(ascending=False).head(5)
            for prod, val in ti_prods.items():
                st.markdown(f"<div style='color:#555;font-size:12px;padding:2px 12px;'>- {prod}: <b style=\"color:{P}\">R${val:,.2f}</b></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Ranking por Departamento")
    dept_resumo = df_f.groupby('DEPARTAMENTO')['VALOR_PRODUTO'].sum().sort_values(ascending=False).reset_index()
    for _, row in dept_resumo.iterrows():
        pct = (row['VALOR_PRODUTO']/total*100) if total > 0 else 0
        st.markdown(f"""<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e0f7;">
            <div style="flex:1;color:#333;font-size:13px;font-weight:500;">{row['DEPARTAMENTO']}</div>
            <div style="color:{P};font-weight:bold;font-size:13px;">R${row['VALOR_PRODUTO']:,.2f}</div>
            <div style="color:#999;font-size:11px;margin-left:12px;width:50px;text-align:right;">{pct:.1f}%</div>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("## Produtos Mais Vendidos")
    torre_prod = st.selectbox("Filtrar por Torre", ["Todas"] + list(torres), key="torre_prod")
    df_prod = df_f if torre_prod == "Todas" else df_f[df_f['TORRE'] == torre_prod]

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### Top Produtos - Migracao")
        prods_mig = df_prod[df_prod['TIPO_VENDA'] == 'MIGRAÇÃO'].groupby('PRODUTO').agg(
            VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')
        ).sort_values('VALOR', ascending=False).head(15)
        for i, (prod, row) in enumerate(prods_mig.iterrows(), 1):
            st.markdown(f"""<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e0f7;">
                <div style="color:{P};font-weight:bold;width:24px;">{i}</div>
                <div style="flex:1;color:#333;font-size:12px;">{prod}</div>
                <div style="color:#888;font-size:11px;margin-right:12px;">{int(row['QTD'])}x</div>
                <div style="color:{P};font-weight:bold;font-size:12px;">R${row['VALOR']:,.2f}</div>
            </div>""", unsafe_allow_html=True)

    with col_p2:
        st.markdown("#### Top Produtos - Novo")
        prods_nov = df_prod[df_prod['TIPO_VENDA'] == 'NOVO'].groupby('PRODUTO').agg(
            VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')
        ).sort_values('VALOR', ascending=False).head(15)
        for i, (prod, row) in enumerate(prods_nov.iterrows(), 1):
            st.markdown(f"""<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e0f7;">
                <div style="color:{P2};font-weight:bold;width:24px;">{i}</div>
                <div style="flex:1;color:#333;font-size:12px;">{prod}</div>
                <div style="color:#888;font-size:11px;margin-right:12px;">{int(row['QTD'])}x</div>
                <div style="color:{P2};font-weight:bold;font-size:12px;">R${row['VALOR']:,.2f}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Avancados - Detalhamento")
    av_detail = df_f[df_f['TORRE'] == 'Avançados'].groupby(['PRODUTO', 'TIPO_VENDA']).agg(
        VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')
    ).sort_values('VALOR', ascending=False).reset_index()
    if len(av_detail) > 0:
        st.dataframe(av_detail, use_container_width=True, height=200)
    else:
        st.info("Sem dados de Avancados no filtro atual")

    st.markdown("#### TI / Digitais - Detalhamento")
    ti_detail = df_f[df_f['TORRE'] == 'TI'].groupby(['PRODUTO', 'TIPO_VENDA']).agg(
        VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')
    ).sort_values('VALOR', ascending=False).reset_index()
    if len(ti_detail) > 0:
        st.dataframe(ti_detail, use_container_width=True, height=200)
    else:
        st.info("Sem dados de TI no filtro atual")

with tab3:
    st.markdown("## Buscar Pedido")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        busca_nome = st.text_input("Buscar por Nome do Negocio / Cliente")
    with col_b2:
        busca_resp = st.selectbox("Filtrar por Responsavel", ["Todos"] + sorted(df['RESPONSAVEL'].unique().tolist()), key="busca_resp")

    df_busca = df_f.copy()
    if busca_nome:
        df_busca = df_busca[df_busca['NOME_NEGOCIO'].str.contains(busca_nome, case=False, na=False)]
    if busca_resp != "Todos":
        df_busca = df_busca[df_busca['RESPONSAVEL'] == busca_resp]

    st.markdown(f"**{len(df_busca)} resultado(s) encontrado(s)**")

    if len(df_busca) > 0:
        for _, row in df_busca.head(50).iterrows():
            st.markdown(f"""<div style="background:{CARD};border:1px solid #e8e0f7;border-radius:8px;padding:12px;margin:8px 0;border-left:3px solid {P};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="color:#1a1a2e;font-size:13px;font-weight:bold;">{row.get('NOME_NEGOCIO','')}</div>
                        <div style="color:#666;font-size:11px;margin-top:4px;">{row.get('RESPONSAVEL','')} | {row.get('TORRE','')} | {row.get('TIPO_VENDA','')}</div>
                        <div style="color:#999;font-size:11px;">{row.get('PRODUTO','')} | {row.get('PIPELINE','')}/{row.get('FASE','')}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:{P};font-size:18px;font-weight:bold;">R${row.get('VALOR_PRODUTO',0):,.2f}</div>
                        <div style="color:#999;font-size:10px;">{row.get('CONCLUSAO_VIVO','')}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

with tab4:
    st.markdown("## Dados Completos")
    st.markdown(f"**{len(df_f)} registros** no filtro atual")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.markdown(card("Registros", f"{len(df_f)}", "no filtro"), unsafe_allow_html=True)
    with col_d2:
        st.markdown(card("Vendedores", f"{df_f['RESPONSAVEL'].nunique()}", "ativos"), unsafe_allow_html=True)
    with col_d3:
        st.markdown(card("Produtos", f"{df_f['PRODUTO'].nunique()}", "diferentes"), unsafe_allow_html=True)

    cols_show = ['NOME_NEGOCIO', 'RESPONSAVEL', 'PRODUTO', 'TORRE', 'TIPO_VENDA', 'VALOR_PRODUTO', 'CONCLUSAO_VIVO', 'PIPELINE', 'FASE', 'DEPARTAMENTO']
    available_cols = [c for c in cols_show if c in df_f.columns]
    st.dataframe(df_f[available_cols].sort_values('VALOR_PRODUTO', ascending=False), use_container_width=True, height=600)
