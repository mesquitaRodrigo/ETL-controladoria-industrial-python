import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Dashboard de Controladoria Industrial - versão inicial

# =====================================================
# 1️⃣ CARGA DOS DADOS
# =====================================================

fato_custos = pd.read_csv(
    "/home/rodrigo/controladoria-industrial/data/processed/fato_custos_tratado.csv"
)
producao = pd.read_csv(
    "/home/rodrigo/controladoria-industrial/data/processed/producao_tratada.csv"
)
produtos = pd.read_csv(
    "/home/rodrigo/controladoria-industrial/data/raw/produtos_raw.csv"
)

fato_custos["ano_mes"] = fato_custos["ano_mes"].astype(str)

# =====================================================
# 2️⃣ BASE ANALÍTICA DE CONTROLADORIA
# =====================================================

# Produção agregada
producao["ano_mes"] = pd.to_datetime(producao["data"]).dt.to_period("M").astype(str)

producao_ag = (
    producao
    .groupby(["ano_mes", "centro_custo", "produto"])["quantidade_produzida"]
    .sum()
    .reset_index()
)

# Custos produtivos
custos_produtivos = fato_custos[fato_custos["tipo"] == "Produtivo"]

custos_prod_ag = (
    custos_produtivos
    .groupby(["ano_mes", "centro_custo"])["valor"]
    .sum()
    .reset_index()
    .rename(columns={"valor": "custo_produtivo_total"})
)

# Base custo unitário
base_custo = producao_ag.merge(
    custos_prod_ag,
    on=["ano_mes", "centro_custo"],
    how="left"
)

base_custo["custo_unitario_real"] = (
    base_custo["custo_produtivo_total"] /
    base_custo["quantidade_produzida"]
)

base_custo = base_custo.merge(
    produtos[["produto", "custo_padrao_unitario"]],
    on="produto",
    how="left"
)

base_custo["desvio_abs"] = (
    base_custo["custo_unitario_real"] -
    base_custo["custo_padrao_unitario"]
)

base_custo["desvio_pct"] = (
    base_custo["desvio_abs"] /
    base_custo["custo_padrao_unitario"]
) * 100

# =====================================================
# 3️⃣ FILTROS
# =====================================================

lista_meses = sorted(fato_custos["ano_mes"].unique())
lista_cc = sorted(fato_custos["centro_custo"].unique())

# =====================================================
# 4️⃣ APP E LAYOUT
# =====================================================

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Dashboard Executivo – Controladoria Industrial"),

    html.Div([
        dcc.Dropdown(
            id="filtro_mes",
            options=[{"label": m, "value": m} for m in lista_meses],
            value=lista_meses,
            multi=True,
            placeholder="Período"
        ),
        dcc.Dropdown(
            id="filtro_cc",
            options=[{"label": cc, "value": cc} for cc in lista_cc],
            value=lista_cc,
            multi=True,
            placeholder="Centro de Custo"
        )
    ], style={"display": "flex", "gap": "20px"}),

    html.Hr(),

    html.Div([
        html.Div([html.H4("Custo Total"), html.H2(id="kpi_custo_total")]),
        html.Div([html.H4("% Custos Indiretos"), html.H2(id="kpi_indireto")]),
        html.Div([
            html.H4("Desvio Médio Ponderado"),
            html.H2(id="kpi_desvio_pond")
        ]),
        html.Div([
            html.H4("Impacto Financeiro do Desvio"),
            html.H2(id="kpi_impacto_fin")
        ])
    ], style={"display": "flex", "gap": "40px"}),

    dcc.Graph(id="graf_evolucao"),
    dcc.Graph(id="graf_tipo"),
    dcc.Graph(id="graf_cc"),
    dcc.Graph(id="graf_real_padrao"),
    dcc.Graph(id="graf_ranking_produto")

])

# =====================================================
# 5️⃣ CALLBACK (CORAÇÃO DO DASHBOARD)
# =====================================================

@app.callback(
    [
        Output("kpi_custo_total", "children"),
        Output("kpi_indireto", "children"),
        Output("kpi_desvio_pond", "children"),
        Output("kpi_desvio_pond", "style"),
        Output("kpi_impacto_fin", "children"),
        Output("graf_evolucao", "figure"),
        Output("graf_tipo", "figure"),
        Output("graf_cc", "figure"),
        Output("graf_real_padrao", "figure"),
        Output("graf_ranking_produto", "figure"),
    ],
    [
        Input("filtro_mes", "value"),
        Input("filtro_cc", "value"),
    ]
)
def atualizar_dashboard(meses, centros):

    # -------- Base de custos
    df = fato_custos[
        fato_custos["ano_mes"].isin(meses) &
        fato_custos["centro_custo"].isin(centros)
    ]

    custo_total = df["valor"].sum()

    perc_indireto = (
        df[df["tipo_custo"] == "INDIRETO"]["valor"].sum() / custo_total
        if custo_total > 0 else 0
    ) * 100

    # -------- Gráficos principais
    fig_evolucao = px.line(
        df.groupby("ano_mes")["valor"].sum().reset_index(),
        x="ano_mes", y="valor",
        title="Evolução Mensal dos Custos"
    )

    fig_tipo = px.pie(
        df.groupby("tipo_custo")["valor"].sum().reset_index(),
        names="tipo_custo", values="valor"
    )

    fig_cc = px.bar(
        df.groupby("centro_custo")["valor"].sum()
          .reset_index().sort_values("valor", ascending=False).head(10),
        x="centro_custo", y="valor",
        title="Top 10 Centros de Custo"
    )

    # -------- Base analítica filtrada
    base_filtrada = base_custo[
        base_custo["ano_mes"].isin(meses) &
        base_custo["centro_custo"].isin(centros)
    ]

    impacto_financeiro = 0
    desvio_medio_pond = 0
    estilo = {"fontWeight": "bold"}

    if not base_filtrada.empty:
        numerador = (base_filtrada["desvio_abs"] *
                     base_filtrada["quantidade_produzida"]).sum()

        denominador = (base_filtrada["custo_padrao_unitario"] *
                       base_filtrada["quantidade_produzida"]).sum()

        desvio_medio_pond = numerador / denominador * 100 if denominador > 0 else 0
        impacto_financeiro = numerador

        estilo["color"] = (
            "green" if desvio_medio_pond < 0 else
            "orange" if desvio_medio_pond <= 5 else
            "red"
        )

    fig_real_padrao = px.scatter(
        base_filtrada,
        x="custo_padrao_unitario",
        y="custo_unitario_real",
        color="desvio_pct",
        title="Custo Unitário Real x Padrão"
    )

    ranking_produto = (
        base_filtrada
        .groupby("produto")
        .apply(lambda x: (x["desvio_abs"] * x["quantidade_produzida"]).sum())
        .reset_index(name="impacto_financeiro")
        .sort_values("impacto_financeiro", ascending=False)
    )

    fig_ranking_produto = px.bar(
        ranking_produto.head(10),
        x="impacto_financeiro",
        y="produto",
        orientation="h",
        title="Ranking de Impacto Financeiro por Produto"
    )

    return (
        f"R$ {custo_total:,.2f}",
        f"{perc_indireto:.2f}%",
        f"{desvio_medio_pond:.2f}%",
        estilo,
        f"R$ {impacto_financeiro:,.2f}",
        fig_evolucao,
        fig_tipo,
        fig_cc,
        fig_real_padrao,
        fig_ranking_produto
    )

# =====================================================
# 6️⃣ RUN
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
