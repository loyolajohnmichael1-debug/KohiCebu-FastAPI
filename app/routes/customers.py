from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


class Customer(BaseModel):
    user_id: int
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = None
    role: str = "CUSTOMER"
    is_active: bool = True


customers = [
    Customer(
        user_id=1,
        full_name="Juan Dela Cruz",
        email="juan@example.com",
        phone="09171234567",
        role="CUSTOMER",
        is_active=True
    ),
    Customer(
        user_id=2,
        full_name="Maria Santos",
        email="maria@example.com",
        phone="09181234567",
        role="CUSTOMER",
        is_active=True
    )
]


@router.get("/", response_model=list[Customer])
async def get_customers():
    return customers


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):

    for customer in customers:

        if customer.user_id == customer_id:
            return customer

    raise HTTPException(
        status_code=404,
        detail="Customer not found."
    )