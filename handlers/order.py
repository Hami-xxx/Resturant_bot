from services.user_service import get_user_by_tel_id
from services.product_service import get_product_by_id
from services.order_services import (
    create_order,
    add_item_order, 
    get_pending_order,
    get_order_by_user_id, 
    get_order_items_by_order_id, 
    delete_order_by_id,
    change_status_order,
    add_total_price_order
)

from db.database import AsyncSessionLocal

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.user_key import confirm_order_key, cart_key

from states.product_state import ProductState 

router = Router()

@router.callback_query(F.data.startswith("product_id:"))
async def start_ordering(callback : CallbackQuery, state : FSMContext):
    product_id = int(callback.data.split(":")[1])
    
    await state.update_data(product_id=product_id)
    await state.set_state(ProductState.waiting_for_quantity)

    await callback.message.answer("تعداد مورد نظر محصول را وارد کنید:")

@router.message(ProductState.waiting_for_quantity)
async def get_quantity(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    
    async with AsyncSessionLocal() as db:
        product = await get_product_by_id(db=db,product_id=product_id)
    if not product.is_available:
        await message.answer("❌ اتمام موجودی")
        return
    
    try:
        quantity = int(message.text)
    except (ValueError, TypeError):
        await message.answer("❌ لطفاً تعداد را به صورت عدد وارد کنید.")
        return

    if quantity <= 0:
        await message.answer("❌ تعداد باید بیشتر از صفر باشد.")
        return


    await message.answer(
f"""
🏷️ نام محصول: {product.name}
📝 تعداد سفارش: {quantity}
💰 قیمت کل: {quantity * product.price:,} تومان
""",
    reply_markup=confirm_order_key(quantity=quantity)
    )

@router.callback_query(F.data.startswith("quantity:"))
async def add_order_to_cart(callback : CallbackQuery, state: FSMContext):
    quantity = int(callback.data.split(":")[1])

    data = await state.get_data()
    product_id = data.get("product_id")


    async with AsyncSessionLocal() as db:
        product = await get_product_by_id(db=db,product_id=product_id)
        user = await get_user_by_tel_id(db=db,telegram_id=callback.from_user.id)
        order_db = await get_pending_order(db=db, user_id=user.id)

        if order_db is None:
            order = await create_order(db=db,user_id=user.id)
        order_items = await add_item_order(
            db=db,
            order_id=order.id if order_db is None else order_db.id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
            )
        
        await add_total_price_order(
            db=db,
            order_id=order.id if order_db is None else order_db.id,
            total_price=order_items.price
        )
    await callback.answer("محصول به سبد اضافه شد! 🛒")
    await state.clear()

@router.message(F.text == "🛒 سبد خرید")
async def get_Invoice(message : Message):
    async with AsyncSessionLocal() as db:
        user = await get_user_by_tel_id(db=db,telegram_id=message.from_user.id)
        order = await get_order_by_user_id(db=db,user_id=user.id)

        if order is None:
            await message.answer("سبد خریدت خالیه! یه چرخی تو منو بزن. 😋")
            return
        
        order_items = await get_order_items_by_order_id(db=db, order_id=order.id)

        invoice_text = "🧾 **فاکتور فعلی**\n\n"

        for item in order_items:
            product = await get_product_by_id(db=db, product_id=item.product_id)
            item_total_price = product.price * item.quantity
        
            invoice_text += f"🍗 {product.name} × {item.quantity}\n💰 {item_total_price:,} تومان\n\n"

        invoice_text += "────────────\n"
        invoice_text += f"💰 مبلغ کل: {order.total_price:,} تومان\n"

        await message.answer(invoice_text, reply_markup=cart_key, parse_mode="Markdown")

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery):
    async with AsyncSessionLocal() as db:
        user = await get_user_by_tel_id(db=db,telegram_id=callback.from_user.id)
        order = await get_order_by_user_id(db=db,user_id=user.id)

        await change_status_order(db=db,order_id=order.id)

        await callback.answer("✅ سفارش شما ثبت شد.")

@router.callback_query(F.data == "clear_cart")
async def delete_order(callback: CallbackQuery):
        async with AsyncSessionLocal() as db:
            user = await get_user_by_tel_id(db=db,telegram_id=callback.from_user.id)
            order = await get_order_by_user_id(db=db,user_id=user.id)

            await delete_order_by_id(db=db,order_id=order.id)
            
            await callback.answer("سفارش با موفقیت حذف شد! 🗑")