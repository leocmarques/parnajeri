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

# Coordenadas centrais do mapa e nível de zoom definidos no código
map_center = [-15.7942, -47.8822]  # Exemplo: Brasília, Brasil
zoom_level = 10  # Nível de zoom inicial do mapa

# Carregar camada vetorial
try:
    gdf = gpd.read_file(vetorial_url)
    st.write("Camada vetorial carregada com sucesso. Primeiras 5 linhas:")
    st.write(gdf.head())
except Exception as e:
    st.error(f"Erro ao carregar a camada vetorial: {e}")

# Criar o mapa
st.subheader("Mapa Interativo")
m = leafmap.Map(center=map_center, zoom=zoom_level, basemap="OpenStreetMap")

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
