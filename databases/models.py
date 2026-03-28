from .db_connection import DatabaseConnection


class User:
    def __init__(self, user_id=None, username=None, password=None, is_admin=False, is_blocked=False, failed_attempts=0):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.is_blocked = is_blocked
        self.failed_attempts = failed_attempts

    @staticmethod
    def authenticate(username, password):
        db = DatabaseConnection()
        cur = db.get_cursor()

        cur.execute(
            "SELECT user_id, username, password, is_admin, is_blocked, failed_attempts FROM users WHERE username = %s",
            (username,))
        row = cur.fetchone()

        if not row:
            return None, "not_found"

        user = User(row[0], row[1], row[2], row[3], row[4], row[5])

        if user.is_blocked:
            return None, "blocked"

        if user.password == password:
            cur.execute("UPDATE users SET failed_attempts = 0 WHERE user_id = %s", (user.user_id,))
            db.commit()
            return user, "success"

        new = user.failed_attempts + 1
        cur.execute("UPDATE users SET failed_attempts = %s WHERE user_id = %s", (new, user.user_id))
        db.commit()

        if new >= 3:
            cur.execute("UPDATE users SET is_blocked = TRUE WHERE user_id = %s", (user.user_id,))
            db.commit()
            return None, "blocked"

        return None, "wrong_password"

    @staticmethod
    def create_user(username, password, is_admin):
        db = DatabaseConnection()
        cur = db.get_cursor()

        cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return False, "Логин уже существует!"

        cur.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)",
                    (username, password, is_admin))
        db.commit()
        return True, "Пользователь добавлен!"

    @staticmethod
    def update_user(user_id, username, password, is_admin):
        db = DatabaseConnection()
        cur = db.get_cursor()

        cur.execute("SELECT user_id FROM users WHERE username = %s AND user_id != %s", (username, user_id))
        if cur.fetchone():
            return False, "Логин уже занят!"

        cur.execute("UPDATE users SET username=%s, password=%s, is_admin=%s WHERE user_id=%s",
                    (username, password, is_admin, user_id))
        db.commit()
        return True, "Обновлено!"

    @staticmethod
    def get_all_users():
        cur = DatabaseConnection().get_cursor()
        cur.execute("SELECT user_id, username, is_admin, is_blocked, failed_attempts FROM users ORDER BY user_id")
        return cur.fetchall()

    @staticmethod
    def unblock_user(user_id):
        cur = DatabaseConnection().get_cursor()
        cur.execute("UPDATE users SET is_blocked=FALSE, failed_attempts=0 WHERE user_id=%s", (user_id,))
        cur.connection.commit()

    @staticmethod
    def delete_user(user_id):
        cur = DatabaseConnection().get_cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
        cur.connection.commit()