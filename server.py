import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CommandRequest(BaseModel):
    command: str

@app.get("/")
def read_root():
    return {"status": "MCP FFmpeg Server online"}

@app.post("/run-ffmpeg")
def run_ffmpeg(req: CommandRequest):
    try:
        # Ejecuta un comando seguro de ffmpeg recibido desde la nube
        # Nota: ajusta esto según los comandos específicos que necesites procesar
        result = subprocess.run(
            req.command, shell=True, capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stderr)
        return {"output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
