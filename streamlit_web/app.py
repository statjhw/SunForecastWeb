import streamlit as st
import pandas as pd

#시각화를 위해서 Matplotlib 사용
import matplotlib.pyplot as plt

df=pd.read_csv("C:/Users/altmx/OneDrive/바탕 화면/ACC_project/경상남도_시간별발전량.csv")
#발전량의 NAN값을 0으로 변경
df['Solar_Power(MWh)'] = df['Solar_Power(MWh)'].fillna(0)

#헤더와 서브타이틀
st.title("경상남도 태양광 발전량 정보")

#연도 선택
selected_year = st.selectbox('연도를 선택하세요',[''] + list(df['Date'].apply(lambda x: pd.to_datetime(x).year).unique()))

if selected_year:
    min_date=pd.to_datetime(f'{selected_year}-01-01')
    max_date=pd.to_datetime(f'{selected_year}-12-31')
    #선택한 연도의 날짜 범위 설정
    start_date = st.date_input('시작 날짜', min_date,min_value=min_date,max_value=max_date)
    end_date = st.date_input('종료 날짜', max_date,min_value=min_date,max_value=max_date)

    #날짜를 datetime 형식으로 변환
    start_date=pd.to_datetime(start_date)
    end_date=pd.to_datetime(end_date)

    #사용자가 선택한 날짜의 범위를 맞춰서 필터링
    df_filtered=df[(pd.to_datetime(df['Date'])>=start_date) & (pd.to_datetime(df['Date'])<=end_date)]

    st.subheader(f'{selected_year}년 데이터')
    st.dataframe(df_filtered)

    df_filtered=df_filtered.set_index('Date')
    df_filtered.index = pd.to_datetime(df_filtered.index)
    daily_power=df_filtered['Solar_Power(MWh)'].resample('D').sum()

    #시각화
    st.subheader('시간별 발전량 시각화')
    fig, ax = plt.subplots()
    daily_power.plot(ax=ax)
    ax.set_xlabel('time')
    ax.set_ylabel('Generation(MWh)')
    ax.set_title(f'{selected_year} GN Photovoltaic Power Generation')

    st.pyplot(fig)




