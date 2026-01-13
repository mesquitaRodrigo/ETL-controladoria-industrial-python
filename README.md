# 📊 Dashboard de Controladoria Industrial

Projeto de análise de custos industriais com foco em **controladoria**, integrando dados de produção, custos produtivos e custos padrão para geração de **KPIs executivos** e **dashboard interativo** em Python.

---

## 🎯 Objetivo do Projeto

Simular um cenário real de controladoria industrial para:

- Apurar custo unitário real
- Comparar com custo padrão
- Medir desvios operacionais
- Avaliar impacto financeiro
- Apoiar tomada de decisão gerencial

---

## 🏭 Contexto de Negócio

- Indústria com múltiplos centros de custo
- Produção mensal por produto
- Custos diretos e indiretos
- Análise de eficiência produtiva

---

## 🔧 Tecnologias Utilizadas

- Python
- Pandas
- Plotly / Dash
- ETL estruturado
- Visualização interativa

---

## 📐 Arquitetura do Projeto


---

## 📊 Principais KPIs

- Custo Total
- % Custos Indiretos
- Desvio Médio Ponderado (%)
- Impacto Financeiro do Desvio (R$)
- Ranking de Produtos por Impacto Financeiro

---

## 📈 Visualizações

- Evolução mensal de custos
- Distribuição Direto x Indireto
- Top centros de custo
- Custo unitário real x padrão
- Ranking de impacto financeiro por produto

---

## ▶️ Como Executar o Projeto

```bash
git clone https://github.com/seu-usuario/controladoria-industrial.git
cd controladoria-industrial
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python dashboard/dashboard.py

http://127.0.0.1:8050
