import streamlit as st
import pandas as pd
import altair as alt
import snowflake.connector

st.set_page_config(page_title="Dashboard de Vendas - Mirai", layout="wide")

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
    'Elias Polinario': 'Time Jéssica',
    'maria cristina duarte': 'Time Jéssica',
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
    'Fernando Xiscatti': 'Time Xiscatti',
    'Xiscatti Liberty Consulting': 'Time Xiscatti',
    'Raquel Macedo': 'Calister', 'Luciene de Oliveira Ferreira': 'Calister',
    'Deisy Ponte': 'Calister',
    'Luis Lopes': 'Time de Tramitação', 'Stela Maira': 'Time de Tramitação',
    'Beatriz Lima': 'Time de Tramitação', 'Bruna Salatiel': 'Time de Tramitação',
    'Evelin Araújo': 'Time de Tramitação', 'Ivete Lemos': 'Time de Tramitação',
}

P = '#7B2FF7'
PA = '#C77DFF'
BG = '#1a1a2e'
CARD = '#16213e'

st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    .metric-card {{
        background: {CARD};
        border: 2px solid {P};
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        margin-bottom: 8px;
    }}
    .metric-card-accent {{
        background: {CARD};
        border: 2px solid {PA};
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        margin-bottom: 8px;
    }}
    .metric-title {{ color: #aaa; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
    .metric-value {{ color: #fff; font-size: 24px; font-weight: bold; margin: 6px 0; }}
    .metric-sub {{ color: {PA}; font-size: 11px; }}
    h1, h2, h3 {{ color: #fff !important; }}
    .stSelectbox label, .stMultiSelect label {{ color: #fff !important; }}
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        background-color: {CARD} !important;
        border-color: {P} !important;
    }}
    .stMultiSelect span[data-baseweb="tag"] {{
        background-color: {P} !important;
        color: white !important;
    }}
    .stMultiSelect span[data-baseweb="tag"] span[role="presentation"] {{
        color: white !important;
    }}
    div[data-baseweb="popover"] li {{
        background-color: {CARD} !important;
        color: white !important;
    }}
    div[data-baseweb="popover"] li:hover {{
        background-color: {P} !important;
    }}
    .stMarkdown hr {{ border-color: #333 !important; }}
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

def card(title, value, subtitle="", accent=False):
    cls = "metric-card-accent" if accent else "metric-card"
    return f'<div class="{cls}"><div class="metric-title">{title}</div><div class="metric-value">{value}</div><div class="metric-sub">{subtitle}</div></div>'

st.title("Dashboard de Vendas - Mirai")

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    meses = sorted(df['MES'].dropna().unique(), reverse=True)
    mes_sel = st.selectbox("Mês", ["Todos"] + list(meses))
with col_f2:
    depts = sorted(df['DEPARTAMENTO'].unique())
    dept_sel = st.multiselect("Departamento", depts, default=depts)
with col_f3:
    torres = sorted(df['TORRE'].unique())
    torre_sel = st.multiselect("Torre", torres, default=torres)

df_f = df.copy()
if mes_sel != "Todos":
    df_f = df_f[df_f['MES'] == mes_sel]
df_f = df_f[df_f['DEPARTAMENTO'].isin(dept_sel)]
df_f = df_f[df_f['TORRE'].isin(torre_sel)]

total = df_f['VALOR_PRODUTO'].sum()
mig = df_f[df_f['TIPO_VENDA'] == 'MIGRAÇÃO']['VALOR_PRODUTO'].sum()
novo = df_f[df_f['TIPO_VENDA'] == 'NOVO']['VALOR_PRODUTO'].sum()
regs = len(df_f)
regs_mig = len(df_f[df_f['TIPO_VENDA'] == 'MIGRAÇÃO'])
regs_nov = len(df_f[df_f['TIPO_VENDA'] == 'NOVO'])

mov_mig = df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum()
mov_nov = df_f[(df_f['TORRE'] == 'Móvel') & (df_f['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum()
fix_mig = df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum()
fix_nov = df_f[(df_f['TORRE'] == 'Fixa PJ') & (df_f['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum()
avanc = df_f[df_f['TORRE'] == 'Avançados']['VALOR_PRODUTO'].sum()
ti = df_f[df_f['TORRE'] == 'TI']['VALOR_PRODUTO'].sum()

st.markdown("### Resultados Gerais")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(card("TOTAL GERAL", f"R${total:,.2f}", f"{regs} registros"), unsafe_allow_html=True)
with c2:
    pct_mig = (mig/total*100) if total > 0 else 0
    st.markdown(card("TOTAL MIGRAÇÃO", f"R${mig:,.2f}", f"{regs_mig} reg | {pct_mig:.1f}%"), unsafe_allow_html=True)
with c3:
    pct_nov = (novo/total*100) if total > 0 else 0
    st.markdown(card("TOTAL NOVO", f"R${novo:,.2f}", f"{regs_nov} reg | {pct_nov:.1f}%", accent=True), unsafe_allow_html=True)
with c4:
    movel_total = mov_mig + mov_nov
    st.markdown(card("MÓVEL TOTAL", f"R${movel_total:,.2f}", f"Mig: R${mov_mig:,.0f} | Nov: R${mov_nov:,.0f}"), unsafe_allow_html=True)

st.markdown("### Por Torre e Tipo")
c5, c6, c7, c8, c9, c10 = st.columns(6)
with c5:
    st.markdown(card("MIG. MÓVEL", f"R${mov_mig:,.2f}", f"{len(df_f[(df_f['TORRE']=='Móvel') & (df_f['TIPO_VENDA']=='MIGRAÇÃO')])} reg"), unsafe_allow_html=True)
with c6:
    st.markdown(card("NOVO MÓVEL", f"R${mov_nov:,.2f}", f"{len(df_f[(df_f['TORRE']=='Móvel') & (df_f['TIPO_VENDA']=='NOVO')])} reg", accent=True), unsafe_allow_html=True)
with c7:
    st.markdown(card("MIG. FIXA", f"R${fix_mig:,.2f}", f"{len(df_f[(df_f['TORRE']=='Fixa PJ') & (df_f['TIPO_VENDA']=='MIGRAÇÃO')])} reg"), unsafe_allow_html=True)
with c8:
    st.markdown(card("NOVO FIXA", f"R${fix_nov:,.2f}", f"{len(df_f[(df_f['TORRE']=='Fixa PJ') & (df_f['TIPO_VENDA']=='NOVO')])} reg", accent=True), unsafe_allow_html=True)
with c9:
    st.markdown(card("AVANÇADOS", f"R${avanc:,.2f}", f"{len(df_f[df_f['TORRE']=='Avançados'])} reg"), unsafe_allow_html=True)
with c10:
    st.markdown(card("TI / DIGITAIS", f"R${ti:,.2f}", f"{len(df_f[df_f['TORRE']=='TI'])} reg"), unsafe_allow_html=True)

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Por Departamento")
    dept_data = df_f.groupby(['DEPARTAMENTO', 'TIPO_VENDA'])['VALOR_PRODUTO'].sum().reset_index()
    chart_dept = alt.Chart(dept_data).mark_bar().encode(
        x=alt.X('sum(VALOR_PRODUTO):Q', title='R$ Total'),
        y=alt.Y('DEPARTAMENTO:N', sort='-x', title=''),
        color=alt.Color('TIPO_VENDA:N', scale=alt.Scale(domain=['MIGRAÇÃO', 'NOVO'], range=[P, PA]), legend=alt.Legend(title=''))
    ).properties(height=400)
    st.altair_chart(chart_dept, use_container_width=True)

with col_right:
    st.markdown("### Por Torre")
    torre_data = df_f.groupby(['TORRE', 'TIPO_VENDA'])['VALOR_PRODUTO'].sum().reset_index()
    chart_torre = alt.Chart(torre_data).mark_bar().encode(
        x=alt.X('TORRE:N', title=''),
        y=alt.Y('sum(VALOR_PRODUTO):Q', title='R$ Total', stack=True),
        color=alt.Color('TIPO_VENDA:N', scale=alt.Scale(domain=['MIGRAÇÃO', 'NOVO'], range=[P, PA]), legend=alt.Legend(title='')),
        tooltip=['TORRE', 'TIPO_VENDA', alt.Tooltip('sum(VALOR_PRODUTO):Q', format=',.2f')]
    ).properties(height=400)
    st.altair_chart(chart_torre, use_container_width=True)

st.markdown("---")
st.markdown("### Ranking de Vendedores")

rank_data = []
for resp, grp in df_f.groupby('RESPONSAVEL'):
    rank_data.append({
        'RESPONSAVEL': resp,
        'QTD': len(grp),
        'MOV_MIG': grp[(grp['TORRE'] == 'Móvel') & (grp['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum(),
        'MOV_NOV': grp[(grp['TORRE'] == 'Móvel') & (grp['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum(),
        'FIX_MIG': grp[(grp['TORRE'] == 'Fixa PJ') & (grp['TIPO_VENDA'] == 'MIGRAÇÃO')]['VALOR_PRODUTO'].sum(),
        'FIX_NOV': grp[(grp['TORRE'] == 'Fixa PJ') & (grp['TIPO_VENDA'] == 'NOVO')]['VALOR_PRODUTO'].sum(),
        'TOTAL': grp['VALOR_PRODUTO'].sum(),
        'DEPARTAMENTO': DEPT_MAP.get(resp, 'Outros')
    })
rank = pd.DataFrame(rank_data).sort_values('TOTAL', ascending=False).reset_index(drop=True)

top15 = rank.head(15).copy()
chart_rank = alt.Chart(top15).mark_bar().encode(
    x=alt.X('RESPONSAVEL:N', sort=alt.EncodingSortField(field='TOTAL', order='descending'), title=''),
    y=alt.Y('TOTAL:Q', title='R$ Total'),
    color=alt.Color('DEPARTAMENTO:N', scale=alt.Scale(scheme='purples'), legend=alt.Legend(title='Depto')),
    tooltip=['RESPONSAVEL', 'DEPARTAMENTO', alt.Tooltip('TOTAL:Q', format=',.2f')]
).properties(height=400)
st.altair_chart(chart_rank, use_container_width=True)

st.markdown("### Tabela Detalhada")
display_rank = rank.copy()
for col in ['MOV_MIG', 'MOV_NOV', 'FIX_MIG', 'FIX_NOV', 'TOTAL']:
    display_rank[col] = display_rank[col].apply(lambda x: f"R${x:,.2f}")
st.dataframe(display_rank, use_container_width=True, height=500)
