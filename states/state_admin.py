from aiogram.fsm.state import State, StatesGroup



class ReklamaState(StatesGroup):
    rek = State()


class AddMedia(StatesGroup):
    media = State()
    media_id = State()


class DeleteMediaState(StatesGroup):
    post_id = State()


class AddSeriesState(StatesGroup):
    series_media = State()
    series_id = State()


class DeleteSeriesState(StatesGroup):
    series_id = State()


class AddChannelState(StatesGroup):
    username = State()
    channel_id = State()
    is_order = State()


class DeleteChannelState(StatesGroup):
    username = State()


class AddLinkState(StatesGroup):
    link = State()


class DeleteLinkState(StatesGroup):
    link = State()
