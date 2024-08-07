import uvicorn

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Float, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import configparser

from fastapi import FastAPI
from datetime import datetime


app = FastAPI()
my_host = "127.0.0.1"
my_port = 8001

config = configparser.ConfigParser()
config.read('config.ini')


database = config['database']['database']
host = config['database']['host']
port = config['database']['port']
user= config['database']['user']
password= config['database']['password']

try : 
    DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    metadata = MetaData()
    print("db connection")
except Exception as e :
    print(e)

tables_cache = {}

def create_table(region_number : int) :
    if region_number in tables_cache :
        return tables_cache[region_number]

    table_name = f"record_region{region_number}"
    table = Table(
        table_name, 
        metadata, 
        Column('timestamp', DateTime, primary_key=True),
        Column("production", Float),
        Column("predicted_production", Float),
    )
    try : 
        if not engine.dialect.has_table(engine, table_name) :
            metadata.create_all(engine, tables=[table])
    except SQLAlchemyError as e :
        print(f"Error creating table {table_name} : {e}")
    tables_cache[region_number] = table
    return table


def get_db() :
    db = SessionLocal()
    try : 
        yield db
    finally :
        db.close()

# 페이지1 : 지역의 발전량 record를 요청하면 보내주는 코드
from sqlalchemy import select 


# @app.get("/record", response_model=list[dict])
# def read_item1(region_numbers : list[int]) :
#     with SessionLocal() as session :

#         regions_data = []
#         return_datas = []

#         for i in len(region_numbers):
#             table = create_table(region_numbers[i])

#             query = select(table)
#             results = session.execute(query).fetchall()
#             regions_data.append(results)


#         return [{"timestamp": row.timestamp, "production": row.production, "predicted_production": row.predicted_production} for results in regions_data for row in results]




@app.get("/record/{region_number}", response_model=list[dict])
def read_item2(region_number : int) :
    with SessionLocal() as session :
        table = create_table(region_number)

        query = select(table)
        results = session.execute(query).fetchall()

        return [{"timestamp": row.timestamp, "production": row.production, "predicted_production": row.predicted_production} for row in results]
    



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
    