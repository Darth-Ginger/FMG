from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

# Static DEBUG
DEBUG: bool = True

app = FastAPI(title="FMG_API",
	    	version="0.1.0",
		openapi_url="/openapi.json",
		servers=[{"url": "http://10.20.0.40:8100"}],
		debug=DEBUG)

# Register Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
	return {"message": "Hello, World!"}
