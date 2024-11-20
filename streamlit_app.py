import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

# Títulos e descrição
st.title("WebGIS com Fotos em Popups")
st.markdown(
    """
    Clique em um ponto no mapa para ver o nome e uma foto associada.
    """
)

# URL da camada vetorial (GeoJSON com links para fotos)
vetorial_url = "https://seusite.com/data/camada.geojson"  # Substitua pela URL do seu vetor

# Carregar camada vetorial
try:
    gdf = gpd.read_file(vetorial_url)
    st.write("Primeiras 5 linhas da camada vetorial:")
    st.write(gdf.head())
except Exception as e:
    st.error(f"Erro ao carregar camada vetorial: {e}")

# Criar o mapa
st.subheader("Mapa Interativo")
m = leafmap.Map(center=(0, 0), zoom=2)

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

# Exibir o mapa no Streamlit
m.to_streamlit(height=600)
