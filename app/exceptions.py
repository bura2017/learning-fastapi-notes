from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class CustomException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=418, detail=detail)


# кастомный обработчик исключения для RequestValidationError (Pydantic validation errors)
async def custom_request_validation_exception_handler(request, exc: RequestValidationError):
    content_errs = []
    for er in exc.errors():
        content_errs.append(er['msg'])
    return JSONResponse(
        status_code=422,
        content={"message": "Custom Request Validation Error", "errors": content_errs}
    )

