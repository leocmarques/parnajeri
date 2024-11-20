import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Título e descrição
st.title("WebGIS com Raster, Vetores e Popups com Fotos")
st.markdown(
    """
    Um WebGIS interativo que permite:
    - Exibir camadas vetoriais com popups contendo links e fotos.
    - Carregar uma camada raster.
    - Configurar coordenada central do mapa.
    - Alterar basemaps.
    """
)

# URLs das camadas
vetorial_url = "https://seusite.com/data/camada.geojson"  # Substitua pela URL do vetor
raster_url = "https://seusite.com/data/camada.tif"        # Substitua pela URL do raster

# Carregar camada vetorial
try:
    gdf = gpd.read_file(vetorial_url)
    st.write("Camada vetorial carregada com sucesso. Primeiras 5 linhas:")
    st.write(gdf.head())
except Exception as e:
    st.error(f"Erro ao carregar a camada vetorial: {e}")

# Criar opções de configuração do mapa
st.sidebar.header("Configurações do Mapa")

# Escolher o centro do mapa
default_center = [0, 0]
center_lat = st.sidebar.number_input("Latitude do centro do mapa", value=default_center[0])
center_lon = st.sidebar.number_input("Longitude do centro do mapa", value=default_center[1])
zoom_level = st.sidebar.slider("Nível de zoom", min_value=2, max_value=18, value=5)

# Escolher basemap
basemap_options = ["OpenStreetMap", "Satellite", "Terrain", "CartoDB.DarkMatter"]
basemap_choice = st.sidebar.selectbox("Escolher basemap", basemap_options)

# Criar o mapa
st.subheader("Mapa Interativo")
m = leafmap.Map(center=(center_lat, center_lon), zoom=zoom_level, basemap=basemap_choice)

# Adicionar camada vetorial com popups personalizados
if 'gdf' in locals():
    for _, row in gdf.iterrows():
        # Extrair atributos
        nome = row["name"]
        foto_url = row["photo_url"]
        coord = row.geometry.coords[0]  # Coordenadas do ponto

        # Criar popup com foto
        popup_html = f"""
        <h4>{nome}</h4>
        <img src="{foto_url}" alt="Foto de {nome}" width="300"/>
        """

        # Adicionar ponto no mapa
        m.add_marker(location=(coord[1], coord[0]), popup=popup_html)

# Adicionar camada raster ao mapa
try:
    m.add_raster(raster_url, layer_name="Camada Raster")
    st.write("Camada raster carregada com sucesso.")
except Exception as e:
    st.error(f"Erro ao carregar a camada raster: {e}")

# Exibir o mapa no Streamlit
m.to_streamlit(height=600)
