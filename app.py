import streamlit as st
from datetime import datetime, date

# -------------------------
# Configurações iniciais
# -------------------------
st.set_page_config(page_title="Central Inteligente", layout="wide")

# Recuperar parâmetros do QR Code (cliente e central)
query_params = st.query_params
cliente = query_params.get("cliente", "JC PIZZARIA LTDA")
central = query_params.get("central", "Central Padrão")

# Sessão para armazenar navegação
if "page" not in st.session_state:
    st.session_state.page = "home"

# Mock de localização automática
def get_location():
    return {"latitude": -19.9227, "longitude": -43.9451}  # Exemplo fixo

# Mock de equipamentos
EQUIPAMENTOS = [
    {"nome": "Tanque P190","quantidade": 2,"fabricante": "ACME","data_fabricacao": "2020-01-01","n_serie": "12345","n_patrimonio": "P190-001"},
    {"nome": "Reguladores de Pressão","quantidade": 4,"fabricante": "Regula","data_fabricacao": "2021-03-15","n_serie": "67890","n_patrimonio": "REG-004"},
]

# -------------------------
# Cabeçalho
# -------------------------
def show_header():
    # Logo centralizada mais acima
    st.markdown(
        """
        <div style='text-align:center; margin-top:-20px;'>
            <img src='https://raw.githubusercontent.com/gledison-bomfim/streamlit-project/master/Logo-Versao-Preferencial.png' width='120'>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Título e informações centralizados
    st.markdown("<h1 style='text-align: center; margin-bottom:5px;'>Central Inteligente</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; margin:0;'>Central: {central}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; margin-top:0;'>Cliente: {cliente}</h4>", unsafe_allow_html=True)

# -------------------------
# Páginas
# -------------------------

def home_page():
    show_header()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📍 Fazer Check-in"):
            st.session_state.page = "checkin"
    with col2:
        st.button("ℹ️ Ver informações do cliente")

    st.markdown("---")
    st.warning("Se for cliente, acesse o app Super Gestão:")

    # Botões responsivos lado a lado
    col3, col4 = st.columns([1, 1])
    with col3:
        st.link_button("Google Play", "https://play.google.com/store/apps/details?id=com.supergasbras.superapp&hl=pt_BR")
    with col4:
        st.link_button("App Store", "https://apps.apple.com/br/app/super-gest%C3%A3o-supergasbras/id1556506493")

def checkin_page():
    show_header()

    motivo = st.selectbox(
        "Selecione o motivo da visita:",
        ["Abastecimento","Visita Relacionamento","Assistência Técnica","Manutenção Preventiva","Visita SPOT","NR13/Requalificação"]
    )

    # Data fixa e não editável
    hoje = date.today().strftime("%d/%m/%Y")
    st.text_input("Data", value=hoje, disabled=True)

    # Hora fixa e não editável
    hora_atual = datetime.now().strftime("%H:%M")
    st.text_input("Hora", value=hora_atual, disabled=True)

    # Localização automática
    loc = get_location()
    st.info(f"Localização detectada: Latitude {loc['latitude']}, Longitude {loc['longitude']}")

    # Upload da foto (obrigatório)
    foto = st.file_uploader(
        "Upload da foto da central (externa, portão aberto, visão dos tanques)",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("✅ Confirmar Check-in", disabled=(foto is None)):
        st.session_state.page = "equipamentos"

def equipamentos_page():
    show_header()

    for eq in EQUIPAMENTOS:
        with st.expander(f"EQUIPAMENTO: {eq['nome']} | QUANTIDADE: {eq['quantidade']}"):
            st.write(f"Fabricante: {eq['fabricante']}")
            st.write(f"Data de Fabricação: {eq['data_fabricacao']}")
            st.write(f"Nº Série: {eq['n_serie']}")
            st.write(f"Nº Patrimônio: {eq['n_patrimonio']}")

# -------------------------
# Roteamento
# -------------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "checkin":
    checkin_page()
elif st.session_state.page == "equipamentos":
    equipamentos_page()
