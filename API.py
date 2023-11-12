import uvicorn
from fastapi import FastAPI
from Image_Caption import Image_Caption
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

model = Image_Caption()

class Datapassin(BaseModel):
    imgBase64: str

@app.get('/')
def index():
    return {
        'message': 'Hello world'
    }

@app.post('/predict')
async def predict(datapassin: Datapassin):
    generated_caption = model.model_run(datapassin.imgBase64)
    return {
        'generated_caption': generated_caption
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
