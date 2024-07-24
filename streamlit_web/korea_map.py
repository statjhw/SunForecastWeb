import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# 스트림릿 앱 제목 설정
st.title("대한민국 남한 지도")

# 대한민국 지도 데이터 로드
@st.cache_data
def load_data():
    # 압축을 풀고 준비된 데이터를 사용하여 대한민국 경계 로드
    path_to_shapefile = 'C:/SPB_Data/cowork_project/streamlit_web/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp'  # 실제 Shapefile 파일 경로로 수정 필요
    world = gpd.read_file(path_to_shapefile)
    south_korea = world[world['NAME'] == "South Korea"]
    return south_korea

south_korea = load_data()

# Folium 지도 객체 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# GeoDataFrame을 folium에 추가
folium.GeoJson(south_korea).add_to(m)

# 스트림릿을 통해 Folium 지도 렌더링
st_data = st_folium(m, width=700, height=500)
