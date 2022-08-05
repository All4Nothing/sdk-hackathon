from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
import numpy as np
from pydantic import BaseModel

class Webtoon(BaseModel):
    genre: str
    description: str

class Fish(BaseModel):
    length: int

# 모델 불러오기
model_path = './models/knnpickle_file'
model = load_model(model_path)

input_shape = model.layers[0].input_shape

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/webtoon/")
async def create_webtoon(webtoon: Webtoon):
    return webtoon

@app.post("/fish/")
async def create_webtoon(fish: Fish):
    return fish

@app.get("/prediction/{item_id}")
async def read_item(item_id: int):
    prediction = model.predict(fish)
    return {"result": int(prediction)}