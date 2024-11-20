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
vetorial_url = "polos_wgs.geojson"  # Substitua pela URL do vetor
#raster_url = "https://seusite.com/data/camada.tif"        # Substitua pela URL do raster

# Coordenadas centrais do mapa e nível de zoom definidos no código
map_center = [-2.8142, -40.4923] 
zoom_level = 11  # Nível de zoom inicial do mapa

# Carregar camada vetorial
try:
    gdf = gpd.read_file(vetorial_url)
    #st.write("Camada vetorial carregada com sucesso. Primeiras 5 linhas:")
    #st.write(gdf.head())
except Exception as e:
    st.error(f"Erro ao carregar a camada vetorial: {e}")

# Criar o mapa
st.subheader("Mapa Interativo")
m = leafmap.Map(center=map_center, zoom=zoom_level, basemap="OpenStreetMap")

m.add_geojson("polos_wgs.geojson", layer_name="Polos")
m.add_geojson("pontos.geojson", layer_name="Pontos")
arvore = leafmap.download_file("https://ambientis.eng.br/jeri/arvore_da_preguica_wgs.tif", "arvore.tif")
m.add_raster(arvore, layer_name="Ortofoto - Árvore da Preguiça")


# Adicionar camada vetorial com popups personalizados
#if 'gdf' in locals():
#    for _, row in gdf.iterrows():
#        nome = row["name"]
#        foto_url = row["photo_url"]
#        coord = row.geometry.coords[0]
#        popup_html = f"""
#        <h4>{nome}</h4>
#        <img src="{foto_url}" alt="Foto de {nome}" width="300"/>
#        """
#        m.add_marker(location=(coord[1], coord[0]), popup=popup_html)

# Adicionar camada raster ao mapa
try:
    m.add_raster("https://api.maptiler.com/tiles/7122380a-6c07-4aa6-9266-67b3be263a1b/{z}/{x}/{y}.png?key=siZ1uTKnlAee8SLZokfo", layer_name="Árvore da Preguiça")
    #st.write("Camada raster carregada com sucesso.")
except Exception as e:
    st.error(f"Erro ao carregar a camada raster: {e}")

#m.add_tile_layer(
#    url="https://api.maptiler.com/tiles/7122380a-6c07-4aa6-9266-67b3be263a1b/{z}/{x}/{y}.png?key=siZ1uTKnlAee8SLZokfo",
#    name="Árvore da Preguiça",
#    attribution="MapTiler"
#)


# Exibir o mapa
m.to_streamlit()
