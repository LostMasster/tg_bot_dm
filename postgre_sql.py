from igbore_git import connection_pool
import psycopg2
import asyncio


async def add_user_language_dict():
    conn = connection_pool.getconn()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'SELECT user_id, language FROM users;'
                )
                user_language_dict = {}
                db = cursor.fetchall()
                for user_id, language in db:
                    user_language_dict[user_id] = language
                print('[DICT] с выбором языка записан')
                return user_language_dict
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Ошибка при получении данных из базы данных: {error}")
            return None
        finally:
            connection_pool.putconn(conn)
    else:
        print("Не удалось получить соединение с базой данных.")
        return None


users_languages = asyncio.run(add_user_language_dict())
print(users_languages[6555200949])


async def new_user(user_id, date_reg):
    conn = connection_pool.getconn()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO users (user_id, date_reg) VALUES (%s, %s)"
                           f" ON CONFLICT (user_id) DO NOTHING",
                           (user_id, date_reg))
            conn.commit()
            print(f"Пользователь {user_id} добавлен в базу данных.")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при работе с PostgreSQL", str(error))
        finally: connection_pool.putconn(conn)
    else: print("Не удалось подключиться к базе данных.")


async def language(user_id, language):
    conn = connection_pool.getconn()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET language = %s WHERE user_id = %s',
                (language, user_id)
            )
            conn.commit()
            print(f"Пользователь {user_id} выбрал/изменил язык на {language}")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при работе с PostgreSQL", str(error))
        finally: connection_pool.putconn(conn)
    else: print("Не удалось подключиться к базе данных.")

