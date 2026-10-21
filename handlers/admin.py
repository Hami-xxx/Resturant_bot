from services.user_service import get_user_by_tel_id
from services.product_service import (
    create_product,
    get_products,
    get_product_by_id, 
    update_product_name,
    update_product_price,
    update_product_description,
    update_available_product,
    delete_product_by_id
)
from services.order_services import get_orders

from db.database import AsyncSessionLocal

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.admin_key import admin_key, edit_key, edit_product_key, delete_product_key

from states.admin_states import ProductState, ProductEditStates

router = Router()

@router.message(Command("admin"))
async def admin_handler(message: Message):
    async with AsyncSessionLocal() as db:
        user = await get_user_by_tel_id(db=db,telegram_id=message.from_user.id)

    if not user or user.role != "admin":
        await message.answer("⛔ شما ادمین نیستید.")
        return

    await message.answer(
        "🔐 پنل مدیریت",
        reply_markup=admin_key
    )

@router.callback_query(F.data == "add_product")
async def product_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("نام محصول را وارد کنید:")
    await state.set_state(ProductState.waiting_for_name)
    await callback.answer()

@router.message(ProductState.waiting_for_name)
async def product_price(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("قیمت محصول را وارد کنید:")
    await state.set_state(ProductState.waiting_for_price)

@router.message(ProductState.waiting_for_price)
async def product_description(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("توضیحات مربوط به محصول را وارد کنید:")
    await state.set_state(ProductState.waiting_for_description)

@router.message(ProductState.waiting_for_description)
async def add_product(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    price = int(data.get("price"))

    async with AsyncSessionLocal() as db:
        product = await create_product(
            db=db,
            name=name,
            price=price,
            description=message.text)

    await message.answer(
        f"محصول ثبت شد ✅\n\n"
        f"نام: {product.name}\n"
        f"قیمت: {product.price:,} تومان\n"
        f"توضیحات: {product.description}"
    )

    await state.clear()

@router.callback_query(F.data == "products")
async def list_products(callback: CallbackQuery):
    async with AsyncSessionLocal() as db:
        products = await get_products(db=db)

    if not products:
        await callback.message.answer("محصولی پیدا نشد 😕")
        return

    product_info = "📦 محصولات:\n\n"

    for product in products:
        product_info += f"""
🏷️ نام محصول: {product.name}
💰 قیمت: {product.price:,} تومان
📝 توضیحات: {product.description if product.description else "❌ توضیحی برای این محصول ثبت نشده است."}
----------------------------------------------------------------------
        """
    await callback.message.answer(product_info)

@router.callback_query(F.data == "edit")
async def list_products_edit(callback: CallbackQuery):
    async with AsyncSessionLocal() as db:
        products = await get_products(db=db)

    if not products:
        await callback.message.answer("محصولی پیدا نشد 😕")
        return

    await callback.message.answer(
        "📦 محصولات:",
        reply_markup=edit_product_key(products=products)
        )

@router.callback_query(F.data.startswith("edit_product_id:"))
async def edit_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as db:
        product = await get_product_by_id(db=db,product_id=product_id)

    await state.update_data(product_id=product_id)

    await callback.message.answer(
f"""
🏷️ نام محصول: {product.name}
💰 قیمت: {product.price:,}
📝 توضیحات: {product.description if product.description else "❌ توضیحی برای این محصول ثبت نشده است."}
📋موجودی: {"موجوداست" if product.is_available else "ناموجود"}
""",
    reply_markup=edit_key
    )

@router.callback_query(F.data.startswith("edit_"))
async def start_editing(callback: CallbackQuery, state: FSMContext):
    field_to_edit = callback.data.split("_")[1]
    
    await state.update_data(
        field=field_to_edit
    )
    await state.set_state(ProductEditStates.editing_field)
    
    messages = {
        "name": "لطفاً نام جدید را وارد کنید:",
        "price": "لطفاً قیمت جدید را وارد کنید (فقط عدد):",
        "available": "وضعیت را وارد کنید (موجود/ناموجود):"
    }
    await callback.message.answer(messages.get(field_to_edit, "لطفاً مقدار را وارد کنید:"))
    await callback.answer()

@router.message(ProductEditStates.editing_field)
async def process_all_edits(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    field = data.get("field")
    
    new_value = message.text
    
    try:
        async with AsyncSessionLocal() as db:
  
            if field == "name":
                await update_product_name(db, product_id, new_value)
                msg = "نام محصول تغییر کرد. ✅"
            
            elif field == "price":
                price_val = int(new_value) 
                await update_product_price(db, product_id, price_val)
                msg = "قیمت محصول تغییر کرد. ✅"

            elif field == "description":
                await update_product_description(db, product_id, new_value)
                msg = "توضیحات مربوط ب محصول تغییر کرد. ✅"
            
            elif field == "available":
                is_avail = True if new_value == "موجود" else False
                await update_available_product(db, product_id, is_avail)
                msg = "وضعیت موجودی تغییر کرد. ✅"

            await message.answer(msg)
            await state.clear()

    except ValueError:
        await message.answer("❌ فرمت ورودی اشتباه است! دوباره تلاش کنید.")
    except Exception as e:
        await message.answer("❌ خطایی رخ داد.")

@router.callback_query(F.data == "delete")
async def list_products_delete(callback: CallbackQuery):
    async with AsyncSessionLocal() as db:
        products = await get_products(db=db)

    if not products:
        await callback.message.answer("محصولی پیدا نشد 😕")
        return

    await callback.message.answer(
        "📦 محصولات:",
        reply_markup=delete_product_key(products=products)
        )

@router.callback_query(F.data.startswith("delete_product_id:")) 
async def delete_product(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    async with AsyncSessionLocal() as db:
        product = await get_product_by_id(db=db,product_id=product_id)

        await delete_product_by_id(db=db, product_id=product_id)

        await callback.answer("محصول با موفقیت حذف شد 🗑")

@router.callback_query(F.data == "orders")
async def orders_list(callback: CallbackQuery):
    async with AsyncSessionLocal() as db:
        orders = await get_orders(db=db)

    orders_text = "📜 *سفارش ها*\n\n"

    order_status = "در انتظار" if order.status == "pending" else "درحال ارسال" 

    for order in orders:
        orders_text += f"""
📋 شناسه سفارش: {order.id}
🧾 وضعیت سفارش: {order_status}
📅 تاریخ سفارش: {order.created_at}
💰 مبلغ کل: {order.total_price}
"""
    await callback.message.answer(orders_text)