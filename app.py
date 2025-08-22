import streamlit as st
from datetime import datetime, date

# -------------------------
# Configurações iniciais
# -------------------------
st.set_page_config(page_title="Central Inteligente", layout="wide")

import streamlit as st

def show_logo():
    st.markdown(
        """
        <style>
        .logo-container {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 100;
        }
        .logo-container img {
            width: 250px;
        }
        </style>
        <div class="logo-container">
            <img src="https://raw.githubusercontent.com/gledison-bomfim/streamlit-project/master/Logo-Versao-Preferencial.png">
        </div>
        """,
        unsafe_allow_html=True
    )


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
    show_logo()
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
    st.warning("Se for cliente, acesse o app Super Gestão:")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("Google Play"):
            st.markdown(
                '<meta http-equiv="refresh" content="0;url=https://play.google.com/store/apps/details?id=com.supergasbras.superapp&hl=pt_BR">',
                unsafe_allow_html=True
            )
    
    with col4:
        if st.button("App Store"):
            st.markdown(
                '<meta http-equiv="refresh" content="0;url=https://apps.apple.com/br/app/super-gest%C3%A3o-supergasbras/id1556506493">',
                unsafe_allow_html=True
            )


def checkin_page():
    show_logo()
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
    data = st.date_input("Data", value=hoje)
    hora = st.time_input("Hora", value=datetime.now().time())

    # Localização automática
    loc = get_location()
    st.info(f"Localização detectada: Latitude {loc['latitude']}, Longitude {loc['longitude']}")

    # Upload da foto
    st.file_uploader(
        "Upload da foto da central (externa, portão aberto, visão dos tanques)",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("✅ Confirmar Check-in"):
        st.session_state.page = "equipamentos"


def equipamentos_page():
    show_logo()
    st.title("Relação de Equipamentos")
    st.caption(f"Cliente: {cliente} | Central: {central}")

    for i, eq in enumerate(EQUIPAMENTOS):
        with st.expander(f"EQUIPAMENTO: {eq['nome']} | QUANTIDADE: {eq['quantidade']}"):
            st.write(f"Fabricante: {eq['fabricante']}")
            st.write(f"Data de Fabricação: {eq['data_fabricacao']}")
            st.write(f"Nº Série: {eq['n_serie']}")
            st.write(f"Nº Patrimônio: {eq['n_patrimonio']}")

            divergencia = st.multiselect(
                "Reportar divergência:",
                ["Quantidade", "Número de Série", "Fabricante", "Nº Patrimônio"],
                key=f"div_{i}"  # 🔑 Corrige erro de duplicidade
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


