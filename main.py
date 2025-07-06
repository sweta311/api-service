import os
import json
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Request Inspector API",
    description="A simple API that inspects HTTP requests and exposes Prometheus metrics.",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app)

@app.api_route("/api", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def inspect_request(request: Request):
    """
    Inspects the incoming request and returns its details as plain text.
    """
    headers_str = "\n".join(f"{key}: {value}" for key, value in request.headers.items())

    body_str = ""
    try:
        body_json = await request.json()
        body_str = json.dumps(body_json, indent=2)
    except json.JSONDecodeError:
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8', errors='ignore')
        if not body_str:
            body_str = "[No Body]"

    response_text = f"""Welcome to our demo API, here are the details of your request:
***Headers***:
{headers_str}

***Method***:
{request.method}

***Body***:
{body_str}
"""

    return PlainTextResponse(content=response_text)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
