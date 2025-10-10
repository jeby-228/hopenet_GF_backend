from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .logger import get_logger
from .routers.item_router import item_router
from .routers.task_router import task_router
from .routers.user_router import user_router
from .settings.app_setting import app_settings


logger = get_logger()


@asynccontextmanager
async def _lifespan(app: FastAPI):
    yield


app = FastAPI(
    lifespan=_lifespan,
    title=app_settings.PROJECT_NAME,
    openapi_url=f'{app_settings.API_V1_STR}/openapi.json',
    swagger_ui_parameters={  # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/#parameters
        'displayRequestDuration': True,
        # display of vendor extension (x-) fields and values for Operations, Parameters, Responses, and Schema
        'showExtensions': True,
        'docExpansion': 'none',
    },
)


logger.info(f'allow_origins: {app_settings.all_cors_origins}')
if app_settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


app.include_router(task_router, prefix=app_settings.API_V1_STR)
app.include_router(user_router, prefix=app_settings.API_V1_STR)

app.include_router(item_router, prefix=app_settings.API_V1_STR, deprecated=True)


app.include_router(task_router, deprecated=True)
app.include_router(user_router, deprecated=True)
