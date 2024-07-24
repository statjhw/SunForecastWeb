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
from datetime import datetime
import altair as alt


# 데이터 준비
data = pd.read_csv("./data/합친거.csv")

st.line_chart(data,x='datetime',y='Solar_Power(MWh)', color = 'code')

# chart = alt.Chart(data).mark_circle().encode(x='datetime',y='Solar_Power(MWh)',color='code')
# st.altair_chart(chart)
# # 'timestamp' 열을 datetime 객체로 변환
# def convert_to_datetime(timestamp_str):
#     # 시간 부분이 24인 경우 00으로 변경하여 처리
#     if timestamp_str.endswith('-24'):
#         timestamp_str = timestamp_str[:-3] + '-00'
#         dt = datetime.strptime(timestamp_str, '%Y-%m-%d-%H') + pd.Timedelta(days=1)
#     else:
#         dt = datetime.strptime(timestamp_str, '%Y-%m-%d-%H')
#     return dt

# df['date'] = df['datetime'].apply(convert_to_datetime)

# # 'datetime' 열을 인덱스로 설정
# df.set_index('date', inplace=True)


