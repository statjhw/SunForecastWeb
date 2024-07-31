import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pathlib import Path
import requests
import base64
import os
import subprocess







# 데이터 준비
data = pd.read_csv("./data/합친거.csv")




# html들 연결
local_codes_html = Path('./htmls/local_codes.html')
korea_html = Path('./htmls/korea.html')




#서버 주소
my_url = 'http://127.0.0.1:8000/'

#쿼리문 저장
query_params = st.query_params



#페이지 생성
st.set_page_config(page_title='중요하지 않아', page_icon='🌎')



#사이드 바
with st.sidebar:

    choice = option_menu("Menu", ["홈", "기존 발전량", "그래프들", "지역별 예측"],
                         icons=['house', 'bar-chart-line', 'bi bi-robot', 'map'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )

    #지역이 선택되면 지역별 예측으로 고정
    if 'region' in query_params:
        choice = '지역별 예측'
        
    

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

    if st.button('누르면 서버와 통신1'):
        response = requests.get(my_url)

        st.title('서버에서 보낸 것:')
        st.subheader(response.content)

    if st.button('누르면 서버와 통신2'):
        response = requests.get(my_url+'items/3')

        st.title('서버에서 보낸 것:')
        st.subheader(response.json()['item_id'])

    
    
#발전량 예측
elif choice=='기존 발전량':

    
    #지역코드보여주는 html파일 불러오기
    if local_codes_html.exists():
        st.html(local_codes_html)
    else:
        st.error('html 파일이 없음')
    ''

    #지역 code들
    locals = data['code'].unique()

    #원하는 지역코드들 선택
    selected_locals = st.multiselect(
        '보고싶은 지역들을 선택하세요!',
        locals,
        ['KSN','KSB','KWJ'])
    
    filtered_data = data[data['code'].isin(selected_locals)]
    
    ''
    st.header('기존 태양광 발전량 그래프')
    st.line_chart(filtered_data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    


#페이지3
elif choice=='그래프들':
    st.header('여러가지 그래프')

    tab1, tab2, tab3 = st.tabs(['막대','영역','점'])

    with tab1:
        st.header('막대그래프')
        st.bar_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    with tab2:
        st.header('영역그래프')
        st.area_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    with tab3:
        st.header('점그래프')
        st.scatter_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')
        

elif choice=='지역별 예측':      

    

    st.header('원하는 지역을 클릭하면 밑에 예측량이 보여집니다')
    
    
    
    # 이미지태그가 안돼서 이미지를 base64로 인코딩
    file_ = open("./img/korea_map.png", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    

    st.html(
        f'''<div>
            <img class="korea_map" src="data:image/png;base64,{data_url}" alt="korea_map" usemap="#image-map">
                <map name="image-map">
                    <area target="_blank" alt="서울" title="서울" href="?region=seoul" coords="269,250,267,236,247,243,230,254,222,261,233,277,250,285,273,280,281,263" shape="poly">
                    <area target="_self" alt="인천" title="인천" href="?region=incheon" coords="214,257,197,242,188,253,194,270,202,283,205,289,215,280" shape="poly">
                    <area target="_self" alt="경기도" title="경기도" href="경기도링크" coords="358,192,333,166,324,148,313,155,301,140,285,121,269,116,238,136,237,159,230,172,223,189,211,203,213,224,195,216,165,216,159,232,162,243,177,243,198,236,217,243,233,244,265,227,277,239,283,249,289,263,283,278,270,288,254,292,235,290,220,269,219,291,208,300,213,308,185,324,197,336,219,343,215,366,230,384,248,389,274,381,299,391,326,370,349,355,367,335,379,289,384,268,345,250,336,220,343,203" shape="poly">
                    <area target="_self" alt="강원도" title="강원도" href="강원도링크" coords="642,360,609,292,595,242,488,53,468,94,389,106,298,105,289,113,301,132,322,142,343,164,363,191,355,212,348,230,362,248,396,270,388,287,381,328,381,342,401,342,417,328,438,331,481,339,522,361" shape="poly">
                    <area target="_self" alt="충청남도" title="충청남도" href="충청남도링크" coords="309,424,273,391,221,404,176,372,161,381,151,376,155,393,136,403,129,388,102,421,121,431,137,451,158,440,171,472,169,500,167,548,197,573,233,547,271,559,302,563,314,580,327,581,340,576,338,560,336,541,309,545,285,536,277,513,278,488,266,456,265,430" shape="poly">
                    <area target="_self" alt="충청북도" title="충청북도" href="충청북도링크" coords="520,369,465,356,453,341,429,348,415,339,405,352,372,352,356,366,338,376,313,392,301,402,318,417,321,434,305,437,311,452,316,466,318,476,332,488,339,502,333,531,349,564,369,573,384,573,398,571,401,549,410,537,391,529,381,512,385,481,379,456,391,447,439,409,481,415" shape="poly">
                    <area target="_self" alt="대전" title="대전" href="대전링크" coords="333,502,317,494,308,486,295,499,289,519,297,534,308,527,317,539,323,532" shape="poly">
                    <area target="_self" alt="세종" title="세종" href="세종링크" coords="310,467,292,451,293,438,273,438,280,466,288,488,300,485" shape="poly">
                    <area target="_self" alt="경상북도" title="경상북도" href="경상북도링크" coords="644,363,602,380,527,381,499,412,470,430,453,422,429,431,429,448,410,448,401,469,393,467,401,524,425,540,416,558,401,587,413,617,442,635,447,652,468,658,472,623,493,586,532,584,542,609,537,646,520,654,508,659,514,667,538,670,578,661,608,647,635,655,656,659,670,593,639,591,654,494,659,420" shape="poly">
                    <area target="_self" alt="경상남도" title="경상남도" href="경상남도링크" coords="607,715,570,684,572,675,503,678,490,666,441,666,430,652,433,641,392,615,357,629,342,674,352,704,337,732,369,786,356,807,409,784,422,810,456,808,464,817,483,778,501,779,515,767,534,768" shape="poly">
                    <area target="_self" alt="울산" title="울산" href="울산링크" coords="648,699,654,672,629,666,600,657,584,682,611,705,629,726" shape="poly">
                    <area target="_self" alt="대구" title="대구" href="대구링크" coords="521,643,530,614,524,592,497,610,485,610,490,631,481,644,482,662" shape="poly">
                    <area target="_self" alt="전라북도" title="전라북도" href="전라북도링크" coords="377,582,319,590,289,570,246,571,228,558,195,585,173,597,205,606,197,631,149,657,179,673,140,694,153,713,180,707,195,681,220,704,247,693,253,720,285,720,315,716,333,716,336,658,351,626,380,608" shape="poly">
                    <area target="_self" alt="전라남도" title="전라남도" href="전라남도링크" coords="360,788,325,728,248,731,236,708,216,716,197,698,183,718,154,722,140,716,120,741,139,772,124,790,129,826,149,852,140,861,129,852,128,863,105,849,106,868,82,906,119,898,118,874,140,889,144,921,179,901,188,869,198,901,225,896,229,858,254,846,280,843,285,852,274,864,256,884,281,900,301,881,310,879,300,848,313,828,325,838,326,861,335,868,341,853,363,853,364,837,343,825,335,815,237,777,189,777,167,763,174,737,217,726,249,751,231,774,334,816" shape="poly">
                    <area target="_self" alt="광주" title="광주" href="광주링크" coords="231,752,213,738,192,738,179,753,177,761,196,769,214,768,229,767" shape="poly">
                    <area target="_self" alt="부산" title="부산" href="부산링크" coords="625,736,613,723,581,744,558,758,547,773,556,779,581,788,608,768" shape="poly">
                    <area target="_self" alt="제주도" title="제주도" href="제주도링크" coords="208,1037,184,1023,121,1034,78,1062,99,1108,193,1076,209,1054" shape="poly">
                    <area target="_self" alt="울릉도,독도" title="울릉도,독도" href="울릉도, 독도링크" coords="775,329,775,267,678,267,680,331" shape="poly">
                </map>
            </div>
            '''
    )

    

    #지역별 그래프불러오기
     #처음에 region이 없으므로 예외처리
    if 'region' not in query_params:
        st.warning("지역을 선택해주세요")

    
    elif query_params['region'] == 'seoul':
        response = requests.get(my_url + '/seoul')
        
        st.write(response.json())
        
    