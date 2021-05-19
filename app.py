from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio, os
from pyngrok import ngrok
import uvicorn
from feedback import feedback

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/upload-video')
async def upload(file: UploadFile = File(...)):
  filename = f'/content/{file.filename}'
  f = open(f'{filename}', 'wb')
  content = await file.read()
  f.write(content)
  
  fb = feedback(filename)
  return {"feedback": fb}

ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=8000)