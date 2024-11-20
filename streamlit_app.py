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
arvore = "arvore_da_preguica_wgs.tif"
arvore = leafmap.download_file("https://ambientis.eng.br/jeri/arvore_da_preguica_wgs.tif", "arvore_da_preguica_wgs.tif")
m.add_raster("arvore_da_preguica_wgs.tif", layer_name="Árvore da Preguiça")


# Caminhos dos arquivos
geotiff_file = "arvore_da_preguica_wgs.tif"  # Substitua pelo caminho do seu GeoTIFF
mbtiles_file = "output.mbtiles"  # Arquivo intermediário MBTiles
pmtiles_file = "output.pmtiles"  # Arquivo final PMTiles

try:
    # Passo 1: Converter GeoTIFF para MBTiles usando gdal2tiles.py
    print("Convertendo GeoTIFF para MBTiles...")
    subprocess.run([
        "gdal2tiles.py",
        "--xyz",
        geotiff_file,
        mbtiles_file
    ], check=True)

    # Passo 2: Converter MBTiles para PMTiles
    print("Convertendo MBTiles para PMTiles...")
    convert.mbtiles_to_pmtiles(mbtiles_file, pmtiles_file)
    print(f"Conversão bem-sucedida: {pmtiles_file}")

except subprocess.CalledProcessError as e:
    print(f"Erro durante a conversão de GeoTIFF para MBTiles: {e}")
except Exception as e:
    print(f"Erro durante a conversão de MBTiles para PMTiles: {e}")



#convert.mbtiles_to_pmtiles("arvore.mbtiles", "pmtiles_arvore.pmtiles",maxzoom=20)
m.add_pmtiles("output.pmtiles", name="Árvore", attribution="Dados PMTiles")

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
