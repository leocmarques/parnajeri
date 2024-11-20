import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Títulos e descrição
st.title("WebGIS com Raster e Vetor")
st.markdown(
    """
    Clique em um ponto no mapa para ver o nome e uma foto associada.
    """
)

# URLs das camadas
vetorial_url = "https://ambientis.eng.br/jeri/polos.geojson"  # Substitua pela URL do vetor
raster_url = "https://seusite.com/data/camada.tif"        # Substitua pela URL do raster

# Carregar camada vetorial
try:
    gdf = gpd.read_file(vetorial_url)
    st.write("Camada vetorial carregada com sucesso. Primeiras 5 linhas:")
    st.write(gdf.head())
except Exception as e:
    st.error(f"Erro ao carregar a camada vetorial: {e}")

# Configurações do mapa no sidebar
st.sidebar.header("Configurações do Mapa")
default_center = [0, 0]
center_lat = st.sidebar.number_input("Latitude do centro do mapa", value=default_center[0])
center_lon = st.sidebar.number_input("Longitude do centro do mapa", value=default_center[1])
zoom_level = st.sidebar.slider("Nível de zoom", min_value=2, max_value=18, value=5)
basemap_options = ["OpenStreetMap", "Satellite", "Terrain", "CartoDB.DarkMatter"]
basemap_choice = st.sidebar.selectbox("Escolher basemap", basemap_options)

# Criar o mapa
m = leafmap.Map(center=(center_lat, center_lon), zoom=zoom_level, basemap=basemap_choice)

# Adicionar camada vetorial com popups personalizados
if 'gdf' in locals():
    for _, row in gdf.iterrows():
        nome = row["name"]
        foto_url = row["photo_url"]
        coord = row.geometry.coords[0]
        popup_html = f"""
        <h4>{nome}</h4>
        <img src="{foto_url}" alt="Foto de {nome}" width="300"/>
        """
        m.add_marker(location=(coord[1], coord[0]), popup=popup_html)

# Adicionar camada raster ao mapa
try:
    m.add_raster(raster_url, layer_name="Camada Raster")
    st.write("Camada raster carregada com sucesso.")
except Exception as e:
    st.error(f"Erro ao carregar a camada raster: {e}")

# Exibir o mapa
m.to_streamlit(height=600)
