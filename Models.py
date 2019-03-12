class UsersModel:
    """Сущность пользователей"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(20) UNIQUE,
                             password_hash VARCHAR(128),
                             email VARCHAR(20),
                             is_admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, email, is_admin=False):
        """Вставка новой записи"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        """Проверка, есть ли пользователь в системе"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        row = cursor.fetchone()
        return (True, row[2], row[0]) if row else (False,)

    def get(self, user_id):
        """Возврат пользователя по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех пользователей"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


class Laryok_Tadzhika:
    """Сущность ларьков"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS larki 
                            (laryok_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20) UNIQUE,
                             address VARCHAR(128)
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, address):
        """Добавление ларька"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO larki 
                          (name, address) 
                          VALUES (?,?)''',
                       (name, address))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск ларька по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM larki WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, laryok_id):
        """Запрос ларька по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM larki WHERE laryok_id = ?", (str(laryok_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех ларьков в городе"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM larki")
        rows = cursor.fetchall()
        return rows

    def delete(self, laryok_id):
        """Удаление ларька"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM larki WHERE laryok_id = ?''', (str(laryok_id)))
        cursor.close()
        self.connection.commit()