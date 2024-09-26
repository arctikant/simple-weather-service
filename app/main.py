from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.main import api_router_v1
from app.core.config import settings
from app.schemas.api import ResponseStatus

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):  # noqa: ARG001
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'code': ResponseStatus.ERROR.value,
            'message': str(exc.detail),
        },
    )


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(api_router_v1, prefix=settings.API_V1_STR)
