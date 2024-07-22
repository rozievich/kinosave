from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models.model import channel, links


def forced_channel():
    channels = channel.get_datas()
    links_info = links.get_datas()
    buttons = []
    for i, v in enumerate(links_info):
        buttons.append([InlineKeyboardButton(text=f"{int(i) + 1} - kanal", url=f"{v['link']}")])
    for i, v in enumerate(channels):
        buttons.append([InlineKeyboardButton(text=f"{int(i) + len(links_info) + 1} - kanal", url=f"{v['username']}")])
    else:
        buttons.append([InlineKeyboardButton(text="Tekshirish ✅", callback_data="channel_check")])
    btn = InlineKeyboardMarkup(inline_keyboard=buttons)
    return btn


def rich_btn():
    btn = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="Boshqa kodlar", url="https://t.me/+9uco-4Gvr5xkNWYy")
            ]
        ]
    )
    return btn
