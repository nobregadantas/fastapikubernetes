from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from starlette.responses import Response

app = FastAPI()

# Criando uma métrica de contagem de requisições
http_requests_total = Counter("http_requests_total", "Total de requisições HTTP")

@app.get("/metrics")
def get_metrics():
    return Response(content=generate_latest(), media_type="text/plain")

@app.get("/")
def read_root():
    http_requests_total.inc()
    return {"message": "API rodando!"}
