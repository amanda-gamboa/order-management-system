"""Initialize the application and register API routers."""

from fastapi import FastAPI

import app.models
from app.api.endpoints.customers import router as customer_router

app = FastAPI()

app.include_router(customer_router)
