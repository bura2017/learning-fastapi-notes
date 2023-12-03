from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, Response
from fastapi.exception_handlers import http_exception_handler
from app.routes import all, auth, items
from app.exceptions import CustomException, HTTPException, \
    RequestValidationError, custom_request_validation_exception_handler
from app.models.all import ErrorResponse
import time


import logging


api_router = APIRouter()
api_router.include_router(all.router)
api_router.include_router(auth.app)
api_router.include_router(items.app, prefix='/items')


app = FastAPI()
app.include_router(api_router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    # if using just Response class then content must have 'encode' attribute
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
        headers={"Nice-But-No": "True"}
    )


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    logging.error("Common Handler Exception is called")
    # In this place raise exc is not used and results in Internal Server Error
    # response = JSONResponse()
    # response.headers["Nice-But-Yes"] = "False"
    # Can not return exc as 'HTTPException' object is not callable
    # exc.headers["Nice-But-Yes"] = "False"
    exc.headers = {"Nice-But-Yes": "False"}
    # return exc
    return await http_exception_handler(request, exc)

app.add_exception_handler(RequestValidationError, custom_request_validation_exception_handler)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response