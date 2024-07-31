import uvicorn
from fastapi import FastAPI

app = FastAPI()
my_host = "127.0.0.1"
my_port = 8000

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/seoul")
def read_seoul():
    return "서버에서온 서울데이터"

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

if __name__ == "__main__":
    uvicorn.run(app,host=my_host,port=my_port)