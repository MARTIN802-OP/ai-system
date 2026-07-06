from fastapi import FastAPI
from pydantic import BaseModel

from tool_server import create_file, run_command, read_file

app = FastAPI()

class FileRequest(BaseModel):
    path: str
    content: str

class CommandRequest(BaseModel):
    command: str
    cwd: str

class ReadRequest(BaseModel):
    path: str


@app.post("/create-file")
def api_create_file(data: FileRequest):
    return create_file(data.path, data.content)


@app.post("/run")
def api_run(data: CommandRequest):
    return run_command(data.command, data.cwd)


@app.post("/read-file")
def api_read(data: ReadRequest):
    content = read_file(data.path)
    return {"content": content}
