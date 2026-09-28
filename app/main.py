from fastapi import FastAPI

from app.routes.products import router as products_router
from app.routes.customers import router as customers_router
from app.routes.orders import router as orders_router

app = FastAPI(
    title="KohiCebu API",
    description="FastAPI service for the KohiCebu Digital Ordering and Management System.",
    version="1.0.0"
)


app.include_router(products_router)
app.include_router(customers_router)
app.include_router(orders_router)


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "KohiCebu FastAPI is running!",
        "system": "KohiCebu Digital Ordering and Management System"
    }