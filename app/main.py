"""Initialize the FastAPI application and register API routers."""

from fastapi import FastAPI

from app.api.endpoints.customers import router as customer_router
import app.models

app = FastAPI()

app.include_router(customer_router)
