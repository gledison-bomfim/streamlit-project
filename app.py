import subprocess
import sys

try:
    import plotly
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    import plotly

# app.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# Configuração inicial da página
st.set_page_config(page_title="DataApp - Otimização de Compras de Gás", layout="wide")

# ---- Header ----
st.title("📊 DataApp - Otimização de Compras de Gás")
st.caption(f"Última atualização: {datetime.now().strftime('%H:%M')}")

tab_dashboard, tab_simulator = st.tabs(["Dashboard", "Simulador"])

# ---- Funções auxiliares ----
def generate_random(min_val, max_val, decimals=0):
    return round(random.uniform(min_val, max_val), decimals)

# ---- Dashboard ----
with tab_dashboard:
    st.subheader("Dashboard de Indicadores")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Consumo Total (m³)", f"{generate_random(1200000,1300000):,}".replace(",", "."))
    col2.metric("Preço Médio (R$/m³)", f"{generate_random(2.30,2.60,2)}")
    col3.metric("Margem Operacional (%)", f"{generate_random(15,22,1)}")
    col4.metric("Nível de Estoque", f"{generate_random(65,85)}%")

    # Consumo por Polo
    polos = ["Polo Norte", "Polo Sul", "Polo Leste", "Polo Oeste"]
    consumo = [320000, 285000, 410000, 230000]
    fig_consumo = px.bar(x=polos, y=consumo, labels={"x": "Polo", "y": "Consumo (m³)"},
                         color=polos, title="Consumo por Polo")
    st.plotly_chart(fig_consumo, use_container_width=True)

    # Tendência de Preços
    dates = [datetime.now() - timedelta(days=i) for i in range(30)] + [datetime.now() + timedelta(days=i) for i in range(1,16)]
    historico = [generate_random(2.2,2.8,2) for _ in range(30)] + [None]*15
    previsao = [None]*30 + [generate_random(2.3,2.9,2) for _ in range(15)]
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=dates, y=historico, mode="lines+markers", name="Preço Real"))
    fig_price.add_trace(go.Scatter(x=dates, y=previsao, mode="lines+markers", name="Previsão", line=dict(dash="dash")))
    fig_price.update_layout(title="Tendência de Preços")
    st.plotly_chart(fig_price, use_container_width=True)

# ---- Simulador ----
with tab_simulator:
    st.subheader("Simulador de Cenários")
    st.write("Analise diferentes cenários para tomar a melhor decisão de compra")

    col1, col2 = st.columns([1,2])
    with col1:
        preco_atual = st.number_input("Preço Atual do Leilão (R$/m³)", min_value=0.0, step=0.01, value=2.45)
        quantidade = st.number_input("Quantidade Desejada (m³)", min_value=0, step=1000, value=100000)
        preco_futuro = st.number_input("Projeção de Preço Futuro (R$/m³)", min_value=0.0, step=0.01, value=2.60)
        estoque_atual = st.number_input("Estoque Atual (m³)", min_value=0, step=1000, value=500000)
        horizonte = st.selectbox("Horizonte de Tempo (dias)", [30,60,90])

        if st.button("▶ Simular Cenários"):
            custo_agora = preco_atual * quantidade
            custo_futuro = preco_futuro * quantidade
            economia = custo_agora - custo_futuro
            risco = max(0, min(100, (1 - estoque_atual / (quantidade*2)) * 100))

            if economia > 0 and risco < 30:
                recomendacao = "Esperar"
                cor = "🟡"
            elif economia < 0 or risco > 50:
                recomendacao = "Comprar Agora"
                cor = "🟢"
            else:
                recomendacao = "Neutra"
                cor = "⚪"

            with col2:
                st.success(f"### {cor} Recomendação: {recomendacao}")
                st.write(f"**Cenário A (Comprar Agora)**\n- Custo: R$ {custo_agora:,.2f}\n- Cobertura: {int((estoque_atual+quantidade)/(quantidade*(30/horizonte)))} dias")
                st.write(f"**Cenário B (Esperar)**\n- Custo: R$ {custo_futuro:,.2f}\n- Economia Potencial: R$ {economia:,.2f}\n- Risco de Falta: {risco:.1f}%")

