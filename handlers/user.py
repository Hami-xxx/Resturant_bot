from services.user_service import create_user, get_user_by_tel_id
from services.order_services import get_orders_by_user_id

from db.database import AsyncSessionLocal

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.user_key import main_key, profile_key

router = Router()

@router.message(Command("start"))
async def start_handler(message:Message):
    async with AsyncSessionLocal() as db:
        user = await create_user(
            db=db,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )

    await message.answer(
        "سلام 👋\nبه رستوران ما خوش آمدید!",
        reply_markup=main_key
    )


@router.message(F.text == "👤 پروفایل")
async def get_profile(message: Message):
    async with AsyncSessionLocal() as db:
        user = await get_user_by_tel_id(db=db,telegram_id=message.from_user.id)

    order_quantity = 0
    for order in user.orders:
        order_quantity += 1

    await message.answer(
f"""
👤 پروفایل کاربر

🆔 شناسه: {user.telegram_id}
👤 نام کاربری: {user.username if user.username else "نام کاربری ثبت نشده است"}
📦 تعداد سفارش‌ها: {order_quantity}

""",
    reply_markup=profile_key
        )

@router.callback_query(F.data == "my_orders")
async def my_orders(callback: CallbackQuery):
    async with AsyncSessionLocal() as db:
        user = await get_user_by_tel_id(db=db,telegram_id=callback.from_user.id)
        orders = await get_orders_by_user_id(db=db,user_id=user.id)
    
    orders_text = "📜 *سفارش ها*\n\n"
    order_number = 0

    for order in orders:
        order_number += 1
        orders_text += f"""
📋 شماره سفارش: {order_number}
🧾 وضعیت سفارش: {order.status}
📅 تاریخ سفارش: {order.created_at}
💰 مبلغ کل: {order.total_price}
"""
    await callback.message.answer(orders_text)


@router.message(F.text == "ℹ️ درباره ما")
async def about_bot(message: Message):
    await message.answer(
"""
این ربات یک پروژه نمونه‌کار برای شبیه‌سازی سیستم سفارش آنلاین رستوران است که با Python و Aiogram توسعه داده شده است.

🛒 امکانات بخش کاربر:
• مشاهده محصولات و اطلاعات آن‌ها
• مشاهده قیمت و وضعیت موجودی
• انتخاب محصول و افزودن به سبد خرید
• تعیین تعداد محصولات
• مشاهده فاکتور سفارش
• ثبت سفارش
• مشاهده سفارش‌های ثبت‌شده و وضعیت آن‌ها
• مدیریت اطلاعات کاربر

⚙️ بخش مدیریت:
• افزودن محصول
• ویرایش و حذف محصول
• مشاهده محصولات
• مشاهده و مدیریت سفارش‌ها

🗄️ اطلاعات کاربران، محصولات و سفارش‌ها در پایگاه داده PostgreSQL ذخیره می‌شوند و ساختار پروژه با SQLAlchemy و Alembic مدیریت می‌شود.

📌 این ربات یک پروژه آموزشی و نمونه‌کار است و به یک رستوران واقعی متصل نیست.
"""
)
    