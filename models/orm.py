from db.connect import cur, conn


class Base:
    def __init__(self, table):
        self.table = table

    def create_data(self, telegram_id: str):
        query = f"INSERT INTO {self.table}(telegram_id) VALUES (%s)"
        cur.execute(query, (telegram_id,))
        conn.commit()

    def get_data(self, telegram_id: str):
        query = f"SELECT * FROM {self.table} WHERE telegram_id = %s"
        cur.execute(query, (telegram_id,))
        return cur.fetchone()

    def get_datas(self):
        query = f"SELECT * FROM {self.table}"
        cur.execute(query)
        return cur.fetchall()

    def statistika(self):
        query = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'"
        cur.execute(query)
        month = cur.fetchall()
        query_week = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('week', CURRENT_DATE) - INTERVAL '1 week'"
        cur.execute(query_week)
        week = cur.fetchall()
        query_day = f"SELECT * FROM {self.table} WHERE created_at >= DATE_TRUNC('day', CURRENT_DATE) - INTERVAL '1 day'"
        cur.execute(query_day)
        day = cur.fetchall()
        return {'month': month, 'week': week, 'day': day}


class MediaClass(Base):

    def create_data(self, file_id: str, caption: str, post_id: int):
        query = f"INSERT INTO {self.table}(post_id, file_id, caption) VALUES (%s, %s, %s)"
        cur.execute(query, (post_id, file_id, caption))
        conn.commit()

    def get_id(self):
        cur.execute(f"SELECT max(id) FROM {self.table}")
        return cur.fetchone()

    def get_data(self, post_id: int):
        query = f"SELECT * FROM {self.table} WHERE post_id = %s"
        cur.execute(query, (post_id,))
        return cur.fetchone()

    def get_movie(self, file_id: str):
        query = f"SELECT * FROM {self.table} WHERE file_id = %s"
        cur.execute(query, (file_id,))
        return cur.fetchone()


class ChannelClass(Base):

    def create_data(self, username: str, channel_id: str, is_order: bool):
        query = f"INSERT INTO {self.table}(username, channel_id, is_order) VALUES (%s, %s, %s)"
        cur.execute(query, (username, channel_id, is_order))
        conn.commit()

    def get_data(self, channel_id: str):
        query = f"SELECT * FROM {self.table} WHERE channel_id = %s"
        cur.execute(query, (channel_id,))
        return cur.fetchone()

    def get_datas_order(self, is_order: bool):
        query = f"SELECT * FROM {self.table} WHERE is_order = %s"
        cur.execute(query, (is_order,))
        return cur.fetchall()

    def delete_data(self, channel_id: str):
        query = f"DELETE FROM {self.table} WHERE channel_id = %s"
        query_request = f"DELETE FROM join_requests WHERE channel_id = %s"
        cur.execute(query, (channel_id,))
        cur.execute(query_request, (channel_id,))
        conn.commit()


class LinkClass(Base):

    def create_data(self, link: str):
        query = f"INSERT INTO {self.table}(link) VALUES (%s)"
        cur.execute(query, (link,))
        conn.commit()

    def get_data(self, link: str):
        query = f"SELECT * FROM {self.table} WHERE link = %s"
        cur.execute(query, (link,))
        return cur.fetchone()

    def delete_data(self, link: str):
        query = f"DELETE FROM {self.table} WHERE link = %s"
        cur.execute(query, (link,))
        conn.commit()


class JoinRequest(Base):
    def create_data(self, channel_id: str, user_id: str):
        query = f"INSERT INTO {self.table}(channel_id, user_id) VALUES (%s, %s)"
        cur.execute(query, (channel_id, user_id))
        conn.commit()

    def get_data(self, channel_id: str, user_id: str):
        query = f"SELECT * FROM {self.table} WHERE channel_id = %s AND user_id = %s"
        cur.execute(query, (channel_id, user_id))
        return cur.fetchone()

    def delete_data(self, channel_id: str, user_id: str):
        query = f"DELETE FROM {self.table} WHERE channel_id = %s AND user_id = %s"
        cur.execute(query, (channel_id, user_id))
        conn.commit()
