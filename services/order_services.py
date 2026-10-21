from db.models.order import Order, OrderItem

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

async def create_order(db: AsyncSession, user_id: int):
    order = Order(
        user_id=user_id
    )
    db.add(order)

    await db.commit()
    await db.refresh(order)

    return order

async def add_item_order(db: AsyncSession, order_id: int, product_id: int, quantity: int, price: int):
    order_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    db.add(order_item)

    await db.commit()
    await db.refresh(order_item)

    return order_item


async def get_pending_order(db: AsyncSession, user_id: int):
    order = await db.scalar(
        select(Order)
        .where(
            Order.user_id == user_id, Order.status == "pending"
        )
    )
    return order

async def get_order_by_user_id(db: AsyncSession, user_id: int):
    order = await db.scalar(
        select(Order)
        .where(
            Order.user_id == user_id, Order.status == "pending"
        )
    )

    return order

async def add_total_price_order(db: AsyncSession, order_id: int, total_price: int):
    order = await db.scalar(
        select(Order)
        .where(
                Order.id == order_id
            )
        )
    
    order.total_price += total_price

    await db.commit()
    await db.refresh(order)


async def get_order_items_by_order_id(db: AsyncSession, order_id: int):
    order_items = await db.scalars(
        select(OrderItem)
        .where(
            OrderItem.order_id == order_id
        )
    )

    return order_items


async def delete_order_by_id(db: AsyncSession, order_id: int):
    order = await db.scalar(
        select(Order)
        .where(
            Order.id == order_id, Order.status == "pending"
        )
    )

    await db.delete(order)
    await db.commit()


async def change_status_order(db: AsyncSession, order_id: int):
    await db.execute(
        update(Order)
        .where(
                Order.id == order_id,
                Order.status == "pending"
            )
            .values(status="sending")
        )

    await db.commit()

async def get_orders(db: AsyncSession):

    result = await db.scalars(
        select(Order)
    )
    orders = result.all()

    return orders

async def get_orders_by_user_id(db: AsyncSession, user_id: int):
    result = await db.scalars(
        select(Order)
        .where(Order.user_id == user_id)
    )
    orders = result.all()

    return orders
