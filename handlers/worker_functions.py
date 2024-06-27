from aiogram import types, Bot, F
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from keyboards.inline_keyboards import forced_channel
from keyboards.reply_keyboards import admin_btn, movies_btn, exit_btn, channels_btn, is_order_btn
from models.model import statistika_user, statistika_movie, create_movie, get_channels, create_channel, delete_channel, \
    get_users, get_movie, create_link, delete_link, check_order_channels, create_join_request
from states.state_admin import AddMedia, AddChannelState, DeleteChannelState, ReklamaState, AddLinkState, \
    DeleteLinkState
from .first_commands import check_sub_channels, mainrouter


@mainrouter.message(F.text == "Statistika 📊")
async def user_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=statistika_user(), reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(F.text == "Kinolar 🎬")
async def media_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Kinolar kategoriyasiga xush kelibsiz 🛠", reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(F.text == "Kino Statistika 📊")
async def kino_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=statistika_movie(), reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(F.text == "Kino qo'shish 📥")
async def kino_add_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(AddMedia.media)
        await msg.answer("Kinoni yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(AddMedia.media)
async def handle_video(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            data = create_movie(file_id=msg.video.file_id, caption=msg.caption)
            if data:
                await msg.reply(f"Kino malumotlar bazasiga saqlandi ✅\nKino Kodi: {data[0]}", reply_markup=movies_btn())
                await state.clear()
    except:
        await msg.answer("Iltimos Kino yuboring!", reply_markup=exit_btn())


@mainrouter.message(F.text == "Kanallar 🖇")
async def channels_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=get_channels(), reply_markup=channels_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(F.text == "Kanal qo'shish ⚙️")
async def add_channel_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(AddChannelState.username)
        await msg.answer(text="Qo'shish kerak bo'lgan kanal linkini kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(AddChannelState.username)
async def add_channel_username_handler(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
            await state.clear()
        else:
            await state.update_data(username=msg.text)
            await state.set_state(AddChannelState.channel_id)
            await msg.answer(text="Iltimos Kanal ID kiriting: ", reply_markup=exit_btn())
    except:
        pass


@mainrouter.message(AddChannelState.channel_id)
async def add_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        await state.update_data(channel_id=msg.text)
        await state.set_state(AddChannelState.is_order)
        await msg.answer(text="Bu kanal buyurtma kanalmi  ⁉️", reply_markup=is_order_btn())


@mainrouter.message(AddChannelState.is_order)
async def is_order_handler(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        channel_info = await state.get_data()
        data = create_channel(channel_info['username'], channel_info['channel_id'], True if msg.text == "Ha ✅" else False)
        if data:
            await msg.answer("Kanal muvaffaqiyatli qo'shildi ✅", reply_markup=channels_btn())
            await state.clear()
        else:
            await msg.answer("Bu kanal oldin qo'shilgan ❌", reply_markup=channels_btn())
            await state.clear()


@mainrouter.message(F.text == "Kanal o'chirish 🗑")
async def movie_delete_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(DeleteChannelState.username)
        await msg.answer(text="O'chirish kerak bo'lgan kanal ID kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(DeleteChannelState.username)
async def delete_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal o'chirish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        data = delete_channel(msg.text)
        if data:
            await msg.answer("Kanal muvaffaqiyatli o'chirildi ✅", reply_markup=channels_btn())
        else:
            await msg.answer("Bunday ID uchun kanal mavjud emas ❌", reply_markup=channels_btn())
        await state.clear()


@mainrouter.message(F.text == "Link qo'shish ⚙️")
async def add_channel_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(AddLinkState.link)
        await msg.answer(text="Qo'shish kerak bo'lgan Linkni kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(AddLinkState.link)
async def add_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Link qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        data = create_link(url=msg.text)
        if data:
            await msg.answer("Link muvaffaqiyatli qo'shildi ✅", reply_markup=channels_btn())
            await state.clear()
        else:
            await msg.answer("Bu Link oldin qo'shilgan ❌", reply_markup=channels_btn())
            await state.clear()


@mainrouter.message(F.text == "Link o'chirish 🗑")
async def movie_delete_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(DeleteLinkState.link)
        await msg.answer(text="O'chirish kerak bo'lgan Linkni kiriting ✍️", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(DeleteLinkState.link)
async def delete_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Link o'chirish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        data = delete_link(msg.text)
        if data:
            await msg.answer("Link muvaffaqiyatli o'chirildi ✅", reply_markup=channels_btn())
        else:
            await msg.answer("Bunday Link mavjud emas ❌", reply_markup=channels_btn())
        await state.clear()


@mainrouter.message(F.text == "Reklama 🎁")
async def reklama_handler(msg: types.Message, bot: Bot, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(ReklamaState.rek)
        await bot.send_message(chat_id=msg.chat.id, text="Reklama tarqatish bo'limi 🤖", reply_markup=exit_btn())
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(ReklamaState.rek)
async def rek_state(msg: types.Message, bot: Bot, state: FSMContext):
    if msg.text == "❌":
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish bekor qilindi 🤖❌", reply_markup=admin_btn())
        await state.clear()
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Reklama yuborish boshlandi 🤖✅", reply_markup=admin_btn())
        await state.clear()
        try:
            summa = 0
            for user in get_users():
                if int(user['telegram_id']) not in ADMINS:
                    try:
                        await msg.copy_to(int(user['telegram_id']), caption=msg.caption, caption_entities=msg.caption_entities, reply_markup=msg.reply_markup)
                    except:
                        summa += 1
            for admin in ADMINS:
                await bot.send_message(int(admin), text=f"Botni bloklagan Userlar soni: {summa}")
        except:
            pass


@mainrouter.callback_query(F.data == "channel_check")
async def channel_check_handler(callback: types.CallbackQuery, bot: Bot):
    check = await check_sub_channels(callback.from_user.id, bot)
    if check:
        await callback.message.delete()
        await callback.answer("Obuna bo'lganingiz uchun rahmat ☺️")
    else:
        await callback.message.answer("Botdan foydalanish uchun ⚠️\nIltimos quidagi kanallarga obuna bo'ling ‼️", reply_markup=forced_channel())


@mainrouter.message(F.text == "❌")
async def exit_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Bosh menyu 🔮", reply_markup=admin_btn())


@mainrouter.message(F.text.isdigit())
async def forward_last_video(msg: types.Message, bot: Bot):
    check = await check_sub_channels(int(msg.from_user.id), bot)
    if check:
        data = get_movie(int(msg.text))
        if data:
            try:
                await bot.send_video(chat_id=msg.from_user.id, video=data[0], caption=f"{data[1]}\n\n🤖 Bizning bot: @Tarjima_KinoIarbot")
            except:
                await msg.reply(f"{msg.text} - id bilan hech qanday kino topilmadi ❌")
        else:
            await msg.reply(f"{msg.text} - id bilan hech qanday kino topilmadi ❌")
    else:
        await msg.answer("Botdan foydalanish uchun ⚠️\nIltimos quidagi kanallarga obuna bo'ling ‼️", reply_markup=forced_channel())


@mainrouter.chat_join_request()
async def chat_join_request_handler(chat_join_request: types.ChatJoinRequest):
    info = check_order_channels(str(chat_join_request.chat.id))
    if info:
        await create_join_request(str(chat_join_request.chat.id), str(chat_join_request.from_user.id))
