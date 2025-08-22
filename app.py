# ----------------------------------
# Páginas (atualizado)
# ----------------------------------
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

    # ---------- ADICIONADO ----------
    # Exibe a imagem antes dos equipamentos
    st.markdown("### Imagem de referência:")
    st.image(
        "https://raw.githubusercontent.com/gledison-bomfim/streamlit-project/master/faton.png",
        caption="Faton (exemplo ilustrativo)",
        use_column_width=True  # Ajusta a largura automaticamente
    )
    # ---------- FIM ADICIONADO ----------

    for eq in EQUIPAMENTOS:
        with st.expander(f"EQUIPAMENTO: {eq['nome']} | QUANTIDADE: {eq['quantidade']}"):
            st.write(f"Fabricante: {eq['fabricante']}")
            st.write(f"Data de Fabricação: {eq['data_fabricacao']}")
            st.write(f"Nº Série: {eq['n_serie']}")
            st.write(f"Nº Patrimônio: {eq['n_patrimonio']}")
