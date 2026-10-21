from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ افزودن محصول", callback_data="add_product"
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 محصولات", callback_data="products"
            )
        ],
        [
            InlineKeyboardButton(
                text="✏️ ویرایش محصول", callback_data="edit"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 حذف محصول", callback_data="delete"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 سفارش‌ها", callback_data="orders"
            )
        ]
    ]
)

def edit_product_key(products):
    buttons = []

    for product in products:
        buttons.append([
            InlineKeyboardButton(
            text=f"🍗 {product.name}",
            callback_data=f"edit_product_id:{product.id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


edit_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✏️ تغییر نام", callback_data="edit_name"
            )
        ],
        [
            InlineKeyboardButton(
                text="✏️ تغییر قیمت", callback_data="edit_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="✏️ تغییر توضیحات", callback_data="edit_description"
            )
        ],
        [
            InlineKeyboardButton(
                text="✏️ تغییر موجودی", callback_data="edit_available"
            )
        ]
    ]
) 

def delete_product_key(products):
    buttons = []

    for product in products:
        buttons.append([
            InlineKeyboardButton(
            text=f"🍗 {product.name}",
            callback_data=f"delete_product_id:{product.id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)