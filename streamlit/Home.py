import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pathlib import Path
import requests
import base64
from datetime import datetime






# 데이터 준비
data = pd.read_csv("./data/합친거한글.csv")




# html들 연결
local_codes_html = Path('./htmls/local_codes.html')
korea_html = Path('./htmls/korea.html')




#서버 주소
my_url = 'http://127.0.0.1:8001/'




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
    if 'region' in st.query_params:
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
    # if local_codes_html.exists():
    #     st.html(local_codes_html)
    # else:
    #     st.error('html 파일이 없음')
    # ''

    #지역 code들
    locals = data['code'].unique()
    
    regions_codes = {
    "강원도": 1,
    "경기도": 2,
    "경상남도": 3,
    "경상북도": 4,
    "광주시": 5,
    "대구시": 6,
    "대전시": 7,
    "부산시": 8,
    "서울시": 9,
    "세종시": 10,
    "울산시": 11,
    "인천시": 12,
    "전라남도": 13,
    "전라북도": 14,
    "제주도": 15,
    "충청남도": 16,
    "충청북도": 17
    }
    #datetime형식으로 바꿔주는 함수
    def convert_to_datetime(timestamp_str):
                    timestamp_str1 = timestamp_str[:10]
                    timestamp_str2 = timestamp_str[11:]
                    timestamp_str = timestamp_str1 + " " + timestamp_str2
                    dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    return dt
    
    def to_datetime_(dt):
        data = datetime.strptime(dt, '%Y-%m')
        return data

    #통신해서 데이터 가져오는 코드
    selected_locals = st.multiselect(
        '보고싶은 지역들을 선택하세요!',
        regions_codes.keys())

    regions_graph_data = pd.DataFrame()

    if st.button('기존발전량 그래프 보기', key = 'button1'):
        try:
            for region in selected_locals:
                response = requests.get(my_url + 'record/' + str(regions_codes[region]))
    
                data1 = pd.DataFrame(response.json())
                

                data1['timestamp'] = data1['timestamp'].apply(convert_to_datetime)
                
                # 인덱스를 'datetime'으로 설정
                data1.set_index('timestamp', inplace=True)

                # 월별 발전량 합계 계산
                monthly_data1 = data1.resample('M').sum()
                monthly_data1['code'] = region

                #datetime YYYY-MM으로 변경
                monthly_data1.index = pd.to_datetime(monthly_data1.index).to_period('M')
                
                regions_graph_data = pd.concat([regions_graph_data, monthly_data1])
            
            
            regions_graph_data = regions_graph_data.reset_index()
            regions_graph_data.to_csv('/Users/admin/OneDrive/Desktop/asd/streamlit/data/서버강원도.csv',index=False)
            print(regions_graph_data.head())
            st.header('기존 태양광 발전량 그래프')
            st.line_chart(regions_graph_data, x='timestamp',y='production', color = 'code')

        except requests.exceptions.RequestException as req_err:
            print(f"요청 중 에러가 발생했습니다: {req_err}")
        except Exception as err:
            print(f"알 수 없는 에러가 발생했습니다: {err}")
    


    #원하는 지역코드들 선택(통신x)
    # selected_locals = st.multiselect(
    #     '보고싶은 지역들을 선택하세요!',
    #     locals,
    #     ['광주','경남','경북'])
    
    # filtered_data1 = data[data['code'].isin(selected_locals)]
    
    
    # ''
    # st.header('기존 태양광 발전량 그래프')
    # st.line_chart(filtered_data1,x='datetime',y='Solar_Power(MWh)', color = 'code')

    ''
    ''
    st.divider()
    #----------------------------------------------------------------------------한 지역 비교
    st.header('한 지역의 발전량과 예측 비교')


    #원하는 지역코드를 선택(예측 데이터가 없음)(통신x)
    # selected_local = st.selectbox(
    #     '보고싶은 지역을 선택하세요!',
    #     locals)
    
    # filtered_data2 = data.loc[data['code']==selected_local]
    # st.line_chart(filtered_data2,x='datetime',y='Solar_Power(MWh)', color = 'code')


    #통신해서 데이터 가져오는 코드
    selected_local = st.selectbox(
        '보고싶은 지역을 선택하세요!',
        regions_codes.keys())
    

    if st.button('한 지역 발전량 예측량 비교', key = 'button2'):
        #데이터 가져올 때 기존 + 예측 합치는데 code를 구별
        try:
            response = requests.get(my_url + 'record/' + str(regions_codes[selected_local]))
            
            data2 = pd.DataFrame(response.json())
            

            data2['timestamp'] = data2['timestamp'].apply(convert_to_datetime)
            
            # 인덱스를 'datetime'으로 설정
            data2.set_index('timestamp', inplace=True)

            # 월별 발전량 합계 계산
            monthly_data2 = data2.resample('M').sum()

            #datetime YYYY-MM으로 변경
            monthly_data2.index = pd.to_datetime(monthly_data2.index).to_period('M')

            #인덱스를 timestamp열로 만듬
            monthly_data2 = monthly_data2.reset_index().rename(columns={'index': 'timestamp'})
            print(monthly_data2.head())
            df1 = pd.DataFrame(monthly_data2.loc[:,monthly_data2.columns != 'predicted_production'])
            df2 = pd.DataFrame(monthly_data2.loc[:,monthly_data2.columns != 'production'])
            
            df1['code'] = '기존량'
            df2['code'] = '예측량'
            
            #예측량데이터 열 이름 바꾸기
            df2.rename(columns={'predicted_production' :'production' }, inplace=True)
            print(df1.head())
            graph_data = pd.concat([df1,df2])


            # graph_data['timestamp'] = graph_data['timestamp'].to_timestamp()

            #인덱스를 timestamp로 변경
            graph_data.set_index('timestamp', inplace=True)

            

            print(graph_data.head())
            st.line_chart(graph_data, y='production', color = 'code')
        except requests.exceptions.RequestException as req_err:
            print(f"요청 중 에러가 발생했습니다: {req_err}")
        except Exception as err:
            print(f"알 수 없는 에러가 발생했습니다: {err}")


    

    


