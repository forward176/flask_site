import sqlite3


def create_user(email: str, password: str) -> None:
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    query = '''
        INSERT INTO Users
        VALUES (?, ?);
    '''
    cursor.execute(query, (email, password))    
    connection.commit()
    connection.close()


def create_table_users():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            email TEXT PRIMARY KEY,
            password TEXT
        );
    ''')
    connection.commit()
    connection.close()


if __name__ == '__main__':
    create_table_users()
    # create_user("tujh.222@mail.ru", 'ewrwe5')

