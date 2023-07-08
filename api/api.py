import numpy as np
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from sift import *


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

class ImagePair(BaseModel):
    image1: list
    image2: list

@app.post("/are_similar")
async def are_similar(image_pair: ImagePair):
    image1 = np.array(image_pair.image1).astype(np.uint8)
    image2 = np.array(image_pair.image2).astype(np.uint8)
    result = clasify(image1, image2)

    response = {"response": result}

    return response


if __name__ == '__main__':
    host = '0.0.0.0'
    uvicorn.run(app, host=host, port=8000)
