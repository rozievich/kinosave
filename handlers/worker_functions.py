from aiogram import types, Bot, F
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from keyboards.reply_keyboards import admin_btn, movies_btn, exit_btn, channels_btn
from keyboards.inline_keyboards import forced_channel
from models.model import statistika_user, statistika_movie, create_movie, get_channels, create_channel, delete_channel, get_users, get_movie, create_link, delete_link, delete_movie_func, get_series_func, create_series_func, delete_series_func
from states.state_admin import AddMedia, AddChannelState, DeleteChannelState, ReklamaState, AddLinkState, DeleteLinkState, DeleteMediaState, AddSeriesState, DeleteSeriesState
from .first_commands import check_sub_channels, mainrouter



@mainrouter.message(lambda msg: msg.text == "Statistika 📊")
async def user_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=statistika_user(), reply_markup=admin_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(lambda msg: msg.text == "Kinolar 🎬")
async def media_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Kinolar kategoriyasiga xush kelibsiz 🛠", reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(lambda msg: msg.text == "Kino Statistika 📊")
async def kino_statistika_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=statistika_movie(), reply_markup=movies_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())



@mainrouter.message(lambda msg: msg.text == "Kino qo'shish 📥")
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
            await state.update_data(file_id=msg.video.file_id, caption=msg.caption)
            await state.set_state(AddMedia.media_id)
            await msg.answer(text="Iltimos Kino uchun ID kiriting: ", reply_markup=exit_btn())
    except:
        await msg.answer("Iltimos Kino yuboring!", reply_markup=exit_btn())
    

