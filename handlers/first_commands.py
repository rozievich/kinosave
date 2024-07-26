from aiogram import types, Router, Bot
from aiogram.filters.command import CommandStart, Command

from keyboards.inline_keyboards import forced_channel
from keyboards.reply_keyboards import admin_btn
from models.model import create_user, get_channels_all
from data.config import ADMINS


mainrouter = Router()


@mainrouter.message(CommandStart())
async def welcome_handler(msg: types.Message, bot: Bot):
    create_user(msg.from_user.id)
    check = await check_sub_channels(int(msg.from_user.id), bot)
    if check:
        await bot.set_my_commands([types.BotCommand(command="start", description="Ishga tushirish ♻️")])
        await bot.send_message(msg.chat.id, text=f"Assalomu alaykum {msg.from_user.first_name} 🤖\n<b>Kinolarni Dodasi Bot</b> - orqali siz o'zingizga yoqqan kinoni topishingiz mumkin 🎬\nShunchaki kino kodini yuboring va kinoni oling ✅")
    else:
        await msg.answer("Botdan foydalanish uchun ⚠️\nIltimos quidagi kanallarga obuna bo'ling ‼️", reply_markup=forced_channel())


@mainrouter.message(Command("panel"))
async def admin_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(f"Assalomu alaykum {msg.from_user.first_name} 🤖\nAdmin sahifaga xush kelibsiz ⚙️", reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


async def check_sub_channels(user_id: int, bot: Bot):
    channels = get_channels_all()
    for channel in channels:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel[2], user_id=user_id)
            if chat_member.status == "left":
                return False
        except:
            pass
    return True

