import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pathlib import Path


# 데이터 준비
data = pd.read_csv("./data/합친거.csv")

#지역별 코드보여주는 html
local_codes_html = Path('./htmls/local_codes.html')


#페이지 생성
st.set_page_config(page_title='중요하지 않아', page_icon='🌎')

#사이드 바
with st.sidebar:
    choice = option_menu("Menu", ["홈", "발전량 예측", "페이지3"],
                         icons=['house', 'bar-chart-line', 'bi bi-robot'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )
    

#홈
if choice=='홈':
    st.header('"중요하지 않아"의 플랫폼에 오신걸 환영합니다!')

    st.divider()

    st.subheader('😎개요')
    '''
    본 플랫폼에서는 2013년01월01일 ~ 2017년02월28일에 측정된 태양광발전량데이터와
    해당 지역별 기상데이터를 이용하여 AI모델에게 학습시킨 후, 이 후의 태양광발전량데이터를 
    예측하였습니다.
    '''
    
    ''

    st.subheader('💸활용성')
    '''
    태양광으로 발전한 전기를 전력시장에 유통할 때 특정 기간동안의 예측된 발전량을 제출한 후
    실제 발전량과 오차가 적은 만큼 가격이 올라간다고 합니다! 그럼 예측된 발전량이 정확할수록
    더 큰 이윤을 남길 수 있겠죠! 
    '''


    
    
#발전량 예측
elif choice=='발전량 예측':

    
    #지역코드보여주는 html파일 불러오기
    if local_codes_html.exists():
        st.html(local_codes_html)
    else:
        st.error('html 파일이 없음')
    ''

    #지역 코드들
    locals = data['code'].unique()

    #원하는 지역코드들 선택
    selected_locals = st.multiselect(
        '보고싶은 지역들을 선택하세요!',
        locals,
        ['KSN','KSB','KWJ'])
    
    filtered_data = data[data['code'].isin(selected_locals)]
    
    ''
    st.header('태양광 발전량 예측 그래프')
    st.line_chart(filtered_data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    


#페이지3
elif choice=='페이지3':
    st.header('여기다가 뭘할까')

    tab1, tab2, tab3 = st.tabs(['탭1','탭2','탭3'])

    with tab1:
        st.header('막대그래프')
        st.bar_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    with tab2:
        st.header('영역그래프')
        st.area_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    with tab3:
        st.header('점그래프')
        st.scatter_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')