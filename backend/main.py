from fastapi import FastAPI
from pydantic import BaseModel

from agents.url_agent import URLAgent

app = FastAPI(title="TrustLens API")

agent = URLAgent()


class URLRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "project": "TrustLens",
        "status": "Running",
        "version": "1.0"
    }


@app.post("/analyze")
def analyze(data: URLRequest):

    result = agent.analyze(data.url)

    return {
        "url": data.url,
        **result
    }