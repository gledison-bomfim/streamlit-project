import streamlit as st
from datetime import datetime, date

# -------------------------
# Configurações iniciais
# -------------------------
st.set_page_config(page_title="Check in", layout="wide")

# -------------------------
# Parâmetros
# -------------------------
query_params = st.query_params
cliente = query_params.get("cliente", "JC PIZZARIA LTDA")
central = query_params.get("central", "Central Padrão")

if "page" not in st.session_state:
    st.session_state.page = "home"

def get_location():
    return {"latitude": -19.9227, "longitude": -43.9451}

EQUIPAMENTOS = [
    {"nome": "Tanque P190","quantidade": 2,"fabricante": "ACME","data_fabricacao": "2020-01-01","n_serie": "12345","n_patrimonio": "P190-001"},
    {"nome": "Reguladores de Pressão","quantidade": 4,"fabricante": "Regula","data_fabricacao": "2021-03-15","n_serie": "67890","n_patrimonio": "REG-004"},
]

# -------------------------
# Estilos globais (mobile-first)
# -------------------------
st.markdown(
    """
    <style>
      @media (max-width: 480px){
        .block-container{padding-top: 0.6rem; padding-bottom: 0.8rem;}
      }

      .header{margin: 0 0 .5rem 0;}
      .header-top{
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        column-gap: 12px;
      }
      .header-logo{
        width: 80px; /* logo menor também pra combinar */
      }
      .header-phantom{width: 80px;}
      .header-title{
        text-align: center;
      margin: 10px 0 0 0;   /* 👈 empurra o título um pouco para baixo */

        /*font-size: clamp(1.3rem, 4vw + .2rem, 1.8rem);  menor */
        font-size: clamp(1.3rem, 3vw + .2rem, 1.5rem);
        line-height: 1.1;
      }
      .header-meta{
        margin-top: .25rem;
      }
      .header-meta .line{
        margin: 0;
        text-align: left;
        font-weight: 600;
        font-size: clamp(0.9rem, 2.5vw + .2rem, 1rem); /* ↓ menor */
      }

      .store-buttons{
        display: flex;
        gap: 10px;
        flex-wrap: nowrap;
        justify-content: center;
        margin-top: .5rem;
      }
      .store-buttons a{
        text-decoration: none;
        border: 1px solid rgba(0,0,0,.15);
        border-radius: .5rem;
        padding: .5rem .8rem;
        display: inline-block;
        font-weight: 600;
        font-size: 0.9rem; /* ↓ menor */
      }
      .hr{margin:.6rem 0 .8rem 0;}
    </style>
    """,
    unsafe_allow_html=True
)



# -------------------------
# Cabeçalho
# -------------------------
def show_header():
    st.markdown(
        f"""
        <div class="header">
          <div class="header-top">
            <img class="header-logo" src="https://raw.githubusercontent.com/gledison-bomfim/streamlit-project/master/Logo-Versao-Preferencial.png" />
            <h1 class="header-title">Check in</h1>
            <div class="header-phantom"></div>
          </div>
          <div class="header-meta">
            <p class="line">Central: {central}</p>
            <p class="line">Cliente: {cliente}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# Páginas
# -------------------------
def home_page():
    show_header()

    st.markdown('<div class="hr"><hr/></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📍 Fazer Check-in"):
            st.session_state.page = "checkin"
    with c2:
        st.button("ℹ️ Ver informações do cliente")

    st.markdown('<div class="hr"><hr/></div>', unsafe_allow_html=True)
    st.warning("Se for cliente, acesse o app Super Gestão:")

    # Botões das lojas lado a lado (inclusive no mobile)
    st.markdown(
        """
        <div class="store-buttons">
          <a href="https://play.google.com/store/apps/details?id=com.supergasbras.superapp&hl=pt_BR" target="_blank" rel="noopener">Google Play</a>
          <a href="https://apps.apple.com/br/app/super-gest%C3%A3o-supergasbras/id1556506493" target="_blank" rel="noopener">App Store</a>
        </div>
        """,
        unsafe_allow_html=True
    )

def checkin_page():
    show_header()

    motivo = st.selectbox(
        "Selecione o motivo da visita:",
        ["Abastecimento","Visita Relacionamento","Assistência Técnica","Manutenção Preventiva","Visita SPOT","NR13/Requalificação"]
    )

    # Data e hora fixas (não editáveis)
    st.text_input("Data", value=date.today().strftime("%d/%m/%Y"), disabled=True)
    st.text_input("Hora", value=datetime.now().strftime("%H:%M"), disabled=True)

    loc = get_location()
    st.info(f"Localização detectada: Latitude {loc['latitude']}, Longitude {loc['longitude']}")

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











