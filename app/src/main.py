
from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from starlette.responses import Response

app = FastAPI()
hits = Counter('hello_hits_total','Total hello hits')

@app.get("/")
def home():
    hits.inc()
    return {"msg": "hello from AWS"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
