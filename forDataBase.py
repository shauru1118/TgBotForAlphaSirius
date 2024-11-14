from mysql.connector import connect, Error

# NULL
# INTEGER
# REAL
# TEXT
# BLOB

# CREATE TABLE IF NOT EXISTS tableName(parameterName TYPE, parameterName TYPE)
# INSERT INTO users (parameterName, parameterName) VALUES(?, ?)

url = "localhost"
user = "root"
password = "albert24112"

def add_order(_id, _name, _order):
    try:
        with connect(host=url, user=user, password=password, database="db") as con:
            query = f"insert into orders (`telegramId`, `name`, `order`) values ( %s, %s, %s ) "
            with con.cursor() as cursor:
                params = (str(_id), _name, _order)
                cursor.execute(query, params)
                print("Order entered in db")
            con.commit()
    except Error as e:
        print(e)
        print("ADD ORDER ERROR")


def get_orders():
    try:
        with connect(host=url, user=user, password=password, database="db") as con:
            query = f"select * from orders"
            with con.cursor() as cursor:
                cursor.execute(query)
                for i in cursor.fetchall():
                    print(i)
            con.commit()
    except Error as e:
        print(e)
        print("GET ORDERS ERROR")

def add_user(_id, _name):
    try:
        with connect(host=url, user=user, password=password, database="db") as con:
            query = "select telegramId from users"
            users = []
            with con.cursor() as cursor:
                cursor.execute(query)
                for i in cursor.fetchall():
                    for j in i:
                        users.append(j)
            if str(_id) not in users:
                query = f"insert into users (`telegramId`, `name`) values ( %s, %s ) "
                with con.cursor() as cursor:
                    params = (str(_id), _name)
                    cursor.execute(query, params)
                    print("User entered in db")
            else:
                print("User has already entered")
            con.commit()
    except Error as e:
        print(e)
        print("ADD USERS ERROR")

def get_users():
    try:
        with connect(host=url, user=user, password=password, database="db") as con:
            query = "select telegramId from users"
            users = []
            with con.cursor() as cursor:
                cursor.execute(query)
                for i in cursor.fetchall():
                    for j in i:
                        users.append(j)
            print(users)
    except Error as e:
        print(e)
        print("GET USERS ERROR")

    return users

