import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import rasterio
import os
import subprocess
import pmtiles.convert as convert


# Títulos e descrição
st.title("WebGIS Parque Nacional de Jericoacoara")
st.markdown(
    """
    Clique em um ponto no mapa para ver o nome e uma foto associada.
    """)

# Coordenadas centrais do mapa e nível de zoom definidos no código
map_center = [-2.8142, -40.4923] 
zoom_level = 11  # Nível de zoom inicial do mapa

# Criar o mapa
st.subheader("Mapa Interativo")
m = leafmap.Map(center=map_center, zoom=zoom_level, basemap="OpenStreetMap")

# Adicionar basemap do Google Satellite
m.add_xyz_service("qms.Google Satellite")

m.add_geojson("polos_wgs.geojson", layer_name="Polos")
m.add_geojson("pontos.geojson", layer_name="Pontos")
arvore = "arvore_wgs84.tif"
arvore = leafmap.download_file("https://ambientis.eng.br/jeri/arvore_wgs84.tif", "arvore_wgs84.tif")
m.add_raster("arvore_wgs84.tif", layer_name="Árvore da Preguiça")


#convert.mbtiles_to_pmtiles("arvore.mbtiles", "arvore.pmtiles",maxzoom=20)
#m.add_pmtiles("arvore.pmtiles", name="Árvore", attribution="Dados PMTiles")

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


# Exibir o mapa
m.to_streamlit()
