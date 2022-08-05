from fastapi import FastAPI, UploadFile, File, Request
import numpy as np
from pydantic import BaseModel
import tensorflow as tf
import keras
import json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
import pandas as pd
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse



class Webtoon(BaseModel):
    description: str

# 모델 불러오기
model_3 = tf.keras.models.load_model('./models/best_model_3.h5')
model_10 = tf.keras.models.load_model('./models/best_model_10.h5')

input_shape = model_3.layers[0].input_shape

app = FastAPI()

origins = [
    "frontend-app.yourdomain.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")


@app.get("/")
async def root():
    return {"message": "Hello World"}

'''
@app.post("/webtoon/{description}")
async def create_webtoon(description: str):

    return description
'''
@app.post("/webtoon/{description}")
async def webtoon_prediction(description: str):
    with open('wordIndex.json') as json_file:
            word_index = json.load(json_file)
            tokenizer = Tokenizer()
            tokenizer.word_index = word_index

    def SentenceToToken(sentence):
        okt = Okt()
        tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', '을', '되다', '이야기']
        stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
        token=[]
        token.append(tokenizer.texts_to_sequences(stopwords_removed_sentence))
        token=pad_sequences(token, maxlen=55)
        token=token.reshape(1,55)
        return token

    def SelectNIceWebtoon(f_var, g_var):
        formatOption = rating['format'] == f_var
        genreOption = rating['genre'] == g_var
        selectedWebtoon = rating[formatOption & genreOption]
        sortedWebtoon=selectedWebtoon.sort_values(['rating'])
        NiceSortedWebtoon=sortedWebtoon[-5:]
        return NiceSortedWebtoon[['title','rating']]

    rating=pd.read_csv('./rating.csv')

    Token = SentenceToToken(description)

    f_var = model_3.predict(Token).argmax()
    g_var = model_10.predict(Token).argmax()

    prediction = SelectNIceWebtoon(f_var, g_var)

    return {"recommendation": prediction}

'''
@app.post("/fish/{fish_length}")
async def create_webtoon(fish: Fish):
    return fish


@app.get("/prediction/{fish_length}")
async def read_item(fish_length: int):
    prediction = model.predict(fish_length)
    return {"fish length":fish_length, "result": int(prediction)}
'''

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )