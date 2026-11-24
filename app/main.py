"""Initialize the application and register API routers."""

from fastapi import FastAPI

import app.models
from app.api.endpoints.customers import router as customer_router
from app.api.endpoints.products import router as product_router

app = FastAPI()

app.include_router(customer_router)
app.include_router(product_router)
