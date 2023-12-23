import os
import sys
import psycopg2
from contextlib import closing
from fastapi import FastAPI
from psycopg2.extras import DictCursor

try:
    db_name=os.environ['POSTGRESS_DB_NAME']
    db_user=os.environ['POSTGRESS_DB_USER']
    db_user_password=os.environ['POSTGRESS_DB_USER_PASSWORD']
    db_host=os.environ['POSTGRESS_DB_HOST']
except KeyError:
    print('ENV error')
    sys.exit(1)

app = FastAPI()
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_user_password, host=db_host)

@app.get("/users")
def read_users():
    users = []
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("SELECT name FROM users;")
        response = cursor.fetchall()

        #print(response)
        for user in response:
            name = str(user[0])
            users.append({"name":name})
    return { "users": users }

@app.get("/user/{user_id}")
def read_user(user_id: int):
    users = []
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("SELECT name FROM users WHERE id = %(id)s;", {"id": user_id})
        response = cursor.fetchall()
        #print(response)
        for user in response:
            name = str(user[0])
            users.append({"name":name})

    return { "users": users }
