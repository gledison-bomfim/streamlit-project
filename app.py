import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import io
import base64
import json

# -----------------------------
# Configurações básicas
# -----------------------------
st.set_page_config(page_title="Central Inteligente", page_icon="📍", layout="centered")

# Estilos (enxuto, mobile-first)
st.markdown(
    """
    <style>
      .central-badge { 
          background: #f0f4ff; 
          color: #1f2d5a; 
          padding: .35rem .6rem; 
          border-radius: 999px; 
          font-weight: 700; 
          display: inline-block;
      }
      .client-name { font-weight: 600; opacity: .9; }
      .footer { opacity: .6; font-size: .8rem; margin-top: 2rem; }
      .small { font-size: .9rem; }
      .ghost { opacity: .7; }
      .tight > div[data-testid="stHorizontalBlock"] { gap: .4rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Estado inicial
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"  # home | checkin | equipamentos | cliente

if "checkins" not in st.session_state:
    st.session_state.checkins = []  # lista de dicts

if "divergencias" not in st.session_state:
    st.session_state.divergencias = []  # lista de dicts

# -----------------------------
# Leitura de parâmetros da URL (ex.: ?cliente=ACME&central=Central%20Betim)
# -----------------------------
params = st.query_params
cliente = params.get("cliente", ["Cliente"])
central = params.get("central", ["Central"])
# st.query_params retorna str quando há um valor; garantir string
cliente = cliente[0] if isinstance(cliente, list) else cliente
central = central[0] if isinstance(central, list) else central

# Guardar no estado
st.session_state["cliente_nome"] = cliente
st.session_state["central_nome"] = central

# -----------------------------
# Header persistente com Cliente e Central
# -----------------------------
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown(f"<div class='client-name'>👤 Cliente: <b>{st.session_state['cliente_nome']}</b></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align:right'>🏭 Central: <span class='central-badge'>{st.session_state['central_nome']}</span></div>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# Dados de exemplo (Equipamentos da Central)
# Em produção, substitua por chamada à sua base (ex.: Databricks/Lakehouse)
# -----------------------------
EQUIPAMENTOS_PADRAO = [
    "Tanque de armazenamento de GLP",
    "Reguladores de Pressão",
    "Válvula de Bloqueio",
    "Válvula de Segurança",
    "Telemetria",
]

amostra_equipamentos = [
    {
        "equipamento": "Tanque de armazenamento de GLP",
        "modelo": "P190",
        "quantidade": 2,
        "fabricante": "ACME Tanques",
        "data_fabricacao": "2022-05-10",
        "num_serie": "P190-22-000345",
        "num_patrimonio": "PAT-001",
    },
    {
        "equipamento": "Reguladores de Pressão",
        "modelo": "RX-300",
        "quantidade": 3,
        "fabricante": "RegulaTech",
        "data_fabricacao": "2021-11-02",
        "num_serie": "RX300-21-888",
        "num_patrimonio": "PAT-002",
    },
    {
        "equipamento": "Válvula de Bloqueio",
        "modelo": "VB-12",
        "quantidade": 4,
        "fabricante": "SafeFlow",
        "data_fabricacao": "2020-03-18",
        "num_serie": "VB12-20-1212",
        "num_patrimonio": "PAT-003",
    },
    {
        "equipamento": "Válvula de Segurança",
        "modelo": "VS-8",
        "quantidade": 2,
        "fabricante": "SafeFlow",
        "data_fabricacao": "2019-09-01",
        "num_serie": "VS8-19-9090",
        "num_patrimonio": "PAT-004",
    },
    {
        "equipamento": "Telemetria",
        "modelo": "Tel-GLP-100",
        "quantidade": 1,
        "fabricante": "SmartSense",
        "data_fabricacao": "2023-07-22",
        "num_serie": "TEL100-23-555",
        "num_patrimonio": "PAT-005",
    },
]

# -----------------------------
# Funções auxiliares
# -----------------------------
MOTIVOS = [
    "Abastecimento",
    "Visita Relacionamento",
    "Assistência Técnica",
    "Manutenção Preventiva",
    "Visita SPOT",
    "NR13/Requalificação",
]

DIVERGENCIAS_OPCOES = [
    "quantidade",
    "numero de serie",
    "fabricante",
    "nº patrimônio",
]

def blob_to_b64(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")

# -----------------------------
# Navegação (por botões)
# -----------------------------
if st.session_state.page == "home":
    st.header("Central Inteligente")

    st.markdown(
        """
        ### Bem-vindo 👋
        Esta aplicação suporta o atendimento **no local** via leitura de QR Code na central. 
        Use os botões abaixo para prosseguir.
        """
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Fazer Check-in", use_container_width=True):
            st.session_state.page = "checkin"
            st.rerun()
    with c2:
        if st.button("ℹ️ Ver informações do cliente", use_container_width=True):
            st.session_state.page = "cliente"
            st.rerun()

    st.info(
        "Se for cliente, acesse o app **Super Gestão**:")
    st.link_button("Abrir App Super Gestão", "https://example.com/super-gestao", use_container_width=True)

    st.caption("Dica: passe parâmetros na URL, ex.: `?cliente=ACME&central=Central%20Betim`.")

elif st.session_state.page == "checkin":
    st.subheader("Check-in na Central")

    with st.container(border=True):
        motivo = st.selectbox("Motivo da visita", MOTIVOS, index=None, placeholder="Selecione um motivo")

        colA, colB = st.columns(2)
        with colA:
            data_sel = st.date_input("Data", value=date.today())
            hora_sel = st.time_input("Hora", value=datetime.now().time())
            dt = datetime.combine(data_sel, hora_sel)
        with colB:
            st.markdown("**Localização (GPS)**")
            manual_lat = st.text_input("Latitude (opcional)", placeholder="-19.9876")
            manual_lon = st.text_input("Longitude (opcional)", placeholder="-44.0123")
            st.caption("Se a localização automática falhar, preencha latitude/longitude manualmente.")

        st.markdown("---")
        st.markdown("**Foto da central**")
        st.info(
            "Tire uma **foto externa** da central **com o portão aberto**, mostrando os **tanques**. ⚠️ **Não entre na central para tirar a foto**.")
        instrucoes = st.text_area("Observações/instruções adicionais para a foto (opcional)", placeholder="Ex.: tirar foto do lado esquerdo, com foco nos tanques")
        foto = st.file_uploader("Enviar foto", type=["png", "jpg", "jpeg"], accept_multiple_files=False)

        # Salvar Check-in
        salvar = st.button("💾 Salvar Check-in", use_container_width=True, type="primary")

        if salvar:
            latlon = None
            if manual_lat and manual_lon:
                latlon = {"lat": manual_lat, "lon": manual_lon}

            foto_b64 = None
            foto_name = None
            if foto is not None:
                foto_bytes = foto.getvalue()
                foto_b64 = blob_to_b64(foto_bytes)
                foto_name = foto.name

            registro = {
                "cliente": st.session_state["cliente_nome"],
                "central": st.session_state["central_nome"],
                "motivo": motivo,
                "datahora": dt.isoformat(),
                "localizacao": latlon,
                "instrucoes_foto": instrucoes,
                "foto_nome": foto_name,
                "foto_b64": foto_b64,
            }
            st.session_state.checkins.append(registro)
            st.success("Check-in salvo!")

    if st.session_state.checkins:
        st.markdown("### Últimos check-ins")
        df = pd.json_normalize(st.session_state.checkins)
        st.dataframe(df.drop(columns=[c for c in df.columns if c.endswith("_b64")]), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with c2:
        if st.button("📋 Ver Equipamentos", use_container_width=True):
            st.session_state.page = "equipamentos"
            st.rerun()

elif st.session_state.page == "equipamentos":
    st.subheader("Equipamentos da Central (visão compacta)")

    for item in amostra_equipamentos:
        with st.container(border=True):
            c1, c2 = st.columns([2, 1])
            with c1:
                titulo = f"**EQUIPAMENTO:** {item['equipamento']}"
                if item.get("modelo"):
                    titulo += f" • **Modelo:** {item['modelo']}"
                st.markdown(titulo)
            with c2:
                st.markdown(f"**QUANTIDADE:** {item['quantidade']}")

            with st.expander("Expandir detalhes"):
                colA, colB = st.columns(2)
                with colA:
                    st.write("Fabricante:", item["fabricante"])
                    st.write("Data de fabricação:", item["data_fabricacao"])
                with colB:
                    st.write("Nº Série:", item["num_serie"])
                    st.write("Nº Patrimônio:", item["num_patrimonio"])

            with st.popover("🚩 Reportar divergência"):
                diverg = st.multiselect(
                    "O que está divergente?", DIVERGENCIAS_OPCOES, placeholder="Selecione um ou mais itens"
                )
                obs = st.text_area("Observações (opcional)")
                if st.button("Enviar relatório", use_container_width=True):
                    registro_div = {
                        "cliente": st.session_state["cliente_nome"],
                        "central": st.session_state["central_nome"],
                        "equipamento": item["equipamento"],
                        "modelo": item.get("modelo"),
                        "divergencias": diverg,
                        "observacoes": obs,
                        "datahora": datetime.now().isoformat(),
                    }
                    st.session_state.divergencias.append(registro_div)
                    st.success("Divergência registrada!")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with c2:
        if st.button("✅ Ir para Check-in", use_container_width=True):
            st.session_state.page = "checkin"
            st.rerun()

    if st.session_state.divergencias:
        st.markdown("### Divergências reportadas")
        df_div = pd.json_normalize(st.session_state.divergencias)
        st.dataframe(df_div, use_container_width=True)

elif st.session_state.page == "cliente":
    st.subheader("Informações do cliente")

    with st.container(border=True):
        st.write("Nome:", st.session_state["cliente_nome"])
        st.write("Central:", st.session_state["central_nome"])
        st.write("CNPJ:", "00.000.000/0000-00")
        st.write("Endereço:", "Rua Exemplo, 123 - Centro")
        st.write("Contato:", "(31) 99999-0000")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Voltar", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with c2:
        if st.button("📋 Ver Equipamentos", use_container_width=True):
            st.session_state.page = "equipamentos"
            st.rerun()

# -----------------------------
# Rodapé
# -----------------------------
st.markdown(
    f"<div class='footer'>Central Inteligente • Cliente: <b>{st.session_state['cliente_nome']}</b> • Central: <b>{st.session_state['central_nome']}</b></div>",
    unsafe_allow_html=True,
)
