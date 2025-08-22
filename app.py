for i, eq in enumerate(equipamentos):
    st.subheader(f"{eq['nome']} — Quantidade: {eq['quantidade']}")

    with st.expander("Ver detalhes"):
        st.write(f"Fabricante: {eq['fabricante']}")
        st.write(f"Data de fabricação: {eq['data_fabricacao']}")
        st.write(f"Nº Série: {eq['numero_serie']}")
        st.write(f"Nº Patrimônio: {eq['patrimonio']}")

        divergencia = st.multiselect(
            f"Reportar divergência ({eq['nome']}):",  # 🔑 label único
            ["Quantidade", "Número de Série", "Fabricante", "Nº Patrimônio"],
            key=f"divergencia_{i}"  # 🔑 também um key único
        )
        if divergencia:
            st.warning(f"Divergências reportadas em {eq['nome']}: {', '.join(divergencia)}")
