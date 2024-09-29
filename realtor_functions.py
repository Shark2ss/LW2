import sqlite3
from client_functions import ClientFunctions

class RealtorFunctions:
    @staticmethod
    def view_properties():
        return ClientFunctions.view_properties()

    @staticmethod
    def add_property(address, area, year_of_construction, floor, price, rooms):
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO properties (address, area, year_of_construction, floor, price, rooms) VALUES (?, ?, ?, ?, ?, ?)
        ''', (address, area, year_of_construction, floor, price, rooms))

        conn.commit()
        conn.close()

    @staticmethod
    def delete_property(property_id):
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM properties WHERE id=?', (property_id,))

        conn.commit()
        conn.close()