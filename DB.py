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


def is_user_exist(email: str) -> bool:
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    query = '''
        SELECT *
        FROM Users
        WHERE email=?;
    '''
    cursor.execute(query, (email,))    
    response = cursor.fetchall()  
    connection.commit()
    connection.close()
    return bool(response)


def check_password(email: str, password: str) -> bool:
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    query = '''
        SELECT password
        FROM Users
        WHERE email=?;
    '''
    cursor.execute(query, (email,))    
    password_from_db = cursor.fetchall()[0][0]
  
    connection.commit()
    connection.close()
    return password_from_db == password


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

