import json
import os
import random

# Создаем класс Книги
class Books:
    def __init__(self, title, author, year,  id_book=None, status='В наличии'):
        self.title = title
        self.author = author
        self.year = year
        self.id_book = id_book or self.id_generate()
        self.status = status

# Преобразуем данные книги в формат словаря для json
    def in_json(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "id": self.id_book,
            "status": self.status
        }

    @staticmethod
    def from_json(data):
        return Books(data["title"], data["author"], data["year"], data["id"], data["status"])

    @staticmethod
    def id_generate():
        return random.randint(100000, 999999)


# Создаем класс "Библиотека"
class Library:
    def __init__(self, json_file='librilary.json'):
        self.json_file = json_file
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump([], file)

        self.books_list = self.load_from_json()

# Сохраняем данные в Json
    def save_in_json(self):
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump([about_book.in_json() for about_book in self.books_list], file, indent=4, ensure_ascii=False)

# Загружаем данные из Json
    def load_from_json(self):
        with open(self.json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Books.from_json(book) for book in data]

# Добавляем книгу
    def add_book(self, book):
        self.books_list.append(book)
        self.save_in_json()
        print(f"\nКнига {book.title} добавлена в библиотеку!")

# Меняем статус, только 2 статуса доступны "Выдана" и "В наличии"
    def status_book(self, id_book, status):
        for book in self.books_list:
            if book.id_book == id_book:
                if status.lower() == 'выдана' or status.lower() == 'в наличии':
                    if book.status.lower() == status.lower():
                        print(f'\nКнига с ID "{book.id_book}" уже имеет статус: "{status.title()}"!')
                        return
                    else:
                        book.status = status.title()
                        self.save_in_json()
                        print(f'\nКнига с ID "{book.id_book}" обновлена: новый статус - "{status.title()}"!')
                        return
                else:
                    print("\nДанный статус не подходит для книг!")
                    return
        print(f'\nКнига с ID "{id_book}" не найдена в библиотеке!')

# Удаляем книгу
    def delete_book(self, id_book):
        for book in self.books_list:
            if book.id_book == id_book:
                self.books_list.remove(book)
                self.save_in_json()
                print(f'\nКнига с ID "{book.id_book}" удалена из библиотеки!')
                return
        print(f'\nКнига с ID "{id_book}" не найдена в библиотеке!')

# Поиск книги
    def find_books(self, word_for_find):
        results = [books for books in self.books_list
                   if word_for_find.lower() in books.title.lower()
                   or word_for_find.lower() in books.author.lower()
                   or word_for_find.lower() in books.year.lower()]
        if results:
            print("\nСписок найденных книг:")
            for book in results:
                self.display_book(book)
        else:
            print("\nКнига не найдена.")
        return []

# Показать все книги
    def display_books(self):
        if self.books_list:
            print("\nСписок всех книг:")
            for book in self.books_list:
                self.display_book(book)
        else:
            print("\nВ библиотеке нет книг.")

# Формат показа книг
    @staticmethod
    def display_book(book):
        print(f"ID: {book.id_book}, Название: {book.title}, Автор: {book.author}, Год издания: {book.year}, Статус: {book.status}")
        return


def main():
    library = Library()

    while True:
        print("\nМеню:"
              "\n1. Показать все книги"
              "\n2. Добавить книгу"
              "\n3. Удалить книгу"
              "\n4. Найти книгу"
              "\n5. Изменить статус"
              "\n6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            library.display_books()
        elif choice == "2":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(Books(title, author, year))
        elif choice == "3":
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)
        elif choice == "4":
            info_for_find = input("Введите название, автора или год издания книги для поиска: ")
            library.find_books(info_for_find)
        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            change_status = input("Введите статус книги на который хотите изменить: ")
            library.status_book(book_id, change_status)
        elif choice == "6":
            print("\nВыход из программы.")
            break
        else:
            print("\nНекорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
