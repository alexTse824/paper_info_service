import uvicorn
from starlette.requests import Request
from fastapi import FastAPI, Form, HTTPException

import settings
from utils import refresh_mirror_list, get_citation


app = FastAPI()

@app.post('/')
def search_paper(request: Request, keyword: str=Form(...)):
    return get_citation(keyword)


def run():
    refresh_mirror_list()
    uvicorn.run(
        app = app,
        host = settings.SERVER_HOST,
        port = settings.SERVER_PORT,
    )


if __name__ == "__main__":
    run()