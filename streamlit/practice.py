# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime

# # # 날짜 및 시간 데이터 정의
# # data = ['2017-01-01-1', '2017-01-01-2', '2017-01-01-3']

# # # 문자열을 datetime 객체로 변환
# # data = [pd.to_datetime(d, format='%Y-%m-%d-%H').to_pydatetime() for d in data]

# # # 슬라이더의 최소값, 최대값, 초기값 설정
# # min_value = data[0]
# # max_value = data[2]
# # initial_value = data[1]

# # # Streamlit 슬라이더 생성
# # value = st.slider('Select a value', min_value=min_value, max_value=max_value, value=initial_value)

# # # 선택된 값 출력
# # st.write('Selected value:', value)

# data = pd.read_csv("./data/합친거.csv")


# def convert_to_datetime(date_str):
#     # 문자열 형식에서 시간 부분이 24인 경우를 처리
#     if '-' in date_str:
#         date_part, hour_part = date_str[0:4],date_str[4:]
#         if hour_part == '24':
#             hour_part = '00'
#         datetime_str = f"{date_part} {hour_part}:00:00"
#         return datetime.strptime(datetime_str, '%Y-%m-%d')
#     else:
#         return pd.NaT  # 형식이 맞지 않으면 NaT 반환

# # 'datetime' 열을 변환
# data['Date'] = data['Date'].apply(convert_to_datetime)

# # data['0']=data['Unnamed: 0']
# st.line_chart(
#     data,
#     x='Date',
#     y='Solar_Power(MWh)',
#     color ='code',
# )
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pathlib import Path


# 데이터 준비
data = pd.read_csv("./data/합친거.csv")
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


    
    

elif choice=='발전량 예측':
    st.header('태양광 발전량 예측 그래프')
    st.line_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    if local_codes_html.exists():
        st.html(local_codes_html)
    else:
        st.error('html 파일이 없음')


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