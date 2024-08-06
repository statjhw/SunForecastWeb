import uvicorn
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()
my_host = "127.0.0.1"
my_port = 8000


#지역 리스트
regions = ['seoul', 'incheon', 'kyunggi', 'gangwon', 'chungnam',
            'chungbuk', 'daejeon', 'sejong', 'gyeongbuk', 'gyeongnam',
            'ulsan', 'daegu', 'jeonbuk', 'jeonnam', 'kwangju', 'busan',
            'jeju', 'ulleungdo_dokdo' ]

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

#기존발전량 불러오기
@app.get("/regions")
def read_regions_old(selected_locals: list):

    return {}#selected_locals에 해당하는 데이터

#한 지역의 기존발전량 + 예측발전량
@app.get("/region")
def read_regions_predict(regions_code : int):

    return {}#region_code에 해당하는 지역의 기존+예측


@app.get("/seoul")
def read_seoul(unit: str, start: datetime, end: datetime):

    if(unit == '년'):
        return f'서버에서 온 {start.year}~{end.year}의 년으로 된 서울데이터'
    elif (unit == '월'):
        return f'서버에서 온 {start:%Y-%m}~{end:%Y-%m}의 월으로 된 서울데이터'
    else:
        return f'서버에서 온 {start:%Y-%m-%d}~{end:%Y-%m-%d}의 일로 된 서울데이터'





@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

if __name__ == "__main__":
    uvicorn.run(app,host=my_host,port=my_port)