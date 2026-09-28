from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.routes.customers import customers
from app.routes.products import products


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


class Order(BaseModel):
    order_id: int
    user_id: int
    product_id: int
    quantity: int = Field(..., ge=1)
    total_amount: float = Field(..., ge=0)
    order_status: str = "PENDING"
    payment_status: str = "UNPAID"


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., ge=1)

class OrderUpdate(BaseModel):
    quantity: int = Field(..., ge=1)    


orders = [
    Order(
        order_id=1,
        user_id=1,
        product_id=1,
        quantity=2,
        total_amount=300.00,
        order_status="PREPARING",
        payment_status="PAID"
    ),
    Order(
        order_id=2,
        user_id=2,
        product_id=2,
        quantity=1,
        total_amount=170.00,
        order_status="PENDING",
        payment_status="UNPAID"
    )
]


@router.get("/", response_model=list[Order])
async def get_orders():
    return orders


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int):

    for order in orders:

        if order.order_id == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found."
    )


@router.post("/", response_model=Order, status_code=201)
async def create_order(order_data: OrderCreate):

    # Find the customer
    customer = next(
        (
            customer
            for customer in customers
            if customer.user_id == order_data.user_id
        ),
        None
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    # Find the product
    product = next(
        (
            product
            for product in products
            if product.product_id == order_data.product_id
        ),
        None
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    # Check product availability
    if not product.is_available:
        raise HTTPException(
            status_code=400,
            detail="Product is not available."
        )

    # Check stock
    if order_data.quantity > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available."
        )

    # Calculate total amount
    total_amount = product.price * order_data.quantity

    # Generate new order ID
    new_order_id = max(order.order_id for order in orders) + 1

    # Create the new order
    new_order = Order(
        order_id=new_order_id,
        user_id=order_data.user_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_amount=total_amount,
        order_status="PENDING",
        payment_status="UNPAID"
    )

    orders.append(new_order)

    return new_order

@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order_data: OrderUpdate):

    # Find the order
    order = next(
        (
            order
            for order in orders
            if order.order_id == order_id
        ),
        None
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found."
        )

    # Find the product
    product = next(
        (
            product
            for product in products
            if product.product_id == order.product_id
        ),
        None
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    # Check product availability
    if not product.is_available:
        raise HTTPException(
            status_code=400,
            detail="Product is not available."
        )

    # Check stock
    if order_data.quantity > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available."
        )

    # Update quantity
    order.quantity = order_data.quantity

    # Recalculate total
    order.total_amount = product.price * order_data.quantity

    return order

@router.delete("/{order_id}")
async def delete_order(order_id: int):

    # Find the order
    order = next(
        (
            order
            for order in orders
            if order.order_id == order_id
        ),
        None
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found."
        )

    # Remove the order
    orders.remove(order)

    return {
        "success": True,
        "message": f"Order #{order_id} deleted successfully."
    }