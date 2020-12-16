import uvicorn
from starlette.requests import Request
from fastapi import FastAPI, Form, HTTPException

import settings
from crawler import BaiduPaperInfoCrawler


app = FastAPI()

@app.post('/paper')
def search_paper(request: Request, engine: str=Form(...), keyword: str=Form(...)):
    if engine == 'baidu':
        crawler = BaiduPaperInfoCrawler(keyword)
    else:
        raise HTTPException(404, 'Wrong search engine')
    return crawler.get_paper_cit()

if __name__ == "__main__":
    uvicorn.run(
        app = app,
        host = settings.SERVER_HOST,
        port = settings.SERVER_PORT,
    )

