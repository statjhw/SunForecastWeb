import streamlit as st
import pandas as pd

#시각화를 위해서 Matplotlib 사용
import matplotlib.pyplot as plt

df_spring=pd.read_csv("C:/Users/altmx/OneDrive/바탕 화면/ACC_project/경상남도_일,달,계절별 정보/2017_경상남도_봄_발전량.csv")
df_summer=pd.read_csv("C:/Users/altmx/OneDrive/바탕 화면/ACC_project/경상남도_일,달,계절별 정보/2017_경상남도_여름_발전량.csv")
df_fall=pd.read_csv("C:/Users/altmx/OneDrive/바탕 화면/ACC_project/경상남도_일,달,계절별 정보/2017_경상남도_가을_발전량.csv")
df_winter=pd.read_csv("C:/Users/altmx/OneDrive/바탕 화면/ACC_project/경상남도_일,달,계절별 정보/2017_경상남도_겨울_발전량.csv")

total_spring = df_spring['Solar_Power(MWh)'].sum()
total_summer = df_summer['Solar_Power(MWh)'].sum()
total_fall = df_fall['Solar_Power(MWh)'].sum()
total_winter = df_winter['Solar_Power(MWh)'].sum()

st.title("GN seasonal solar power generation inform")

# 계절별 총 발전량 막대 그래프
st.subheader("Comparison of total power generation by season")
seasons = ['Winter', 'Fall', 'Summer', 'Spring']
totals = [total_winter, total_fall, total_summer, total_spring]

fig, ax = plt.subplots()
ax.bar(seasons, totals, color=['green', 'yellow', 'orange', 'blue'])
ax.set_xlabel('wether')
ax.set_ylabel('Total Generation (MWh)')
ax.set_title('Comparison of total power generation by season')

st.pyplot(fig)

# 계절 선택
selected_season = st.selectbox('Select Wether', ['spring', 'summer', 'fall', 'winter'])

# 선택한 계절에 따라 데이터프레임 설정
if selected_season == 'spring':
    df_season = df_spring
elif selected_season == 'summer':
    df_season = df_summer
elif selected_season == 'fall':
    df_season = df_fall
else:
    df_season = df_winter

# 데이터프레임 표시
st.subheader(f'{selected_season} Data')
st.dataframe(df_season)

# 'Date' 열을 datetime 형식으로 변환
df_season['Date'] = pd.to_datetime(df_season['Date'])

# 시간별 발전량 합계 계산
df_season = df_season.set_index('Date')
daily_power = df_season['Solar_Power(MWh)'].resample('D').sum()

# 시각화
st.subheader(f'{selected_season} Visualization of power generation by hour')
fig, ax = plt.subplots()
daily_power.plot(ax=ax)
ax.set_xlabel('Time')
ax.set_ylabel('Generation (MWh)')
ax.set_title(f'{selected_season} GN solar power generation')

st.pyplot(fig)


