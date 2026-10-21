from services.product_service import get_products, get_product_by_id

from db.database import AsyncSessionLocal

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.user_key import product_key, select_product_key


router = Router()

@router.message(F.text == "📦 محصولات")
async def product_handler(message:Message):
    async with AsyncSessionLocal() as db:
        products = await get_products(db=db)

        if not products:
            await message.answer("محصولی پیدا نشد 😕")
            return

        await message.answer(
            "📦 محصولات:",
            reply_markup=product_key(products=products)
            )

@router.callback_query(F.data.startswith("product:"))
async def product_detail(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as db:
        product = await get_product_by_id(db=db,product_id=product_id)

    price_info = f"{product.price:,} تومان" if product.is_available else "❌ اتمام موجودی"
    description_info = f"{product.description}" if product.description else "❌ توضیحی برای این محصول ثبت نشده است."
    await callback.message.answer(
f"""
╔══════════════════════════════════════════════════
║ 🏷️ نام محصول: {product.name}
║ 💰 قیمت: {price_info}
║ 📝 توضیحات: {description_info}
╚══════════════════════════════════════════════════
""",
    reply_markup=select_product_key(product_id=product_id)
    )

@router.callback_query(F.data == "back_to_products")
async def back_to_menu(callback: CallbackQuery):
        async with AsyncSessionLocal() as db:
            products = await get_products(db=db)

        await callback.message.answer(
            "📦 محصولات:",
            reply_markup=product_key(products=products)
            )
