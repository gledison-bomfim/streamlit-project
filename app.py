import streamlit as st
from datetime import datetime, date, time

# -------------------------
# Configurações iniciais
# -------------------------
st.set_page_config(page_title="Central Inteligente", layout="wide")

# Recuperar parâmetros do QR Code (cliente e central)
query_params = st.query_params
cliente = query_params.get("cliente", "Cliente Exemplo")
central = query_params.get("central", "Central Exemplo")

# Sessão para armazenar navegação
if "page" not in st.session_state:
    st.session_state.page = "home"

# Mock de localização automática (simulação)
def get_location():
    return {"latitude": -19.9227, "longitude": -43.9451}  # Exemplo fixo (Belo Horizonte)

# Mock de equipamentos
EQUIPAMENTOS = [
    {
        "nome": "Tanque P190",
        "quantidade": 2,
        "fabricante": "ACME",
        "data_fabricacao": "2020-01-01",
        "n_serie": "12345",
        "n_patrimonio": "P190-001"
    },
    {
        "nome": "Reguladores de Pressão",
        "quantidade": 4,
        "fabricante": "Regula",
        "data_fabricacao": "2021-03-15",
        "n_serie": "67890",
        "n_patrimonio": "REG-004"
    },
]

# -------------------------
# Funções de Páginas
# -------------------------

def home_page():
    st.title("Central Inteligente")
    st.subheader(f"Central: {central}")
    st.caption(f"Cliente: {cliente}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📍 Fazer Check-in"):
            st.session_state.page = "checkin"
    with col2:
        st.button("ℹ️ Ver informações do cliente")

    st.markdown("---")
    st.warning("Se for cliente acesse o app Super Gestão:")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("[📱 Google Play](https://play.google.com/store/apps/details?id=com.supergasbras.superapp&hl=pt_BR)")
    with col4:
        st.markdown("[🍎 App Store](https://apps.apple.com/br/app/super-gest%C3%A3o-supergasbras/id1556506493)")


def checkin_page():
    st.title("Check-in")
    st.caption(f"Cliente: {cliente} | Central: {central}")

    # Motivo da visita
    motivo = st.selectbox(
        "Selecione o motivo da visita:",
        [
            "Abastecimento",
            "Visita Relacionamento",
            "Assistência Técnica",
            "Manutenção Preventiva",
            "Visita SPOT",
            "NR13/Requalificação"
        ]
    )

    # Data e hora
    hoje = date.today()
    agora = datetime.now().time()
    data = st.date_input("Data", value=hoje)
    hora = st.time_input("Hora", value=agora)

    # Localização automática
    loc = get_location()
    st.info(f"Localização detectada: Latitude {loc['latitude']}, Longitude {loc['longitude']}")

    # Upload da foto
    st.file_uploader(
        "Upload da foto da central (externa, portão aberto, visão dos tanques)",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("✅ Confirmar Check-in"):
        # Salvar check-in temporário (sem histórico persistente)
        st.session_state.page = "equipamentos"


def equipamentos_page():
    st.title("Relação de Equipamentos")
    st.caption(f"Cliente: {cliente} | Central: {central}")

    for eq in EQUIPAMENTOS:
        with st.expander(f"EQUIPAMENTO: {eq['nome']} | QUANTIDADE: {eq['quantidade']}"):
            st.write(f"Fabricante: {eq['fabricante']}")
            st.write(f"Data de Fabricação: {eq['data_fabricacao']}")
            st.write(f"Nº Série: {eq['n_serie']}")
            st.write(f"Nº Patrimônio: {eq['n_patrimonio']}")

            divergencia = st.multiselect(
                "Reportar divergência:",
                ["Quantidade", "Número de Série", "Fabricante", "Nº Patrimônio"]
            )
            if divergencia:
                st.error(f"Divergências reportadas: {', '.join(divergencia)}")

# -------------------------
# Roteamento
# -------------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "checkin":
    checkin_page()
elif st.session_state.page == "equipamentos":
    equipamentos_page()
