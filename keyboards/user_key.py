from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_key = ReplyKeyboardMarkup(
    keyboard=[
        [   
            KeyboardButton(text="📦 محصولات"),
            KeyboardButton(text="🛒 سبد خرید")
        ],
        [
            KeyboardButton(text="👤 پروفایل"),
            KeyboardButton(text="ℹ️ درباره ما")
        ]
    ],
    resize_keyboard=True
)

def product_key(products):
    buttons = []

    for product in products:
        buttons.append([
            InlineKeyboardButton(
            text=f"🍗 {product.name}",
            callback_data=f"product:{product.id}"
            )
        ])


    return InlineKeyboardMarkup(inline_keyboard=buttons)

def select_product_key(product_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="[انتخاب محصول]",
                callback_data=f"product_id:{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 بازگشت",
                callback_data="back_to_products"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_order_key(quantity):
    buttons=[
        [
            InlineKeyboardButton(
                text="اضافه کردن محصول 🛒",
                callback_data=f"quantity:{quantity}"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)

cart_key = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(
                text="✅ ثبت نهایی سفارش", callback_data="confirm_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑 حذف سفارش", callback_data="clear_cart"
                )
            ]
        ])

profile_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📋 سفارش‌های من", callback_data="my_orders"
            )
        ]
    ]
)
