import sqlite3
import os
from getpass import getpass

class DatabaseManager:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
        self.setup_database()
    
    def setup_database(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course INTEGER,
                gpa REAL,
                email TEXT
            )
        ''')
        
        users_data = [
            ('admin', 'admin123', 'administrator'),
            ('teacher', 'teach456', 'teacher'),
            ('student', 'stud789', 'student')
        ]
        cursor.executemany('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', users_data)
        
        students_data = [
            ('Іван Петренко', 3, 4.5, 'ivan.petrenko@univ.edu'),
            ('Марія Коваленко', 2, 4.8, 'maria.kovalenko@univ.edu'),
            ('Олег Шевченко', 4, 4.2, 'oleg.shevchenko@univ.edu'),
            ('Анна Бондаренко', 1, 4.9, 'anna.bondarenko@univ.edu'),
            ('Дмитро Ткаченко', 3, 3.8, 'dmytro.tkachenko@univ.edu')
        ]
        cursor.executemany('INSERT INTO students (name, course, gpa, email) VALUES (?, ?, ?, ?)', students_data)
        
        conn.commit()
        conn.close()
        print("База даних створена успішно!\n")


class VulnerableApp:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
    
    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"\n[ВРАЗЛИВИЙ ЗАПИТ]: {query}")
        
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def search_students(self, search_term):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = f"SELECT * FROM students WHERE name LIKE '%{search_term}%'"
        print(f"\n[ВРАЗЛИВИЙ ЗАПИТ]: {query}")
        
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        return results


class SecureApp:
    def __init__(self, db_name='students.db'):
        self.db_name = db_name
    
    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        print(f"\n[ЗАХИЩЕНИЙ ЗАПИТ]: {query}")
        print(f"[ПАРАМЕТРИ]: username={username}, password={password}")
        
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def search_students(self, search_term):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        query = "SELECT * FROM students WHERE name LIKE ?"
        print(f"\n[ЗАХИЩЕНИЙ ЗАПИТ]: {query}")
        print(f"[ПАРАМЕТРИ]: search_term=%{search_term}%")
        
        cursor.execute(query, (f'%{search_term}%',))
        results = cursor.fetchall()
        conn.close()
        
        return results


def print_separator(title=""):
    print("\n" + "="*70)
    if title:
        print(f" {title}")
        print("="*70)


def display_results(results, result_type="студентів"):
    if results:
        if result_type == "користувача":
            print(f"\n✓ Вхід успішний!")
            print(f"ID: {results[0]}, Користувач: {results[1]}, Роль: {results[3]}")
        else:
            print(f"\n✓ Знайдено {len(results)} {result_type}:")
            for student in results:
                print(f"  • {student[1]} (Курс: {student[2]}, GPA: {student[3]})")
    else:
        print(f"\n✗ Нічого не знайдено")


def demo_vulnerable_login():
    print_separator("ДЕМОНСТРАЦІЯ 1: Вразлива авторизація")
    
    app = VulnerableApp()
    
    print("\n--- Спроба 1: Звичайна авторизація ---")
    result = app.login("admin", "admin123")
    display_results(result, "користувача")
    
    print("\n--- Спроба 2: SQL-ін'єкція (обхід пароля) ---")
    print("Ввід: username = admin'--")
    print("Пояснення: Символ ' закриває рядок, -- коментує перевірку пароля")
    result = app.login("admin'--", "anything")
    display_results(result, "користувача")
    
    print("\n--- Спроба 3: SQL-ін'єкція (універсальний обхід) ---")
    print("Ввід: username = ' OR '1'='1'--")
    print("Пояснення: Умова завжди істинна, отримуємо першого користувача")
    result = app.login("' OR '1'='1'--", "anything")
    display_results(result, "користувача")


def demo_secure_login():
    print_separator("ДЕМОНСТРАЦІЯ 2: Захищена авторізація")
    
    app = SecureApp()
    
    print("\n--- Спроба 1: Звичайна авторізація ---")
    result = app.login("admin", "admin123")
    display_results(result, "користувача")
    
    print("\n--- Спроба 2: Спроба SQL-ін'єкції (ЗАБЛОКОВАНО) ---")
    print("Ввід: username = admin'--")
    result = app.login("admin'--", "anything")
    display_results(result, "користувача")
    
    print("\n--- Спроба 3: Спроба SQL-ін'єкції (ЗАБЛОКОВАНО) ---")
    print("Ввід: username = ' OR '1'='1'--")
    result = app.login("' OR '1'='1'--", "anything")
    display_results(result, "користувача")


def demo_vulnerable_search():
    print_separator("ДЕМОНСТРАЦІЯ 3: Вразливий пошук студентів")
    
    app = VulnerableApp()
    
    print("\n--- Спроба 1: Звичайний пошук ---")
    results = app.search_students("Іван")
    display_results(results)
    
    print("\n--- Спроба 2: SQL-ін'єкція (витік всіх даних) ---")
    print("Ввід: %' OR '1'='1")
    print("Пояснення: Умова завжди істинна, отримуємо всі записи")
    results = app.search_students("%' OR '1'='1")
    display_results(results)
    
    print("\n--- Спроба 3: SQL-ін'єкція (витік даних з іншої таблиці) ---")
    print("Ввід: %' UNION SELECT id, username, password, role, username FROM users--")
    print("Пояснення: UNION дозволяє об'єднати результати з таблиці users")
    try:
        results = app.search_students("%' UNION SELECT id, username, password, role, username FROM users--")
        print(f"\n✓ КРИТИЧНА УРАЗЛИВІСТЬ! Витік даних користувачів:")
        for row in results:
            if '@' in str(row[4]):
                print(f"  • {row[1]} (Курс: {row[2]}, GPA: {row[3]})")
            else:
                print(f"  • ID: {row[0]}, Логін: {row[1]}, Пароль: {row[2]}, Роль: {row[3]}")
    except Exception as e:
        print(f"\n✗ Помилка: {e}")


def demo_secure_search():
    print_separator("ДЕМОНСТРАЦІЯ 4: Захищений пошук студентів")
    
    app = SecureApp()
    
    print("\n--- Спроба 1: Звичайний пошук ---")
    results = app.search_students("Іван")
    display_results(results)
    
    print("\n--- Спроба 2: Спроба SQL-ін'єкції (ЗАБЛОКОВАНО) ---")
    print("Ввід: %' OR '1'='1")
    results = app.search_students("%' OR '1'='1")
    display_results(results)
    
    print("\n--- Спроба 3: Спроба SQL-ін'єкції UNION (ЗАБЛОКОВАНО) ---")
    print("Ввід: %' UNION SELECT id, username, password, role, username FROM users--")
    results = app.search_students("%' UNION SELECT id, username, password, role, username FROM users--")
    display_results(results)


def demo_comparison():
    print_separator("ПОРІВНЯННЯ: Вразлива vs Захищена версія")
    
    print("\n📌 ВРАЗЛИВА ВЕРСІЯ:")
    print("  ✗ Пряме підставлення користувацького вводу в SQL-запит")
    print("  ✗ Можливість виконання довільних SQL-команд")
    print("  ✗ Витік конфіденційних даних")
    print("  ✗ Можливість обходу авторизації")
    print("  ✗ Можливість модифікації/видалення даних")
    
    print("\n📌 ЗАХИЩЕНА ВЕРСІЯ:")
    print("  ✓ Використання параметризованих запитів (prepared statements)")
    print("  ✓ Автоматичне екранування спеціальних символів")
    print("  ✓ Неможливість виконання довільного SQL-коду")
    print("  ✓ Захист від всіх типів SQL-ін'єкцій")
    print("  ✓ Збереження цілісності даних")
    
    print("\n📌 МЕХАНІЗМ ЗАХИСТУ:")
    print("  • Prepared statements відокремлюють SQL-код від даних")
    print("  • Параметри передаються окремо і обробляються як значення")
    print("  • БД знає структуру запиту до підстановки параметрів")
    print("  • Спеціальні символи (', --, ;) розглядаються як дані, а не код")


def interactive_mode():
    print_separator("ІНТЕРАКТИВНИЙ РЕЖИМ")
    
    vuln = VulnerableApp()
    secure = SecureApp()
    
    while True:
        print("\n" + "-"*70)
        print("Виберіть дію:")
        print("1. Вразлива авторизація")
        print("2. Захищена авторизація")
        print("3. Вразливий пошук")
        print("4. Захищений пошук")
        print("0. Вихід")
        
        choice = input("\nВаш вибір: ").strip()
        
        if choice == "1":
            username = input("Введіть username: ")
            password = input("Введіть password: ")
            result = vuln.login(username, password)
            display_results(result, "користувача")
        
        elif choice == "2":
            username = input("Введіть username: ")
            password = input("Введіть password: ")
            result = secure.login(username, password)
            display_results(result, "користувача")
        
        elif choice == "3":
            search = input("Введіть пошуковий запит: ")
            results = vuln.search_students(search)
            display_results(results)
        
        elif choice == "4":
            search = input("Введіть пошуковий запит: ")
            results = secure.search_students(search)
            display_results(results)
        
        elif choice == "0":
            break


def main():
    print("\n" + "="*70)
    print(" ДЕМОНСТРАЦІЯ SQL-ІН'ЄКЦІЙ ТА МЕТОДІВ ЗАХИСТУ")
    print("="*70)
    
    db = DatabaseManager()
    
    print("\nРЕЖИМИ РОБОТИ:")
    print("1. Автоматична демонстрація (всі сценарії)")
    print("2. Інтерактивний режим (ручне тестування)")
    
    mode = input("\nВиберіть режим (1/2): ").strip()
    
    if mode == "1":
        demo_vulnerable_login()
        demo_secure_login()
        demo_vulnerable_search()
        demo_secure_search()
        demo_comparison()
    else:
        interactive_mode()
    
    print_separator()
    print(" ДЕМОНСТРАЦІЮ ЗАВЕРШЕНО")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()