#페이지3
elif choice=='그래프들':
    st.header('여러가지 그래프')

    tab1, tab2, tab3, tab4 = st.tabs(['막대','영역','점','테스트'])

    with tab1:
        st.header('막대그래프')
        st.bar_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    with tab2:
        st.header('영역그래프')
        st.area_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

    with tab3:
        st.header('점그래프')
        st.scatter_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')
    
    with tab4:
        st.header('테스트')
        a = pd.read_csv("./data/서버강원도.csv")
        st.line_chart(a,x='timestamp', y='production')

elif choice=='지역별 예측':      

    if 'region' not in st.query_params:
        st.header('원하는 지역을 클릭하면 밑에 예측량이 보여집니다')
    
    
    
        # 이미지태그가 안돼서 이미지를 base64로 인코딩
        file_ = open("./img/korea_map.png", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
    
        # korea.html을 불러온 후 이미지를 base64로 인코딩한것을 입력
        with open("./htmls/korea.html", 'r', encoding='utf-8') as file:
                korea_html_content = file.read()
                korea_html_content = korea_html_content.replace("data_url", data_url)

        # 변경된 html실행       
        st.html(korea_html_content)
    


    #지역 리스트
    regions = ['seoul', 'incheon', 'kyunggi', 'gangwon', 'chungnam',
               'chungbuk', 'daejeon', 'sejong', 'gyeongbuk', 'gyeongnam',
                'ulsan', 'daegu', 'jeonbuk', 'jeonnam', 'kwangju', 'busan',
                'jeju', 'ulleungdo_dokdo' ]
    
    #홈 이동버튼 만드는 함수
    def go_home():
        if st.button('홈으로 이동'):
            st.query_params.clear()
            st.experimental_rerun()

    #슬라이더를 만들어 불러올 데이터의 단위, 기간을 param로 반환해주는 함수
    def make_slider_and_params():
        #단위 정하기
        unit = st.selectbox(label='단위',options=['년','월','일'])
        
        if(unit == '년'):
            start, end = st.slider(
                label='기간', 
                min_value=datetime.strptime('2017','%Y'),
                max_value=datetime.strptime('2023','%Y'),
                value=[datetime.strptime('2017','%Y'), datetime.strptime('2023','%Y')], format='Y')
            
        elif(unit == '월'):
            start, end = st.slider(
                label='기간', 
                min_value=datetime.strptime('2017-01','%Y-%m'),
                max_value=datetime.strptime('2023-01','%Y-%m'),
                value=[datetime.strptime('2017-01','%Y-%m'), datetime.strptime('2023-01','%Y-%m')], format='Y-M')
            
        elif(unit == '일'):
            start, end = st.slider(
                label='기간', 
                min_value=datetime.strptime('2017-01-01','%Y-%m-%d'), 
                max_value=datetime.strptime('2023-01-01','%Y-%m-%d'),
                value=[datetime.strptime('2017-01-01','%Y-%m-%d'), datetime.strptime('2023-01-01','%Y-%m-%d')])
            
        else:
            st.warning('단위를 정해주세요.')
        
        return {'unit': unit, 'start': start, 'end': end}


    #지역별 그래프불러오기
    #처음에 쿼리문에 region이 없으므로 예외처리
    if 'region' not in st.query_params:
        st.warning("지역을 선택해주세요")

    
    elif st.query_params['region'] == 'seoul':
        param = make_slider_and_params()

        if st.button('요청'):
            response = requests.get(my_url + '/seoul',params=param)
            st.write(response.json())
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'incheon':
        st.warning(st.query_params['region'])
        go_home()
    
    elif st.query_params['region'] == 'kyunggi':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'gangwon':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'chungnam':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'chungbuk':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'daejeon':
        st.warning(st.query_params['region'])
        go_home()
    
    elif st.query_params['region'] == 'sejong':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'gyeongbuk':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'gyeongnam':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'ulsan':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'daegu':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'jeonbuk':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'jeonnam':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'kwangju':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'busan':
        st.warning(st.query_params['region'])
        go_home()

    elif st.query_params['region'] == 'jeju':
        st.warning(st.query_params['region'])
        go_home()
    
    elif st.query_params['region'] == 'ulleungdo_dokdo':
        st.warning(st.query_params['region'])
        go_home()

    else:
        st.warning('예상치못한 오류가 발생하였습니다.')