import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute("CREATE TABLE users (username TEXT, password TEXT, firstname TEXT)")
cursor.execute("INSERT INTO users VALUES ('admin', 'admin', 'Petro')")
cursor.execute("INSERT INTO users VALUES ('user', 'pass', 'Ivan')")
conn.commit()

username = "admin' OR '1'='1"
password = "anything"

print("Уразливий запит:")
query = f"SELECT firstname FROM users WHERE username='{username}' AND password='{password}'"
print(query)
try:
    result = cursor.execute(query).fetchall()
    print(f"Результат: {result}")
    if result:
        print("УВАГА! SQL-ін'єкція успішна - отримано несанкціонований доступ!")
except sqlite3.OperationalError as e:
    print(f"Помилка SQL: {e}")
print()

print("Безпечний запит:")
query = "SELECT firstname FROM users WHERE username=? AND password=?"
print(query)
try:
    result = cursor.execute(query, (username, password)).fetchall()
    print(f"Результат: {result}")
    if not result:
        print("Доступ заборонено: невірний логін або пароль")
except sqlite3.OperationalError as e:
    print(f"Помилка SQL: {e}")

conn.close()