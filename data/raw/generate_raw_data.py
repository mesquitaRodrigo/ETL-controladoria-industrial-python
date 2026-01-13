import pandas as pd # type: ignore
import numpy as np # type: ignore
import random
from datetime import datetime, timedelta

# -----------------------------
# Configurações gerais
# -----------------------------
np.random.seed(42)
random.seed(42)

DATA_INICIO = datetime(2023, 1, 1)
DATA_FIM = datetime(2024, 12, 31)

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# -----------------------------
# Centros de Custo
# -----------------------------
centros_custo = [
    ("CC100", "Produção Linha A", "Carlos Silva", "Produtivo"),
    ("CC200", "Produção Linha B", "Ana Souza", "Produtivo"),
    ("CC300", "Manutenção", "Marcos Lima", "Produtivo"),
    ("CC400", "Logística", "Fernanda Rocha", "Produtivo"),
    ("CC500", "Administrativo", "Juliana Alves", "Administrativo"),
]

df_centros = pd.DataFrame(
    centros_custo,
    columns=["centro_custo", "descricao", "gestor", "tipo"]
)

# -----------------------------
# Produtos
# -----------------------------
produtos = [
    ("PROD_A", "Produto Acabado", 25.0),
    ("PROD_B", "Produto Acabado", 32.5),
    ("PROD_C", "Produto Acabado", 18.7),
    ("PROD_D", "Semiacabado", 12.3),
    ("PROD_E", "Semiacabado", 9.8),
]

df_produtos = pd.DataFrame(
    produtos,
    columns=["produto", "categoria_produto", "custo_padrao_unitario"]
)

# -----------------------------
# Produção (≈300 linhas)
# -----------------------------
producao_data = []

for _ in range(300):
    produto = random.choice(df_produtos["produto"])
    centro = random.choice(["CC100", "CC200"])
    producao_data.append({
        "data": random_date(DATA_INICIO, DATA_FIM),
        "produto": produto,
        "linha_producao": random.choice(["Linha 1", "Linha 2"]),
        "quantidade_produzida": random.randint(50, 500),
        "horas_maquina": round(random.uniform(5, 40), 2),
        "centro_custo": centro
    })

df_producao = pd.DataFrame(producao_data)

# -----------------------------
# Lançamentos de Custos (≈800 linhas)
# -----------------------------
categorias = [
    "Materia Prima", "Energia", "Mao de Obra",
    "Manutencao", "Frete", "Servicos Terceiros"
]

fornecedores = [
    "Fornecedor A", "Fornecedor B", "Fornecedor C",
    "FORN-XYZ", "Serviços LTDA", "Energia SA"
]

custos_data = []

for i in range(1, 801):
    tipo_custo = random.choice(["Direto", "Indireto"])
    categoria = random.choice(categorias)

    valor = round(random.uniform(100, 20000), 2)

    # Introduz erro proposital
    if random.random() < 0.03:
        valor *= -1

    custos_data.append({
        "id_lancamento": i,
        "data": random_date(DATA_INICIO, DATA_FIM),
        "centro_custo": random.choice(df_centros["centro_custo"]),
        "tipo_custo": tipo_custo,
        "categoria": categoria,
        "valor": valor,
        "fornecedor": random.choice(fornecedores),
        "ordem_producao": random.choice(
            [None, f"OP{random.randint(1000, 9999)}"]
        )
    })

df_custos = pd.DataFrame(custos_data)

# -----------------------------
# Ajustes finais (dados sujos)
# -----------------------------
df_custos["categoria"] = df_custos["categoria"].str.lower()
df_custos.loc[df_custos.sample(frac=0.05).index, "centro_custo"] = None

# -----------------------------
# Salvando CSVs
# -----------------------------
df_centros.to_csv("centros_custo_raw.csv", index=False)
df_produtos.to_csv("produtos_raw.csv", index=False)
df_producao.to_csv("producao_raw.csv", index=False)
df_custos.to_csv("custos_lancamentos_raw.csv", index=False)

print("✅ Dados brutos gerados com sucesso!")
print(f"Centros de custo: {len(df_centros)}")
print(f"Produtos: {len(df_produtos)}")
print(f"Produção: {len(df_producao)}")
print(f"Lançamentos de custos: {len(df_custos)}")
print(f"Total de linhas: {len(df_centros) + len(df_produtos) + len(df_producao) + len(df_custos)}")
