from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



def admin_btn():
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Statistika 📊"),
                KeyboardButton(text="Kinolar 🎬"),
                KeyboardButton(text="Reklama 🎁"),
            ],
            [
                KeyboardButton(text="Kanallar 🖇")
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return btn


def movies_btn():
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Kino Statistika 📊"),
                KeyboardButton(text="Kino qo'shish 📥")
            ],
            [
                KeyboardButton(text="Kino o'chirish 🗑"),
                KeyboardButton(text="❌")
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return btn


def channels_btn():
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Kanal qo'shish ⚙️"),
                KeyboardButton(text="Kanal o'chirish 🗑")
            ],
            [
                KeyboardButton(text="Link qo'shish ⚙️"),
                KeyboardButton(text="Link o'chirish 🗑")
            ],
            [
                KeyboardButton(text="❌")
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return btn


def exit_btn():
    btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❌")
            ]
        ],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    return btn
