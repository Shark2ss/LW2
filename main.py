import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import re
from client_functions import ClientFunctions
from realtor_functions import RealtorFunctions
from manager_functions import ManagerFunctions


class RealEstateApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Management")
        self.root.geometry("800x600")

        # Load background image
        self.bg_image = Image.open("background.png")
        self.bg_image = self.bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_menu()

    def main_menu(self):
        self.clear_window()
        self.create_title("Виберіть свою роль")

        self.create_button("Клієнт", self.client_menu).pack(pady=5)
        self.create_button("Ріелтор", self.realtor_menu).pack(pady=5)
        self.create_button("Менеджер", self.manager_menu).pack(pady=5)
        self.create_button("Вихід", self.root.quit).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_button(self, text, command):
        return tk.Button(self.root, text=text, command=command, width=35, height=2)

    def create_title(self, text):
        label = tk.Label(self.root, text=text, font=('Helvetica', 18, 'bold'), bg='#add8e6')
        label.pack(pady=10)
        return label

    def create_table(self, columns, data):
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=0, width=100)
        for item in data:
            tree.insert('', tk.END, values=item)
        tree.pack(pady=5, fill=tk.BOTH, expand=True)
        return tree

    def client_menu(self):
        self.clear_window()
        self.create_title("Клієнт")

        self.create_button("Реєстрація", self.client_registration).pack(pady=5)
        self.create_button("Перегляд списку нерухомостей", self.view_properties).pack(pady=5)
        self.create_button("Найдорожча нерухомість", self.most_expensive_property).pack(pady=5)
        self.create_button("Середня вартість нерухомостей", self.average_property_price).pack(pady=5)
        self.create_button("Нерухомість з найбільшою кількістю кімнат", self.property_with_most_rooms).pack(pady=5)
        self.create_button("Назад", self.main_menu).pack(pady=5)

    def client_registration(self):
        self.clear_window()
        self.create_title("Реєстрація")

        self.create_form(
            [
                ("Назва фірми", 52),
                ("Ім'я", 92),
                ("Номер телефону", 132),
                ("Тип послуги", 172, ["Купівля", "Оренда"]),
            ],
            self.register_client,
            self.client_menu,
        )

    def create_form(self, fields, submit_command, back_command):
        entries = {}
        errors = {}

        for field_info in fields:
            if len(field_info) == 3:
                field, y, options = field_info
            else:
                field, y = field_info
                options = None

            tk.Label(self.root, text=field, font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=y)

            # Якщо є опції, використовуємо випадаючий список, інакше звичайне текстове поле
            entry = ttk.Combobox(self.root, values=options) if options else tk.Entry(self.root)
            entry.place(x=340, y=y + 2)
            entries[field] = entry

            error_label = tk.Label(self.root, text="", font=('Helvetica', 8), fg='red', bg='#add8e6')
            error_label.place(x=340, y=y + 24)
            errors[field] = error_label

        self.create_button("Зареєструватись", lambda: submit_command(entries, errors)).place(x=300, y=300)
        self.create_button("Назад", back_command).place(x=300, y=350)

    def register_client(self, entries, errors):
        firm, name, phone, service_type = entries["Назва фірми"].get(), entries["Ім'я"].get(), entries["Номер телефону"].get(), entries["Тип послуги"].get()
        valid = True

        valid = self.validate_input(firm, errors["Назва фірми"], "Назва фірми не може бути порожньою") and valid
        valid = self.validate_input(name, errors["Ім'я"], "Ім'я не може бути порожнім") and valid
        valid = self.validate_phone(phone, errors["Номер телефону"]) and valid
        valid = self.validate_input(service_type, errors["Тип послуги"], "Тип послуги не може бути порожнім") and valid

        if valid:
            phone = "380" + phone[1:]  # Add country code
            ClientFunctions.registration(firm, name, phone, service_type)
            messagebox.showinfo("Успіх", "Реєстрація успішна")
            self.client_menu()
        else:
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля правильно")

    def validate_input(self, value, error_label, error_message):
        if not value:
            error_label.config(text=error_message)
            return False
        else:
            error_label.config(text="")
            return True

    def validate_phone(self, phone, error_label):
        pattern = r'^0\d{9}$'
        if not phone:
            error_label.config(text="Номер телефону не може бути порожнім")
            return False
        elif not re.match(pattern, phone):
            error_label.config(text="Номер телефону повинен бути у форматі 0ХХХХХХХХХ")
            return False
        else:
            error_label.config(text="")
            return True

    def view_properties(self):
        self.clear_window()
        self.create_title("Список нерухомостей")

        columns = ('ID', 'Адреса', 'Площа', 'Рік побудови', 'Поверх', 'Ціна', 'Кількість кімнат')
        properties = ClientFunctions.view_properties()
        self.create_table(columns, properties)

        self.create_button("Назад", self.client_menu).pack(pady=5)

    def most_expensive_property(self):
        self.display_single_property("Найдорожча нерухомість", ClientFunctions.most_expensive_property)

    def average_property_price(self):
        self.clear_window()
        self.create_title("Середня вартість нерухомостей")

        avg_price = ClientFunctions.average_property_price()
        tk.Label(self.root, text=f"Середня вартість: {avg_price}").pack(pady=10)

        self.create_button("Назад", self.client_menu).pack(pady=5)

    def property_with_most_rooms(self):
        self.display_single_property("Нерухомість з найбільшою кількістю кімнат", ClientFunctions.property_with_most_rooms)

    def display_single_property(self, title, property_function):
        self.clear_window()
        self.create_title(title)

        columns = ('ID', 'Адреса', 'Площа', 'Рік побудови', 'Поверх', 'Ціна', 'Кількість кімнат')
        property = [property_function()]
        self.create_table(columns, property)

        self.create_button("Назад", self.client_menu).pack(pady=5)

    def realtor_menu(self):
        self.clear_window()
        self.create_title("Ріелтор")

        self.create_button("Перегляд списку нерухомостей", self.view_properties_realtor).pack(pady=5)
        self.create_button("Додати нову нерухомість", self.add_property).pack(pady=5)
        self.create_button("Видалити нерухомість", self.delete_property).pack(pady=5)
        self.create_button("Назад", self.main_menu).pack(pady=5)

    def view_properties_realtor(self):
        self.clear_window()
        self.create_title("Список нерухомостей")

        columns = ('ID', 'Адреса', 'Площа', 'Рік побудови', 'Поверх', 'Ціна', 'Кількість кімнат')
        properties = RealtorFunctions.view_properties()
        self.create_table(columns, properties)

        self.create_button("Назад", self.realtor_menu).pack(pady=5)

    def add_property(self):
        self.clear_window()
        self.create_title("Додати нову нерухомість")

        self.create_form(
            [
                ("Адреса", 52),
                ("Площа", 92),
                ("Рік побудови", 132),
                ("Поверх", 172),
                ("Ціна", 212),
                ("Кількість кімнат", 252)
            ],
            self.register_property,
            self.realtor_menu,
        )

    def register_property(self, entries, errors):
        address, area, year, floor, price, rooms = (
            entries["Адреса"].get(),
            entries["Площа"].get(),
            entries["Рік побудови"].get(),
            entries["Поверх"].get(),
            entries["Ціна"].get(),
            entries["Кількість кімнат"].get()
        )

        valid = True
        valid = self.validate_input(address, errors["Адреса"], "Адреса не може бути порожньою") and valid
        valid = self.validate_input(area, errors["Площа"], "Площа не може бути порожньою") and valid
        valid = self.validate_input(year, errors["Рік побудови"], "Рік побудови не може бути порожнім") and valid
        valid = self.validate_input(floor, errors["Поверх"], "Поверх не може бути порожнім") and valid
        valid = self.validate_input(price, errors["Ціна"], "Ціна не може бути порожньою") and valid
        valid = self.validate_input(rooms, errors["Кількість кімнат"], "Кількість кімнат не може бути порожньою") and valid

        if valid:
            RealtorFunctions.add_property(address, area, year, floor, price, rooms)
            messagebox.showinfo("Успіх", "Нерухомість додана")
            self.realtor_menu()
        else:
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля правильно")

    def delete_property(self):
        self.clear_window()
        self.create_title("Видалити нерухомість")

        tk.Label(self.root, text="ID нерухомості", font=('Helvetica', 10, 'bold'), bg='#add8e6').place(x=220, y=52)
        id_entry = tk.Entry(self.root)
        id_entry.place(x=340, y=54)

        def delete():
            property_id = id_entry.get()
            if property_id:
                RealtorFunctions.delete_property(property_id)
                messagebox.showinfo("Успіх", "Нерухомість видалена")
                self.realtor_menu()
            else:
                messagebox.showerror("Помилка", "Будь ласка, введіть ID нерухомості")

        self.create_button("Видалити", delete).place(x=300, y=100)
        self.create_button("Назад", self.realtor_menu).place(x=300, y=150)

    def manager_menu(self):
        self.clear_window()
        self.create_title("Менеджер")

        self.create_button("Перегляд списку клієнтів", self.view_clients).pack(pady=5)
        self.create_button("Перегляд списку ріелторів", self.view_realtors).pack(pady=5)
        self.create_button("Додати нового ріелтора", self.add_realtor).pack(pady=5)
        self.create_button("Назад", self.main_menu).pack(pady=5)

    def view_clients(self):
        self.clear_window()
        self.create_title("Список клієнтів")

        columns = ('ID', 'Назва фірми', "Ім'я", 'Номер телефону', 'Тип послуги')
        clients = ManagerFunctions.view_clients()
        self.create_table(columns, clients)

        self.create_button("Назад", self.manager_menu).pack(pady=5)

    def view_realtors(self):
        self.clear_window()
        self.create_title("Список ріелторів")

        columns = ('ID', "Ім'я", 'Номер телефону')
        realtors = ManagerFunctions.view_realtors()
        self.create_table(columns, realtors)

        self.create_button("Назад", self.manager_menu).pack(pady=5)

    def add_realtor(self):
        self.clear_window()
        self.create_title("Додати ріелтора")

        self.create_form(
            [
                ("Ім'я", 52),
                ("Номер телефону", 92),
            ],
            self.register_realtor,
            self.manager_menu,
        )

    def register_realtor(self, entries, errors):
        name, phone = entries["Ім'я"].get(), entries["Номер телефону"].get()

        valid = True
        valid = self.validate_input(name, errors["Ім'я"], "Ім'я не може бути порожнім") and valid
        valid = self.validate_phone(phone, errors["Номер телефону"]) and valid

        if valid:
            phone = "380" + phone[1:]  # Add country code
            ManagerFunctions.add_realtor(name, phone)
            messagebox.showinfo("Успіх", "Ріелтор доданий")
            self.manager_menu()
        else:
            messagebox.showerror("Помилка", "Будь ласка, заповніть всі поля правильно")


if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()
