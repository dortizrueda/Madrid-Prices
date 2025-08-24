import streamlit as st


st.set_page_config(page_title="Tasador", page_icon="🏠")
st.title("Predicción de precios de pisos de Madrid")

tab1, tab2 = st.tabs(["Resumen", "Contacto"])

with tab1:
    st.subheader("Resumen del proyecto")
    st.write("Este proyecto predice precio de pisos en la ciudad de Madrid")

with tab2:
    st.subheader("Contacto")
    st.write("Autor: David Ortiz Rueda")
    st.write("Correo: dortizrueda@uma.es")