@mainrouter.message(AddMedia.media_id)
async def handle_media_id(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        elif not get_movie(int(msg.text)):
            movie_info = await state.get_data()
            data = create_movie(post_id=int(msg.text), file_id=movie_info["file_id"], caption=movie_info["caption"])
            if data:
                await msg.reply(f"Kino malumotlar bazasiga saqlandi ✅\nKino Kodi: <b>{data}</b>", reply_markup=movies_btn())
            await state.clear()
        else:
            await msg.reply(f"{msg.text} - ID bilan kino mavjud!")
    except:
        await msg.answer("Iltimos Kod sifatida Raqam yuboring!", reply_markup=exit_btn())


@mainrouter.message(F.text == "Kino o'chirish 🗑")
async def handle_delete_media_func(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(DeleteMediaState.post_id)
        await msg.answer("Kinoni Kodini yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(DeleteMediaState.post_id)
async def handle_delete_media(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino o'chirish bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            data = delete_movie_func(int(msg.text))
            await msg.reply(text=data, reply_markup=movies_btn())
            await state.clear()
    except:
        await msg.answer("Iltimos Kod sifatida Raqam yuboring!", reply_markup=exit_btn())


@mainrouter.message(F.text == "Serial qo'shish 📌")
async def series_add_handler(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(AddSeriesState.series_media)
        await msg.answer("Serialning bitta qismini yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(AddSeriesState.series_media)
async def series_handle_video(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Serial yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            await state.update_data(file_id=msg.video.file_id, caption=msg.caption)
            await state.set_state(AddSeriesState.series_id)
            await msg.answer(text="Iltimos Serial uchun yangi ID kiriting yoki qo'shmoqchi bo'lgan serialingizning ID raqamini yozing: ", reply_markup=exit_btn())
    except:
        await msg.answer("Iltimos Kino yuboring!", reply_markup=exit_btn())
    

@mainrouter.message(AddSeriesState.series_id)
async def series_handle_media_id(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Kino yuklash bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            movie_info = await state.get_data()
            series_info = create_series_func(series_id=int(msg.text[1:]), file_id=movie_info["file_id"], caption=movie_info["caption"])
            if series_info:
                await msg.reply(f"Serial malumotlar bazasiga saqlandi ✅\nSerial Kodi: <b>S{msg.text[1:]}</b>", reply_markup=movies_btn())
            await state.clear()
    except:
        await msg.answer("Iltimos yuborgan kodingizni tekshiring hamda Boshida <b>S</b> va qolgani raqam ekanligiga ishonch hosil qiling!\nMisol: <b>S123</b>", reply_markup=exit_btn())


@mainrouter.message(F.text == "Serial o'chirish 🗑")
async def series_handle_delete_media_func(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        await state.set_state(DeleteSeriesState.series_id)
        await msg.answer("O'chirish kerak bo'lgan Serial kodini yuborishingiz mumkin 🎬", reply_markup=exit_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(DeleteSeriesState.series_id)
async def series_handle_delete_media(msg: types.Message, state: FSMContext):
    try:
        if msg.text == "❌":
            await msg.answer("Serial o'chirish bekor qilindi ❌", reply_markup=movies_btn())
            await state.clear()
        else:
            data = delete_series_func(int(msg.text[1:]))
            await msg.reply(text=data, reply_markup=movies_btn())
            await state.clear()
    except:
        await msg.answer("Iltimos Kod sifatida Raqam yuboring!", reply_markup=exit_btn())



@mainrouter.message(lambda msg: msg.text == "Kanallar 🖇")
async def channels_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer(text=get_channels(), reply_markup=channels_btn())
    else:
        await msg.answer("Siz admin emassiz ❌", reply_markup=types.ReplyKeyboardRemove())


@mainrouter.message(lambda msg: msg.text == "Kanal qo'shish ⚙️")
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
    except Exception as e:
        pass


@mainrouter.message(AddChannelState.channel_id)
async def add_channel_handler_func(msg: types.Message, state: FSMContext):
    if msg.text == "❌":
        await msg.answer("Kanal qo'shish bekor qilindi ❌", reply_markup=channels_btn())
        await state.clear()
    else:
        channel_info = await state.get_data()
        data = create_channel(channel_info['username'], msg.text)
        if data:
            await msg.answer("Kanal muvaffaqiyatli qo'shildi ✅", reply_markup=channels_btn())
            await state.clear()
        else:
            await msg.answer("Bu kanal oldin qo'shilgan ❌", reply_markup=channels_btn())
            await state.clear()


@mainrouter.message(lambda msg: msg.text == "Kanal o'chirish 🗑")
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


@mainrouter.message(lambda msg: msg.text == "Reklama 🎁")
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
                    except Exception as e:
                        summa += 1
            for admin in ADMINS:
                await bot.send_message(int(admin), text=f"Botni bloklagan Userlar soni: {summa}")
        except Exception as e:
            pass


@mainrouter.callback_query(F.data == "channel_check")
async def channel_check_handler(callback: types.CallbackQuery, bot: Bot):
    check = await check_sub_channels(callback.from_user.id, bot)
    if check:
        await callback.message.delete()
        await callback.answer("Obuna bo'lganingiz uchun rahmat ☺️")
    else:
        await callback.message.answer("Botdan foydalanish uchun ⚠️\nIltimos quidagi kanallarga obuna bo'ling ‼️", reply_markup=forced_channel())


@mainrouter.message(lambda msg: msg.text == "❌")
async def exit_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        await msg.answer("Bosh menyu 🔮", reply_markup=admin_btn())


@mainrouter.message()
async def forward_last_video(msg: types.Message, bot: Bot):
    try:
        check = await check_sub_channels(int(msg.from_user.id), bot)
        if check:
            if msg.text[0] in ["S", "s"]:
                data = get_series_func(int(msg.text[1:]))
                if data:
                    for i in data:
                        try:
                            await bot.send_video(chat_id=msg.from_user.id, video=i[0], caption=f"{i[1]}\n\n🤖 Bizning bot: @Tarjima_KinoIarbot")
                        except:
                            await msg.reply(f"Serialni yuborishda xatoliklar yuzaga kelmoqda iltimos adminga murojat qiling!")
                else:
                    await msg.reply(f"{msg.text} - id bilan hech qanday serial topilmadi ❌")
            else:
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
    except:
        await msg.answer("Iltimos ID sifatida raqam yuboring ⚠️")
