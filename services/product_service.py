from db.models.product import Product

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

async def get_products(db: AsyncSession):

    result = await db.scalars(
        select(Product)
    )
    products = result.all()

    return products

async def get_product_by_id(db: AsyncSession, product_id: int):
    product = await db.scalar(
        select(Product)
        .where(Product.id == product_id)
    )

    return product

async def create_product(db: AsyncSession, name: str, price: int, description: str):
    product = Product(
        name=name,
        price=price,
        description=description
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product

async def update_product_name(db: AsyncSession, product_id: int, new_name: str):
    product = await db.execute(
        update(Product)
        .where(
                Product.id == product_id
            )
            .values(name=new_name)
        )

    await db.commit()

async def update_product_price(db: AsyncSession, product_id: int, new_price: int):
    product = await db.execute(
        update(Product)
        .where(
                Product.id == product_id
            )
            .values(price=new_price)
        )

    await db.commit()

async def update_product_description(db: AsyncSession, product_id: int, new_description: str):
    product = await db.execute(
        update(Product)
        .where(
                Product.id == product_id
            )
            .values(description=new_description)
        )

    await db.commit()

async def update_available_product(db: AsyncSession, product_id: int, new_available: bool):
    product = await db.execute(
        update(Product)
        .where(
                Product.id == product_id
            )
            .values(is_available=new_available)
        )

    await db.commit()

async def delete_product_by_id(db: AsyncSession, product_id: int):
    product =  await db.scalar(
        select(Product)
        .where(
            Product.id == product_id
        )
    )

    await db.delete(product)
    await db.commit()