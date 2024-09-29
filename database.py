import sqlite3


def init_db():
    conn = sqlite3.connect('real_estate.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firm TEXT NOT NULL,
            name TEXT NOT NULL,
            phone_number INTEGER NOT NULL,
            type TEXT NOT NULL,
            id_property INTEGER 
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS realtors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firm TEXT NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone_number INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            area INTEGER NOT NULL,
            year_of_construction INTEGER NOT NULL,
            floor INTEGER NOT NULL,
            price REAL NOT NULL,
            rooms INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()

