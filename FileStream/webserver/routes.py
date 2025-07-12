from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from FileStream.config import DOWNLOAD_DIR, PORT
import os
import uvicorn

app = FastAPI()

@app.get("/file/{file_name}")
async def serve_file(file_name: str):
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name)
    return HTMLResponse("<h2>File Not Found</h2>", status_code=404)

def run_webserver():
    uvicorn.run(app, host="0.0.0.0", port=PORT)
