from fastapi import FastAPI, Request, Response
import requests
from gateway.limiter import allow_request

app = FastAPI()

BACKEND_URL = "http://127.0.0.1:9000"

@app.get("/data")
def proxy_data(request: Request):
    client_ip = request.client.host
    key = f"rate:{client_ip}"

    if not allow_request(key):
        return Response(
            content='{"error":"rate limit exceeded"}',
            status_code=429,
            media_type="application/json"
        )

    r = requests.get(f"{BACKEND_URL}/data")
    return Response(content=r.content, status_code=r.status_code, media_type="application/json")
