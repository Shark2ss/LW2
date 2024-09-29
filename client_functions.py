import sqlite3


class ClientFunctions:

    @staticmethod
    def registration(firm, name, phone_number, type):
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('''
                    INSERT INTO clients (firm, name, phone_number, type, id_property) VALUES (?, ?, ?, ?, ?)
                ''', (firm, name, phone_number, type, 0))

        conn.commit()
        conn.close()

    @staticmethod
    def view_properties():
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM properties')
        properties = cursor.fetchall()
        conn.close()

        return properties

    @staticmethod
    def most_expensive_property():
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM properties ORDER BY price DESC LIMIT 1')
        property = cursor.fetchone()
        conn.close()

        return property

    @staticmethod
    def average_property_price():
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('SELECT AVG(price) FROM properties')
        avg_price = cursor.fetchone()[0]
        conn.close()

        return avg_price

    @staticmethod
    def property_with_most_rooms():
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM properties ORDER BY rooms DESC LIMIT 1')
        property = cursor.fetchone()
        conn.close()

        return property