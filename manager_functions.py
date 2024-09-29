import sqlite3


class ManagerFunctions:
    @staticmethod
    def view_clients():
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clients')
        clients = cursor.fetchall()
        conn.close()

        return clients

    @staticmethod
    def view_realtors():
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM realtors')
        realtors = cursor.fetchall()
        conn.close()

        return realtors

    @staticmethod
    def add_realtor(firm, name, address, phone_number):
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO realtors (firm, name, address, phone_number) VALUES (?, ?, ?, ?)
        ''', (firm, name, address, phone_number,))

        conn.commit()
        conn.close()

