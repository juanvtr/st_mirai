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
BG = '#ffffff'
CARD = '#f8f6ff'

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    .card {{ background: {CARD}; border: 1px solid #e8e0f7; border-radius: 12px; padding: 18px 14px; text-align: center; margin-bottom: 10px; border-left: 4px solid {P}; box-shadow: 0 2px 8px rgba(123,47,247,0.06); }}
    .card-accent {{ background: linear-gradient(135deg, #f3e8ff, #ede0ff); border: 1px solid #d4b8ff; border-radius: 12px; padding: 18px 14px; text-align: center; margin-bottom: 10px; border-left: 4px solid {P2}; box-shadow: 0 2px 8px rgba(157,78,221,0.1); }}
    .card-title {{ color: #666; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
    .card-value {{ color: #1a1a2e; font-size: 22px; font-weight: 700; margin: 6px 0; }}
    .card-sub {{ color: {P}; font-size: 10px; }}
    h1, h2, h3 {{ color: #1a1a2e !important; }}
    .stMultiSelect span[data-baseweb="tag"] {{ background-color: {P} !important; color: white !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: #f3f0fa; border-radius: 8px; }}
    .stTabs [data-baseweb="tab"] {{ color: #666 !important; }}
    .stTabs [aria-selected="true"] {{ color: white !important; background-color: {P} !important; border-radius: 6px; }}
    .stMarkdown hr {{ border-color: #e8e0f7 !important; }}
    section[data-testid="stSidebar"] {{ background-color: #f9f7fe !important; }}
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

df = load_data()
df_metas = load_metas()
df_tram = load_tramitando()
has_metas = len(df_metas) > 0

def card(title, value, sub="", accent=False):
    cls = "card-accent" if accent else "card"
    return f'<div class="{cls}"><div class="card-title">{title}</div><div class="card-value">{value}</div><div class="card-sub">{sub}</div></div>'

def count_linhas(dataframe):
    if len(dataframe) == 0:
        return 0
    return int(dataframe.groupby('NOME_NEGOCIO')['LINHAS'].max().clip(lower=1).sum())

with st.sidebar:
    st.markdown("### Filtros")
    cargas = sorted(df['DATA_CARGA'].dropna().unique(), reverse=True)
    carga_labels = [str(c) for c in cargas]
    carga_sel = st.selectbox("Snapshot (Data Carga)", carga_labels, index=0)
    st.markdown("---")
    meses = sorted(df['MES'].dropna().unique(), reverse=True)
    mes_sel = st.selectbox("Mes", ["Todos"] + list(meses))
    depts = sorted(df['DEPARTAMENTO'].unique())
    dept_sel = st.multiselect("Departamento", depts, default=depts)
    torres = sorted(df['TORRE'].unique())
    torre_sel = st.multiselect("Torre", torres, default=torres)
    tipos = ['MIGRAÇÃO', 'NOVO']
    tipo_sel = st.multiselect("Tipo de Venda", tipos, default=tipos)

df_f = df[df['DATA_CARGA'] == pd.to_datetime(carga_sel).date()].copy()
if mes_sel != "Todos":
    df_f = df_f[df_f['MES'] == mes_sel]
df_f = df_f[df_f['DEPARTAMENTO'].isin(dept_sel)]
df_f = df_f[df_f['TORRE'].isin(torre_sel)]
df_f = df_f[df_f['TIPO_VENDA'].isin(tipo_sel)]

tab1, tab2, tab5, tab6, tab3, tab4, tab7 = st.tabs(["Visao Geral", "Produtos", "Metas", "Tramitando", "Buscar Pedido", "Dados", "Sobre"])

with tab1:
    st.markdown("## Visao Geral")
    total = df_f['VALOR_PRODUTO'].sum()
    mig = df_f[df_f['TIPO_VENDA'] == 'MIGRAÇÃO']['VALOR_PRODUTO'].sum()
    novo = df_f[df_f['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()
    mov_mig = df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum()
    mov_nov = df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum()
    fix_mig = df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum()
    fix_nov = df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum()
    avanc = df_f[df_f['TORRE'] == 'Avançados']['VALOR_PRODUTO'].sum()
    ti = df_f[df_f['TORRE'] == 'TI']['VALOR_PRODUTO'].sum()
    mov_mig_linhas = count_linhas(df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')])
    mov_nov_linhas = count_linhas(df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'NOVO')])
    fix_mig_linhas = count_linhas(df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')])
    fix_nov_linhas = count_linhas(df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'NOVO')])
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(card("Total Geral", f"R${total:,.2f}", f"{count_linhas(df_f)} linhas"), unsafe_allow_html=True)
    with c2: st.markdown(card("Total Migracao", f"R${mig:,.2f}", f"{count_linhas(df_f[df_f['TIPO_VENDA']=='MIGRAÇÃO'])} linhas"), unsafe_allow_html=True)
    with c3: st.markdown(card("Total Novo", f"R${novo:,.2f}", f"{count_linhas(df_f[df_f['TIPO_VENDA']=='NOVO'])} linhas", accent=True), unsafe_allow_html=True)
    st.markdown("#### Movel")
    cm1, cm2, cm3 = st.columns(3)
    with cm1: st.markdown(card("Movel Total", f"R${mov_mig+mov_nov:,.2f}", f"{mov_mig_linhas+mov_nov_linhas} linhas"), unsafe_allow_html=True)
    with cm2: st.markdown(card("Mig. Movel", f"R${mov_mig:,.2f}", f"{mov_mig_linhas} linhas"), unsafe_allow_html=True)
    with cm3: st.markdown(card("Novo Movel", f"R${mov_nov:,.2f}", f"{mov_nov_linhas} linhas", accent=True), unsafe_allow_html=True)
    st.markdown("#### Fixa PJ")
    cf1, cf2, cf3 = st.columns(3)
    with cf1: st.markdown(card("Fixa Total", f"R${fix_mig+fix_nov:,.2f}", f"{fix_mig_linhas+fix_nov_linhas} linhas"), unsafe_allow_html=True)
    with cf2: st.markdown(card("Mig. Fixa", f"R${fix_mig:,.2f}", f"{fix_mig_linhas} linhas"), unsafe_allow_html=True)
    with cf3: st.markdown(card("Novo Fixa", f"R${fix_nov:,.2f}", f"{fix_nov_linhas} linhas", accent=True), unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Ranking por Departamento")
    dept_resumo = df_f.groupby('DEPARTAMENTO')['VALOR_PRODUTO'].sum().sort_values(ascending=False).reset_index()
    for _, row in dept_resumo.iterrows():
        pct = (row['VALOR_PRODUTO']/total*100) if total > 0 else 0
        st.markdown(f'<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e0f7;"><div style="flex:1;color:#333;font-size:13px;font-weight:500;">{row["DEPARTAMENTO"]}</div><div style="color:{P};font-weight:bold;font-size:13px;">R${row["VALOR_PRODUTO"]:,.2f}</div><div style="color:#999;font-size:11px;margin-left:12px;width:50px;text-align:right;">{pct:.1f}%</div></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("## Produtos Mais Vendidos")
    torre_prod = st.selectbox("Filtrar por Torre", ["Todas"] + list(torres), key="torre_prod")
    df_prod = df_f if torre_prod == "Todas" else df_f[df_f['TORRE'] == torre_prod]
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("#### Top Produtos - Migracao")
        for i, (prod, row) in enumerate(df_prod[df_prod['TIPO_VENDA'] == 'MIGRAÇÃO'].groupby('PRODUTO').agg(VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')).sort_values('VALOR', ascending=False).head(15).iterrows(), 1):
            st.markdown(f'<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e0f7;"><div style="color:{P};font-weight:bold;width:24px;">{i}</div><div style="flex:1;color:#333;font-size:12px;">{prod}</div><div style="color:#888;font-size:11px;margin-right:12px;">{int(row["QTD"])}x</div><div style="color:{P};font-weight:bold;font-size:12px;">R${row["VALOR"]:,.2f}</div></div>', unsafe_allow_html=True)
    with col_p2:
        st.markdown("#### Top Produtos - Novo")
        for i, (prod, row) in enumerate(df_prod[df_prod['TIPO_VENDA'] == 'NOVO'].groupby('PRODUTO').agg(VALOR=('VALOR_PRODUTO', 'sum'), QTD=('VALOR_PRODUTO', 'count')).sort_values('VALOR', ascending=False).head(15).iterrows(), 1):
            st.markdown(f'<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e0f7;"><div style="color:{P2};font-weight:bold;width:24px;">{i}</div><div style="flex:1;color:#333;font-size:12px;">{prod}</div><div style="color:#888;font-size:11px;margin-right:12px;">{int(row["QTD"])}x</div><div style="color:{P2};font-weight:bold;font-size:12px;">R${row["VALOR"]:,.2f}</div></div>', unsafe_allow_html=True)

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
            elif pct >= 75: color = '#7B2FF7'
            elif pct >= 50: color = '#9D4EDD'
            elif pct >= 25: color = '#C77DFF'
            else: color = '#E0AAFF'
            width = min(pct, 100)
            return f'<div style="margin:4px 0;"><div style="display:flex;justify-content:space-between;font-size:11px;color:#666;"><span>{label_r}: <b style="color:#333">R${real:,.2f}</b></span><span>Meta: <b>R${meta:,.2f}</b></span></div><div style="background:#e8e0f7;border-radius:6px;height:14px;margin:3px 0;"><div style="background:{color};border-radius:6px;height:14px;width:{width}%;min-width:2px;"></div></div><div style="text-align:right;font-size:10px;color:{color};font-weight:bold;">{pct:.1f}%</div></div>'
        for _, row in merged.iterrows():
            dept = row['DEPARTAMENTO']; meta_novo = float(row['META_NOVO_TOTAL']); meta_mig = float(row['META_MIGRACAO_TOTAL'])
            real_novo = float(row['REAL_NOVO']); real_mig = float(row['REAL_MIG']); meta_total = meta_novo + meta_mig; real_total = float(row['REAL_TOTAL'])
            pct_total = (real_total / meta_total * 100) if meta_total > 0 else 0
            badge_color = '#4CAF50' if pct_total >= 100 else '#7B2FF7' if pct_total >= 50 else '#9D4EDD'
            st.markdown(f'<div style="background:{CARD};border:1px solid #e8e0f7;border-radius:12px;padding:16px;margin:10px 0;border-left:4px solid {badge_color};"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="color:#1a1a2e;font-size:16px;font-weight:700;">{dept}</div><div style="background:{badge_color};color:white;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:bold;">{pct_total:.0f}% total</div></div></div>', unsafe_allow_html=True)
            real_ap_qtd = int(row['REAL_APARELHOS_QTD']); meta_ap_qtd = int(row['META_APARELHOS_QTD'])
            ca1, ca2, ca3 = st.columns(3)
            with ca1: st.markdown(pct_bar(real_novo, meta_novo, "Novo", "Meta"), unsafe_allow_html=True)
            with ca2: st.markdown(pct_bar(real_mig, meta_mig, "Migracao", "Meta"), unsafe_allow_html=True)
            with ca3:
                pct_ap = (real_ap_qtd / meta_ap_qtd * 100) if meta_ap_qtd > 0 else 0
                color_ap = '#4CAF50' if pct_ap >= 100 else '#7B2FF7' if pct_ap >= 50 else '#9D4EDD'
                width_ap = min(pct_ap, 100)
                st.markdown(f'<div style="margin:4px 0;"><div style="display:flex;justify-content:space-between;font-size:11px;color:#666;"><span>Aparelhos: <b style="color:#333">{real_ap_qtd}</b></span><span>Meta: <b>{meta_ap_qtd}</b></span></div><div style="background:#e8e0f7;border-radius:6px;height:14px;margin:3px 0;"><div style="background:{color_ap};border-radius:6px;height:14px;width:{width_ap}%;min-width:2px;"></div></div><div style="text-align:right;font-size:10px;color:{color_ap};font-weight:bold;">{pct_ap:.0f}% ({real_ap_qtd}/{meta_ap_qtd})</div></div>', unsafe_allow_html=True)
            st.markdown("---")

with tab6:
    st.markdown("## Tramitando - Previsao")
    st.markdown("Pedidos em andamento que podem ser concluidos neste mes.")
    tram_total = df_tram['VALOR_PRODUTO'].sum()
    tram_regs = len(df_tram)
    resultado_total = df_f['VALOR_PRODUTO'].sum()
    estimativa_otimista = resultado_total + tram_total
    estimativa_realista = resultado_total + (tram_total * 0.70)
    ct1, ct2, ct3, ct4 = st.columns(4)
    with ct1: st.markdown(card("Concluido", f"R${resultado_total:,.2f}", f"{len(df_f)} registros"), unsafe_allow_html=True)
    with ct2: st.markdown(card("Em Tramitacao", f"R${tram_total:,.2f}", f"{tram_regs} pedidos", accent=True), unsafe_allow_html=True)
    with ct3: st.markdown(card("Estimativa Otimista", f"R${estimativa_otimista:,.2f}", "100% concluir"), unsafe_allow_html=True)
    with ct4: st.markdown(card("Estimativa Realista", f"R${estimativa_realista:,.2f}", "70% concluir (-30%)", accent=True), unsafe_allow_html=True)
    st.markdown(f'<div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:8px;padding:12px;margin:10px 0;"><b style="color:#e65100;">Atencao:</b> <span style="color:#bf360c;">Historicamente, ~30% dos pedidos em tramitacao podem nao ser concluidos (cancelamentos, credito reprovado, desistencias). A estimativa realista ja considera esse corte.</span></div>', unsafe_allow_html=True)
    st.markdown("#### Por Pipeline")
    for _, row in df_tram.groupby('PIPELINE').agg(QTD=('VALOR_PRODUTO', 'count'), VALOR=('VALOR_PRODUTO', 'sum')).sort_values('VALOR', ascending=False).reset_index().iterrows():
        st.markdown(f'<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e0f7;"><div style="flex:1;color:#333;font-size:13px;font-weight:500;">{row["PIPELINE"]}</div><div style="color:#888;font-size:12px;margin-right:12px;">{int(row["QTD"])} pedidos</div><div style="color:{P};font-weight:bold;font-size:13px;">R${row["VALOR"]:,.2f}</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Por Fase")
    for _, row in df_tram.groupby('FASE').agg(QTD=('VALOR_PRODUTO', 'count'), VALOR=('VALOR_PRODUTO', 'sum')).sort_values('VALOR', ascending=False).reset_index().iterrows():
        st.markdown(f'<div style="display:flex;align-items:center;padding:6px 0;border-bottom:1px solid #f0eaf7;"><div style="flex:1;color:#555;font-size:12px;">{row["FASE"]}</div><div style="color:#888;font-size:11px;margin-right:12px;">{int(row["QTD"])}x</div><div style="color:{P2};font-weight:bold;font-size:12px;">R${row["VALOR"]:,.2f}</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Detalhamento")
    cols_tram = ['NOME_NEGOCIO', 'RESPONSAVEL', 'PRODUTO', 'TORRE', 'TIPO_VENDA', 'VALOR_PRODUTO', 'PIPELINE', 'FASE']
    available_tram = [c for c in cols_tram if c in df_tram.columns]
    st.dataframe(df_tram[available_tram].sort_values('VALOR_PRODUTO', ascending=False), use_container_width=True, height=400)

with tab3:
    st.markdown("## Buscar Pedido")
    col_b1, col_b2 = st.columns(2)
    with col_b1: busca_nome = st.text_input("Buscar por Nome do Negocio / Cliente")
    with col_b2: busca_resp = st.selectbox("Filtrar por Responsavel", ["Todos"] + sorted(df['RESPONSAVEL'].unique().tolist()), key="busca_resp")
    df_busca = df_f.copy()
    if busca_nome: df_busca = df_busca[df_busca['NOME_NEGOCIO'].str.contains(busca_nome, case=False, na=False)]
    if busca_resp != "Todos": df_busca = df_busca[df_busca['RESPONSAVEL'] == busca_resp]
    st.markdown(f"**{len(df_busca)} resultado(s)**")
    for _, row in df_busca.head(50).iterrows():
        st.markdown(f'<div style="background:{CARD};border:1px solid #e8e0f7;border-radius:8px;padding:12px;margin:8px 0;border-left:3px solid {P};"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="color:#1a1a2e;font-size:13px;font-weight:bold;">{row.get("NOME_NEGOCIO","")}</div><div style="color:#666;font-size:11px;margin-top:4px;">{row.get("RESPONSAVEL","")} | {row.get("TORRE","")} | {row.get("TIPO_VENDA","")}</div></div><div style="text-align:right;"><div style="color:{P};font-size:18px;font-weight:bold;">R${row.get("VALOR_PRODUTO",0):,.2f}</div></div></div></div>', unsafe_allow_html=True)

with tab4:
    st.markdown("## Dados Completos")
    st.markdown(f"**{len(df_f)} registros**")
    cols_show = ['NOME_NEGOCIO', 'RESPONSAVEL', 'PRODUTO', 'TORRE', 'TIPO_VENDA', 'VALOR_PRODUTO', 'LINHAS', 'CONCLUSAO_VIVO', 'PIPELINE', 'FASE', 'DEPARTAMENTO']
    available_cols = [c for c in cols_show if c in df_f.columns]
    st.dataframe(df_f[available_cols].sort_values('VALOR_PRODUTO', ascending=False), use_container_width=True, height=600)

with tab7:
    st.markdown("## Sobre o Dashboard")
    st.markdown(f"""
<div style="background:{CARD};border:1px solid #e8e0f7;border-radius:12px;padding:24px;margin:10px 0;">

### O que sao os Resultados?
Pedidos **concluidos** no mes:
- **Logistica**: todas as fases (pedido vendido, em entrega/ativacao)
- **Fixa Basica / Avancados / Digitais(TI)**: apenas fase "Pedido Concluido"

**Nao contam**: DOWN, TT, Troca Pura, cancelados.

---

### O que esta Tramitando?
Pedidos **em andamento** nos pipelines Pre Vendas, Insercao, Quality, Fixa Basica, Avancados, Digitais(TI).

**Excluidos**: Cancelado, Perda de Vendas, Credito Reprovado/Negado, Cancelamento Comercial.

---

### Estimativa do Mes
**Concluido + Tramitando = Estimativa**

---

### Classificacao
- **Torre**: Smart Empresas/Ilimitado = Movel
- **Tipo Venda**: produto "| NOVO" ou Alta/Portabilidade = NOVO; com "MIGRACAO/PADRAO" = MIGRACAO
- **Linhas**: MAX por pedido, minimo 1

---

### Atualizacao
Dados atualizados via notebook ETL. Historico com snapshots por data.

</div>
""", unsafe_allow_html=True)

