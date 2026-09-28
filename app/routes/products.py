from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


class Product(BaseModel):
    product_id: int
    product_name: str = Field(..., min_length=1, max_length=100)
    description: str = ""
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., ge=0)
    image_url: str | None = None
    stock_quantity: int = Field(..., ge=0)
    is_available: bool = True


products = [
    Product(
        product_id=1,
        product_name="Flat White",
        description="Smooth espresso with steamed milk.",
        category="Coffee",
        price=150.00,
        image_url=None,
        stock_quantity=20,
        is_available=True
    ),
    Product(
        product_id=2,
        product_name="Matcha Cream",
        description="Creamy matcha drink topped with a smooth cream layer.",
        category="Matcha",
        price=170.00,
        image_url=None,
        stock_quantity=15,
        is_available=True
    ),
    Product(
        product_id=3,
        product_name="Cookies",
        description="Freshly baked cookies from KohiCebu.",
        category="Cookies",
        price=95.00,
        image_url=None,
        stock_quantity=25,
        is_available=True
    )
]


@router.get("/", response_model=list[Product])
async def get_products():
    return products


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):

    for product in products:

        if product.product_id == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found."
    )