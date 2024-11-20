import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import rasterio
import os
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

# Função para analisar o raster
def analyze_raster(file_path):
    try:
        with rasterio.open(file_path) as src:
            # Coletar informações do raster
            bounds = src.bounds
            crs = src.crs
            width = src.width
            height = src.height
            band_count = src.count
            data_type = src.dtypes[0]  # Tipo de dado da primeira banda

            # Criar um dicionário com as informações
            raster_info = {
                "Bounds (Extent)": bounds,
                "CRS (Sistema de Referência)": crs,
                "Largura (Pixels)": width,
                "Altura (Pixels)": height,
                "Quantidade de Bandas": band_count,
                "Tipo de Dado": data_type
            }
            return raster_info
    except Exception as e:
        st.error(f"Erro ao analisar o raster: {e}")
        return None

# Caminho para o raster
raster_path = "arvore_wgs84.tif"

# Analisar o raster
raster_info = analyze_raster(raster_path)

# Exibir os resultados no Streamlit
if raster_info:
    st.subheader("Informações do Raster")
    for key, value in raster_info.items():
        st.write(f"**{key}:** {value}")



with rasterio.open("arvore_wgs84.tif") as src:
    bounds = src.bounds
    center_lat = (bounds.top + bounds.bottom) / 2
    center_lon = (bounds.left + bounds.right) / 2

m = leafmap.Map(center=[center_lat, center_lon], zoom=18)
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
