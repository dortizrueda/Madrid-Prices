import streamlit as st
import pandas as pd
import mlflow
import mlflow.pyfunc
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# Configuración inicial
mlflow.set_tracking_uri("http://localhost:5000") 
st.set_page_config(page_title="Predicción Inmuebles", layout="wide")

# Encabezado bonito
st.markdown("""
<h1 style="text-align:center;">🏠 Predicción de Precios de Vivienda</h1>
<p style="text-align:center; font-size:18px;">
Introduce los datos de un inmueble y obtén una estimación de su valor con el mejor modelo disponible.
</p>
""", unsafe_allow_html=True)

#  Carga optimizada del modelo
@st.cache_resource
def load_model():
    return mlflow.pyfunc.load_model("models:/ModeloProduccion/2")

modelo = load_model()

#  Zonas predefinidas
@st.cache_data
def cargar_zonas():
    return pd.DataFrame({
        "zona": [
            "arganzuela","barajas","barrio-de-salamanca","carabanchel","centro",
            "chamartin","chamberi","ciudad-lineal","fuencarral","hortaleza",
            "latina","moncloa","moratalaz","puente-de-vallecas","retiro",
            "san-blas","tetuan","usera","vicalvaro","villa-de-vallecas","villaverde"
        ],
        "Latitud": [
            40.396954,40.473318,40.436438,40.374211,40.417653,
            40.473954,40.438962,40.448431,40.426213,40.472549,
            40.403532,40.435020,40.405933,40.386860,40.411150,
            40.427500,40.460578,40.383894,40.401838,40.373958,40.345610
        ],
        "Longitud": [
            -3.697289,-3.579845,-3.685703,-3.744676,-3.707955,
            -3.682709,-3.705302,-3.650495,-3.700993,-3.642552,
            -3.736152,-3.719236,-3.644874,-3.659180,-3.676057,
            -3.615954,-3.698281,-3.706446,-3.595054,-3.612163,-3.695956
        ]
    })

zonas_df = cargar_zonas()

def detectar_zona(lat, lon):
    punto_usuario = (lat, lon)
    distancias = zonas_df.apply(
        lambda row: geodesic(punto_usuario, (row["Latitud"], row["Longitud"])).meters,
        axis=1
    )
    return zonas_df.loc[distancias.idxmin(), "zona"]

#  Entrada de datos
with st.expander("📌 Datos del inmueble", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        metros = st.number_input("Metros cuadrados", value=50.0, min_value=10.0)
        habitaciones = st.number_input("Habitaciones", value=2, min_value=0)
        baños = st.number_input("Baños", value=1, min_value=0)

    with col2:
        planta_num = st.number_input("Planta", value=1, min_value=-1)
        localizacion = st.radio("Localización", ["EXTERIOR", "INTERIOR"], horizontal=True)
        tiene_ascensor = st.checkbox("¿Tiene ascensor?", value=True)
        tiene_ascensor = int(tiene_ascensor)

#  Mapa de ubicación
with st.expander("🌍 Selecciona ubicación en el mapa", expanded=True):
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=11)
    map_data = st_folium(m, width=700, height=500)

    latitud, longitud, zona_auto = None, None, None

    if map_data and map_data["last_clicked"]:
        latitud = map_data["last_clicked"]["lat"]
        longitud = map_data["last_clicked"]["lng"]
        zona_auto = detectar_zona(latitud, longitud)
        folium.Marker([latitud, longitud], popup="Ubicación seleccionada").add_to(m)

        st.info(f"📍 Coordenadas: **Lat {latitud:.5f}, Lon {longitud:.5f}**")
        st.success(f"Zona detectada automáticamente: **{zona_auto}**")

    zona = zona_auto or st.selectbox("Zona (si no seleccionas en el mapa)", zonas_df["zona"].tolist())

#  Predicción
entrada_df = pd.DataFrame([{
    "metros": metros,
    "habitaciones": habitaciones,
    "tiene_ascensor": tiene_ascensor,
    "planta_num": planta_num,
    "baños": baños,
    "Latitud": latitud,
    "Longitud": longitud,
    "zona": zona,
    "localizacion": localizacion
}])

st.markdown("---")

if st.button("🔮 Predecir precio"):
    try:
        with st.spinner("Calculando predicción..."):
            pred = modelo.predict(entrada_df)

        st.markdown(f"""
        <div style="background-color:#e0f7fa; padding:20px; border-radius:10px; text-align:center;">
            <h2>💰 Precio estimado: {pred[0]:,.2f} €</h2>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error al predecir: {str(e)}")
