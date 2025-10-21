from aiogram import Bot
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os


load_dotenv()
tg_token = os.getenv('BOT_TOKEN')
ai_token = os.getenv('ai_token')
admin_id = os.getenv('admin_id')
database_password = os.getenv('DATABASE_PASSWORD')
consultant_1 = os.getenv('consultant_1')
api_key = os.getenv('api_key')
api_key_rm = os.getenv('api_key_rm')
consultant_dm = os.getenv('consultant_dm')
consultant_andrej = os.getenv('consultant_andrej')
table_id = os.getenv('table_id')
table_link = os.getenv('table_link')
client_init = os.getenv("client_init")

bot = Bot(token=tg_token)

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    user='postgres',
    password=database_password,
    host='localhost',
    database='dm_bot_db'
)
# if connection_pool:
#     print("Connection pool created successfully")

