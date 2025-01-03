import uvicorn

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Float, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import configparser
import logging
import pandas as pd

#로깅 설정
logging.basicConfig(level=logging.INFO)
logging = logging.getLogger(__name__)


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
    logging.info("Database connection successful")
except Exception as e :
    logging.error(f"Database connection failed: {e}")
    raise RuntimeError("Failed to connect to the database")


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
        logging.error(f"Error creating table {table_name} : {e}")
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

@app.get("/record/{region_number}", response_model=list[dict])
def read_item2(region_number : int, db : session = Depends(get_db)) :
    table = create_table(region_number)
    query = select(table)
    try :
        results = db.execute(query).fetchall()
        if not results :
            raise HTTPException(status_code=404, detail="No records found")
        return [{"timestamp": row.timestamp, "production": row.production, "predicted_production": row.predicted_production} for row in results]
    except SQLAlchemyError as e :
        logging.error(f"Error fectching data for region {region_number} : {e}")
        raise HTTPException(status_code=500, detail="Internal server error")




@app.get("/")
def read_root():
    return {"Hello": "World"}


#페이지 2 : 예측 발전량과 가격을 제공하는 코드
@app.get("/predict_price/{region_number}/{date}")
def read_value(region_number : int, date):
    #데이터베이스에서 불러오기 -> 예측 발전량과 가격을 쌓아둔 데이터 -> 지역 별로 존재해야 함
    data = pd.DataFrame() #데이터라고 생각

    row_data = data.loc[data['date'] == date]
    return row_data['predict'], row_data['price']



@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


if __name__ == "__main__":
    uvicorn.run(app,host=my_host,port=my_port)
