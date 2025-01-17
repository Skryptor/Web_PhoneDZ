from os.path import curdir

import psycopg2
import configparser
config = configparser.ConfigParser()
config.read('settings.ini')
password = config["password"]['passwords'].strip()
print(password)
conn = psycopg2.connect(database = 'clientData', user = 'postgres', password = password)

def create_table():
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS Numbers;
            DROP TABLE IF EXISTS Client;
                """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS Client(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(60) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    email VARCHAR(60) NOT NULL
                    );           
                """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS Numbers(
                    numbersid SERIAL PRIMARY KEY,
                    number VARCHAR(16),
                    id int not null,
                    FOREIGN KEY (id) REFERENCES Client(id) ON DELETE CASCADE
                    );
            """)
        conn.commit()

class UploadUser:

    def __init__(self, first_names=None, last_names=None, emails=None, number=None, userid=None):
        self.first_names = first_names
        self.last_names = last_names
        self.emails = emails
        self.number = number
        self.userid = userid

    def create_user (self, conn):

        if not all([self.first_names, self.last_names, self.emails]):
            raise ValueError('Что бы добавить пользователя необходимо добавить Имя, Фамилию, Мыло')

        with conn.cursor() as cur:
            cur.execute(""" 
                insert into Client (first_name, last_name, email)
                VALUES (%s, %s, %s);
            """, (self.first_names, self.last_names, self.emails))

        conn.commit()

    def create_num (self, conn):

        if not all([self.number, self.userid]):
            raise ValueError('Что бы добавить номер необходимо добавить и айди конкретного пользователя')

        with conn.cursor() as cur:
            cur.execute(""" 
                insert into Numbers (number, id)
                VALUES (%s, %s);
            """, (self.number, self.userid))

        conn.commit()
    @staticmethod
    def add_number(conn, number, userid):
        with conn.cursor() as cur:
            cur.execute("""
            insert into Numbers(number,id)
            VALUES (%s, %s);
        """, (number, userid))
        conn.commit()

    def update_value_num(self, conn):

        if not all([self.number, self.userid]):
            raise ValueError('Что бы изменить номер необходимо добавить и айди конкретного пользователя или вы угарнули и не добавили номер?')

        with conn.cursor() as cur:
            cur.execute(""" 
                update Numbers set number = %s WHERE id = %s
            """, (self.number, self.userid))
        conn.commit()

    def update_value_client(self, conn):

        if not self.userid:
            raise ValueError('Что бы изменить данные нужно айди конкретного пользователя')

        updating = []
        values = []
        if self.first_names is not None:
            updating.append('first_name = %s')
            values.append(self.first_names)
        if self.last_names is not None:
            updating.append('last_name = %s')
            values.append(self.last_names)
        if self.emails is not None:
            updating.append('email = %s')
            values.append(self.emails)

        if not updating:
            raise ValueError("Нечего обновлять хорош испытывать этот код")

        value = f"UPDATE Client SET {', '.join(updating)} WHERE id = %s"
        values.append(self.userid)

        with conn.cursor() as cur:
            cur.execute( value,tuple(values))
        conn.commit()

    def delete_value(self, conn, table_name):
        if not self.userid:
            raise ValueError('Необходимо указать ID пользователя.')

        conditions = ["id = %s"]
        values = [self.userid]

        if table_name == "Client":
            if self.first_name:
                conditions.append("first_name = %s")
                values.append(self.first_name)
            if self.last_name:
                conditions.append("last_name = %s")
                values.append(self.last_name)
            if self.email:
                conditions.append("email = %s")
                values.append(self.email)

        elif table_name == "Numbers":
            if self.number:
                conditions.append("number = %s")
                values.append(self.number)

        else:
            raise ValueError('Неправильное имя таблицы.')

        query = f"DELETE FROM {table_name} WHERE {' AND '.join(conditions)}"

        with conn.cursor() as cur:
            cur.execute(query, tuple(values))
        conn.commit()

    def search_user(self, conn, table_name, first_name=None, last_name=None, email=None, number=None):
        conditions = []
        values = []

        if first_name is not None:
            conditions.append("first_name = %s")
            values.append(first_name)
        if last_name is not None:
            conditions.append("last_name = %s")
            values.append(last_name)
        if email is not None:
            conditions.append("email = %s")
            values.append(email)
        if number is not None:
            conditions.append("number = %s")
            values.append(number)

        if not conditions:
            raise ValueError("Не указаны параметры для поиска")

        query = f"SELECT * FROM {table_name} WHERE {' AND '.join(conditions)}"

        with conn.cursor() as cur:
            cur.execute(query, tuple(values))
            result = cur.fetchall()

        return result
create_table()


conn.close()