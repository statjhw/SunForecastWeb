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

@app.get("/")
def read_root():
    return {"Hello": "World"}


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