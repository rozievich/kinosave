from .orm import Base, MediaClass, ChannelClass, LinkClass, SeriesClass


user = Base("users")
channel = ChannelClass("channels")
movie = MediaClass("movies")
links = LinkClass("links")
series = SeriesClass("series")

# User table data


def create_user(telegram_id: int):
    data = user.get_data(str(telegram_id))
    if not data:
        user.create_data(telegram_id=str(telegram_id))
        return True
    else:
        return False


def get_users():
    return user.get_datas()


def statistika_user():
    data = user.statistika()
    all_data = user.get_datas()
    if data:
        return (f"Admin uchun Userlar statistikasi 📊\n\n"
                f"Oxirgi 30 kun ichida ro'yhatdan o'tgan userlar soni: {len(data['month'])}\n"
                f"Oxirgi 7 kun ichida ro'yhatdan o'tgan userlar soni: {len(data['week'])}\n"
                f"Oxirgi 24 soat ichida ro'yhatdan o'tgan userlar soni: {len(data['day'])}\n\n"
                f"Barcha Userlar soni: {len(all_data)}")
    else:
        return False


# Movies table data
def create_movie(post_id: int, file_id: str, caption: str) -> int:
    data = movie.get_movie(file_id)
    if not data:
        movie.create_data(post_id, file_id, caption)
        return post_id
    else:
        return data.get('post_id', None)


def delete_movie_func(post_id: int):
    data = movie.get_data(post_id=post_id)
    if data:
        try:
            movie.delete_movie(post_id=post_id)
            return f"Kino muvaffaqiyatli o'chirildi ✅"
        except:
            return f"Kino o'chrishda xatolik yuzaga keldi ❌"
    else:
        return f"{post_id} - ID bilan kino topilmadi ❌"


def get_movie(post_id: int):
    data = movie.get_data(post_id)
    if data:
        return [data['file_id'], data['caption']]
    else:
        return False


def statistika_movie():
    data = movie.statistika()
    all_data = movie.get_datas()
    all_series = series.get_all_series()
    if data:
        return (f"Admin uchun Kinolar statistikasi 📊\n\n"
                f"Oxirgi 30 kun ichida yuklangan kinolar soni: {len(data['month'])}\n"
                f"Oxirgi 7 kun ichida yuklangan kinolar soni: {len(data['week'])}\n"
                f"Oxirgi 24 soat ichida yuklangan kinolar soni: {len(data['day'])}\n\n"
                f"Barcha Kinolar soni: {len(all_data)} 📽\n\n"
                f"Barcha Seriallar soni: {len(all_series)} 🎞")
    else:
        return False


# Channel table data
def create_channel(username: str, channel_id: str):
    data = channel.get_data(channel_id=channel_id)
    if data:
        return False
    else:
        channel.create_data(username, channel_id)
        return True
    

def delete_channel(channel_id: str):
    data = channel.get_data(channel_id)
    if data:
        channel.delete_data(channel_id)
        return True
    else:
        return None


def get_channels():
    data = channel.get_datas()
    links_info = links.get_datas()
    text = f"Hamkor Kanallar ro'yhati 📥\n\n"
    for i in data:
        text += f"{i['username']}\n"
    else:
        text += "\nHamkor Linklar ro'yhati 🔗\n\n"
        for j in links_info:
            text += f"{j['link']}\n"
    return text


def get_channels_all():
    return channel.get_datas()


# Links table data
def create_link(url: str):
    data = links.get_data(link=url)
    if data:
        return False
    else:
        links.create_data(link=url)
        return True


def delete_link(url: str):
    data = links.get_data(link=url)
    if data:
        links.delete_data(link=url)
        return True
    else:
        return None


# Series models
def create_series_func(series_id: int, file_id: str, caption: str):
    try:
        series.create_series(series_id, file_id, caption)
    except:
        return False
    else:
        return True


def delete_series_func(series_id: int):
    data = series.get_series(series_id)
    if data:
        series.delete_series(series_id=series_id)
        return "Serial muvaffaqiyatli o'chirildi ✅"
    else:
        return f"S{series_id} - ID bilan kino topilmadi ❌"


def get_series_func(series_id: int):
    data = series.get_series(series_id)
    if data:
        return [data['file_id'], data['caption']]
    else:
        return False

