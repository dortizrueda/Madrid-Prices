import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Análisis de Precios de Pisos", page_icon="🏠")
sns.set_style("whitegrid")

# Cargar datos con cache
@st.cache_data
def load_data():
    return pd.read_csv("../data/datos_limpios_eda.csv")

df = load_data()

# Funciones de visualización
def grafico_precio_superficie(data):
    data['metros_rango'] = pd.cut(
        data['metros'],
        bins=[0, 40, 60, 80, 100, 150, 200, 300],
        labels=['<40', '40-60', '60-80', '80-100', '100-150', '150-200', '200+']
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x='metros_rango', y='PrecioActual', palette='Set2', ax=ax)
    ax.set_title("Precio medio según superficie del piso")
    ax.set_xlabel("Superficie (m²)")
    ax.set_ylabel("Precio (€)")
    st.pyplot(fig)

def grafico_precios_zona(data):
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.violinplot(x='zona', y='PrecioActual', data=data,
                   inner='quartile', density_norm='width', ax=ax)
    ax.set_title('Distribución de PrecioActual por Zona')
    ax.set_xlabel('Zona')
    ax.set_ylabel('Precio Actual (€)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def histograma_precios(data):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data.loc[data['PrecioActual'] <= 5_000_000, 'PrecioActual'],
                 bins=50, kde=True, color='salmon', ax=ax)
    ax.set_title('Distribución de precios actuales (<= 5M €)')
    ax.set_xlabel('Precio Actual (€)')
    ax.set_ylabel('Número de pisos')
    st.pyplot(fig)

def mapa_precios(data):
    centro = [data['Latitud'].mean(), data['Longitud'].mean()]
    mapa = folium.Map(location=centro, zoom_start=12, tiles='CartoDB positron')

    colormap = folium.LinearColormap(
        colors=['blue', 'green', 'yellow', 'red'],
        vmin=data['PrecioActual'].min(),
        vmax=data['PrecioActual'].max(),
        caption='Precio Actual (€)'
    )

    marker_cluster = MarkerCluster().add_to(mapa)

    for _, row in data.iterrows():
        precio = row['PrecioActual']
        color = colormap(precio)
        folium.CircleMarker(
            location=[row['Latitud'], row['Longitud']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=f"Precio: {precio:,.0f} €"
        ).add_to(marker_cluster)

    colormap.add_to(mapa)
    st_folium(mapa, width=700, height=500)

# Interfaz principal
st.title("📊 Análisis de Precios de Pisos en Madrid")

opcion = st.selectbox(
    "Selecciona la visualización:",
    [
        "Precio medio según superficie",
        "Distribución de precios por zona",
        "Histograma de precios actuales",
        "Mapa interactivo de precios"
    ]
)

if opcion == "Precio medio según superficie":
    grafico_precio_superficie(df)
elif opcion == "Distribución de precios por zona":
    grafico_precios_zona(df)
elif opcion == "Histograma de precios actuales":
    histograma_precios(df)
elif opcion == "Mapa interactivo de precios":
    mapa_precios(df)
