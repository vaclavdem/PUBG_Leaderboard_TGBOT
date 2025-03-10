import mysql.connector

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYjBmMjI5MC1kYThhLTAxM2QtYmUyOC00NjQ0ZDA0YjAzMzEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzQxMDI2Mjk1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImNsYW5fYm90In0.VP7mJuRRQEJd27HJrEdzEIq1VpCZ3DIOr7GrE0oyxy8"

tg_token = "7397648711:AAFRcN2Rq-2fjrwftgXTi0UDRNlP-ny54bI"

def db_main():
    # Настраиваем параметры соединения
    connection = mysql.connector.connect(
        host="localhost",
        user="Vadim",
        password="7830",
        database="PUBGdatabase"
    )

    cursor = connection.cursor()

    # Создаём таблицу (если её нет)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)

    # Добавляем несколько пользователей
    cursor.execute("INSERT INTO users (name) VALUES (%s)", ("Vadim",))
    connection.commit()

    # Извлекаем все данные
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Закрываем соединение
    cursor.close()
    connection.close()
