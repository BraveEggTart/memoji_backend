
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from jwt import DecodeError, ExpiredSignatureError


def register_exceptions(app: FastAPI):

    @app.exception_handler(DecodeError)
    async def decode_handle(
        _: Request,
        exc: DecodeError
    ) -> JSONResponse:
        return JSONResponse(status_code=401, content=str(exc))

    @app.exception_handler(ExpiredSignatureError)
    async def expiredsignature_handle(
        _: Request,
        exc: ExpiredSignatureError
    ) -> JSONResponse:
        return JSONResponse(status_code=401, content=str(exc))
