import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import rasterio

# Títulos e descrição
st.title("WebGIS Parque Nacional de Jericoacoara")
st.markdown(
    """
    Clique em um ponto no mapa para ver o nome e uma foto associada.
    """)

# Coordenadas centrais do mapa e nível de zoom definidos no código
#map_center = [-2.8142, -40.4923] 
#zoom_level = 11  # Nível de zoom inicial do mapa

# Criar o mapa
#st.subheader("Mapa Interativo")
#m = leafmap.Map(center=map_center, zoom=zoom_level, basemap="OpenStreetMap")




#m.add_geojson("polos_wgs.geojson", layer_name="Polos")
#m.add_geojson("pontos.geojson", layer_name="Pontos")
arvore = "arvore_da_preguica_wgs.tif"
arvore = leafmap.download_file("https://ambientis.eng.br/jeri/arvore_da_preguica_wgs.tif", "arvore_da_preguica_wgs.tif")
#m.add_raster("arvore_da_preguica_wgs.tif", layer_name="Árvore da Preguiça")

# Calcular os bounds do raster
with rasterio.open(arvore) as src:
    bounds = src.bounds  # Obtém os limites do raster
    center = [(bounds.top + bounds.bottom) / 2, (bounds.left + bounds.right) / 2]  # Centro

# Criar o mapa ajustado aos bounds
zoom = 18  # Ajuste o zoom conforme necessário
m = leafmap.Map(center=center, zoom=zoom)
m.add_raster("arvore_da_preguica_wgs.tif", layer_name="Árvore da Preguiça")


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


#m.add_tile_layer(
#    url="https://api.maptiler.com/tiles/7122380a-6c07-4aa6-9266-67b3be263a1b/{z}/{x}/{y}.png?key=siZ1uTKnlAee8SLZokfo",
#    name="Árvore da Preguiça",
#    attribution="MapTiler"
#)


# Exibir o mapa
m.to_streamlit()
