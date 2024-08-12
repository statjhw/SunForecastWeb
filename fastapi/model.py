import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, mean_absolute_error

def kmeans_process(region_number, data) :
    """
        input :
            region_number : 어떤 지역의 kmeans모델을 넣을 것인지 판단하기 위해서 
            들어오는 데이터 : 일사와 일조만 
        output : 
            kmeans클러스터, region_number
    """
    #지역 번호와 맞는 지역 이름 매칭
    regions_codes = {
    1:"강원도", 
    2:"경기도",
    3:"경상남도",
    4:"경상북도",
    5:"광주시",
    6:"대구시",
    7:"대전시",
    8:"부산시",
    9:"서울시",
    10:"세종시", 
    11:"울산시",
    12:"인천시",
    13:"전라남도",
    14:"전라북도", 
    16:"충청남도", 
    17:"충청북도" 
    }

    optimal_clusters = 3 #최적의 cluster 수

    #kmeans model 불러오기
    region_name = regions_codes[region_number]
    kmeans_model = joblib.load(f"fastapi/models/kmeans/kmeans_model_{region_name}.joblib")

    #데이터 스케일링 
    scaler = RobustScaler()
    #일사, 일조를 이용해서 kmeans 군집화 진행
    data_scaled = scaler.fit_transform(data[['일사', '일조']])

    label = kmeans_model.predict(data_scaled) #label
    return label, region_number


#날씨 데이터의 cluster, year, month, day, dayofweek, 
# lag_1, lag_2, rolling_mean 부착 필요



#선택지1 : 하나의 값만 리턴 
#장점 : 나중에 컨트롤하기 쉬움
#단점 : 새롭게 model불러오기, 데이터 처리 등이 반복된다.
#선택지2 : 들어온 모든 데이터에대해서 처리
#장점 : 속도 상승, 메모리 절약
#단점 : 모든 값을 리턴하기 때문에 컨트롤 하기 어렵다
def lightgbm_process(df, region_number) :
    """
        선택지2를 활용하여 모든 데이터에 대해 예측량 리턴
        input : 여러가지 변수( cluster, year, month, day, dayofweek, 
                lag_1, lag_2, rolling_mean)가 붙은 데이터 프레임
        output : 각 행에 맞는 예측량 시퀸스
    """
    regions_codes = {
    1:"강원도", 
    2:"경기도",
    3:"경상남도",
    4:"경상북도",
    5:"광주시",
    6:"대구시",
    7:"대전시",
    8:"부산시",
    9:"서울시",
    10:"세종시", 
    11:"울산시",
    12:"인천시",
    13:"전라남도",
    14:"전라북도", 
    16:"충청남도", 
    17:"충청북도" 
    }
    
    region_name = regions_codes[region_number]

    #cluster 0,1,2 model return
    lightgbm0_model = joblib.load(f"fastapi/models/lightgbm/lightgbm_cluster_0_{region_name}.joblib")
    lightgbm1_model = joblib.load(f"fastapi/models/lightgbm/lightgbm_cluster_1_{region_name}.joblib")
    lightgbm2_model = joblib.load(f"fastapi/models/lightgbm/lightgbm_cluster_2_{region_name}.joblib")

    predict_array = []

    #각 cluster의 정보를 얻기 위한 데이터
    labels = df['Cluster']
    #모델에 맞도록 데이터 처리
    X_lightgbm = df.drop(columns=['Solar_Power(MWh)', 'date']) #들어오는 데이터 형식에 맞도록 데이터 처리
    y_lightgbm = df['Solar_Power(MWh)'].values.reshape(-1, 1) #이과정 고려해봐함 아니면 내장으로 있을 수 있음

    scaler_X = RobustScaler()
    scaler_Y = RobustScaler()

    X_lightgbm_scaled = scaler_X.fit_transform(X_lightgbm)
    y_lightgbm_scaled = scaler_y.fit_transform(y_lightgbm)

    for label, row_data in zip(labels, X_lightgbm_scaled) :
        
        predict_value = 0
        
        if label == 0 :
            predict_value = lightgbm0_model.predict(row_data)
        elif label == 1 :
            predict_value = lightgbm1_model.predict(row_data)
        elif label == 2 : 
            predict_value = lightgbm2_model.predict(row_data)
        else : 
            pass
        
        predict_value = scaler_Y.inverse_transform(predict_value.reshape(-1, 1))

        if predict_value < 0 :
            predict_value = 0
        
        predict_array.append(predict_value)
    
    return predict_array 


def price_predict() :
    """
        태양광 예측량을 토대로 가격을 예측하는 함수

        
    """