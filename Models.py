# Все execute переделаны под .format, потому что при значении id > 9 ругается на то,
# что ожидался 1 символ. Я не смог поправить через знаки ?, поэтому {}.format

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
                             email VARCHAR(20)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, email):
        """Вставка новой записи"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email) 
                          VALUES (?, ?, ?)''', (user_name, password_hash, email))
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
        cursor.execute("SELECT * FROM users WHERE id = {}".format(user_id))
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
                          VALUES (?, ?)''', (name, address))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск ларька по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM larki WHERE name = {}".format(name))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, laryok_id):
        """Запрос ларька по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM larki WHERE laryok_id = {}".format(laryok_id))
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
        cursor.execute('''DELETE FROM larki WHERE laryok_id = {}'''.format(laryok_id))
        cursor.close()
        self.connection.commit()


class FruitModel:
    def __init__(self, connection):
        self.connection = connection
        # self.i = 0

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS fruits
                            (fruit_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             sort VARCHAR(20),
                             price INTEGER,
                             number INTEGER,
                             laryok INTEGER
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, sort, price, number, laryok):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO fruits 
                          (sort, price, number, laryok) 
                          VALUES (?, ?, ?, ?)''', (sort, price, number, laryok))
        cursor.close()
        self.connection.commit()

    def exists(self, sort):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM fruits WHERE sort = {}".format(sort))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, fruit_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM fruits WHERE fruit_id = {}".format(fruit_id))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT sort, price, number, fruit_id, laryok FROM fruits")
        rows = cursor.fetchall()
        return rows

    def get_by_price(self, start_price, end_price):
        cursor = self.connection.cursor()
        # Тут никак не получилось поправить pep8
        cursor.execute(
            "SELECT sort, price, number, fruit_id FROM fruits WHERE price >= {} AND price <= {}".format(start_price,
                                                                                                        end_price))
        row = cursor.fetchall()
        return row

    def get_by_laryok(self, laryok_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT sort, price, number, fruit_id FROM fruits WHERE laryok = {}".format(
            laryok_id))
        row = cursor.fetchall()
        return row

    def update_buy(self, num, fruit_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT number FROM fruits WHERE fruit_id = {}".format(fruit_id))
        row = cursor.fetchone()
        cursor.execute("UPDATE fruits SET number = {} WHERE fruit_id = {}".format(num + row[0],
                                                                                  fruit_id))
        cursor.close()
        self.connection.commit()

    def update_sell(self, num, fruit_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT number FROM fruits WHERE fruit_id = {}".format(fruit_id))
        row = cursor.fetchone()
        if row[0] >= num:
            cursor.execute("UPDATE fruits SET number = {} WHERE fruit_id = {}".format(row[0] - num,
                                                                                      fruit_id))
            f = True
        else:
            f = False
        cursor.close()
        self.connection.commit()
        return f

    def get_delete_by_laryok(self, laryok_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM fruits WHERE laryok = {}'''.format(laryok_id))
        cursor.close()
        self.connection.commit()

    def delete(self, fruit_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM fruits WHERE fruit_id = {}'''.format(fruit_id))
        cursor.close()
        self.connection.commit()
