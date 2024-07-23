import streamlit as st
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='지역별 발전량',
    page_icon=':earth_americas:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def load_data():
    """Read solar power generation data from a CSV file."""
    data_df = pd.read_csv("./data/경상남도1.csv")
      # Ensure the Date column is in datetime format
    return data_df

data_df = load_data()
data_df['datetime'] = pd.to_datetime(data_df['datetime'], format='%Y-%m-%d-%H')
data_df['datetime'] = data_df['datetime'].apply(lambda x: x.to_pydatetime())

# Display the first few rows of the dataframe
st.write(data_df.head())

# Set the title that appears at the top of the page.
st.title(':earth_americas: 지역별 발전량')

# Add some spacing
st.write('')
st.write('')

# Filter the data based on the selected range
min_date = data_df['datetime'].min()
max_date = data_df['datetime'].max()

print(min_date)

from_date, to_date = st.slider(
        '몇년도를 보고싶으세요?',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    

# # Convert from_date and to_date back to datetime for filtering
# filtered_data_df = data_df[
#     (data_df['datetime'] >= from_date) & (data_df['datetime'] <= to_date)
# ]

# st.header('지역별 발전량', divider='gray')

# filtered_data_df.set_index('datetime', inplace=True)

# # Check if '시간' column exists before setting it as index
# st.line_chart(filtered_data_df.set_index('datetime')['Solar_Power(MWh)'])

# st.write('')
# st.write('')
