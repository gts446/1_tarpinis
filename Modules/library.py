import Modules.helpers as helpers
from Modules.book import Book
from Modules.user import Reader, Librarian
from Modules.db import Database
from datetime import date, timedelta

my_db = Database()
class Library:
    def __init__(self) -> None:
        pass

    
    def add_book(self, book:Book) -> None:
        existing_book = self.get_book(None, book.author, book.title)
        if existing_book:
            self.book_increment(existing_book.id, book.quantity)
        else:
            my_db.query('INSERT INTO books (title, author, year, genre, quantity) VALUES (?,?,?,?,?)',(book.title, book.author, book.year, book.genre, book.quantity))

    
    def book_increment(self, id:int, qty:int):
        my_db.query('UPDATE books SET quantity = quantity + ? WHERE books.id = ?',(qty,id))

    def get_genres(self):
        return my_db.query("SELECT * FROM genres")

    def get_number_of_books_taken(self, book_id):
        result =  my_db.query("SELECT COUNT(*) FROM journal WHERE book_id = ?",(book_id,))
        print(result)

    def remove_old_books(self, days:int):
        books = self.get_books()
        datepoint = date.today() + timedelta(days)
        counter = 0
        if books:
            for book in books.values():
                if book.last_taken and book.last_taken < datepoint:
                    counter += self.remove_book(book.id)
        return counter


    def remove_book(self, book_id:str, quantity:int = 0):
            """
            Returns:
            int - Number of books that have been removed
            """
            result = 0
            book = self.get_book(book_id)
            if not book:
                return result
            remaining = book.quantity - book.taken
            if quantity:
                if quantity > remaining:
                    return result
                else:
                    self.book_increment(book.id, quantity*-1)
                    result = quantity
            else:
                    self.book_increment(book.id, remaining*-1)
                    result = remaining
            return result

    def get_book(self, id:int=None, author:str = None, title:str = None):
        """
        Returns Book object if book was found.
        Returns None if no book found
        
        """
        qry = """
            SELECT books.id, 
            books.title, 
            books.author, 
            genres.name AS 'genre',
            books.quantity,
            books.year,
            MAX(journal.date_taken) AS 'last_taken',
            SUM(CASE WHEN journal.date_returned IS NOT NULL THEN 1 ELSE 0 END) as 'taken'
            FROM books 
            LEFT JOIN journal 
            ON journal.book_id = books.id
            LEFT JOIN genres
            ON genres.id = books.genre
            WHERE quantity > 0"""    
        if id:
            qry += " AND books.id = ?"
            qry += " GROUP BY books.id, books.title, books.author, genres.name, books.quantity, books.year ORDER BY books.id"
            books = my_db.query(qry, id)
        elif author and title:
            qry += " AND LOWER(books.author) = ? AND LOWER(books.title) = ?"
            qry += " GROUP BY books.id, books.title, books.author, genres.name, books.quantity, books.year ORDER BY books.id"
            books = my_db.query(qry, (author.lower(), title.lower()))
        else:
            print("Please provide only id, or author and title")
            return False
        if books:
            book = books[0]
            return Book(book['id'], book['author'],book['title'], book['year'], book['genre'], book['quantity'], book['last_taken'], book['taken'])
        else:
            return None
            

    def get_books(self, author:str = "", title:str = ""):
        """
        Return dict[book_id:Book] if any books were found
        Return None if no books were found
        """
        books: dict[int, Book] = {}
        qry = """
        SELECT books.id, 
        books.title, 
        books.author, 
        genres.name AS 'genre',
        books.quantity,
        books.year,
        MAX(journal.date_taken) AS 'last_taken',
        SUM(CASE WHEN journal.book_id IS NOT NULL AND journal.date_returned IS NULL THEN 1 ELSE 0 END) as 'taken'
        FROM books 
        LEFT JOIN journal 
        ON journal.book_id = books.id
        LEFT JOIN genres
        ON genres.id = books.genre
        WHERE quantity > 0"""
        if author:
            qry += f" AND LOWER(books.author) LIKE '%{author.lower()}%'"
        if title:
            qry += f" AND LOWER(books.title) LIKE '%{title.lower()}%'"

        qry += " GROUP BY books.id, books.title, books.author, genres.name, books.quantity, books.year ORDER BY books.id"
        qry_result = my_db.query(qry)
        if qry_result:
            for book in qry_result:
                books[book['id']] = Book(book['id'], book['author'],book['title'],book['year'], book['genre'], book['quantity'], book['last_taken'], book['taken'])
            return books
        else:
            return None
    
    def add_reader(self, reader:Reader):
        a = self.get_readers(reader.card_number)
        if a == None:
            my_db.query("INSERT INTO users (name, card_number, type) VALUES(?,?,2)", (reader.name, reader.card_number))
            return True
        else:
            return False
        
    def give_book(self, user_id, book_id):
        my_db.query("INSERT INTO journal (book_id, user_id, date_taken) VALUES (?,?,?)", (book_id, user_id, date.today()))

    def get_readers(self, card_number = None):
        """
        Returns dict[card_number:int,Reader] if any readers were found
        Return None if no readers were found
        """
        result: dict[int,Reader] = {}
        if card_number:
            readers = my_db.query("SELECT * FROM users WHERE type = 2 AND card_number = ?", (card_number,))
        else:
            readers = my_db.query("SELECT * FROM users WHERE type = 2")
        if readers:
            for reader in readers:
                result[reader['card_number']] = Reader(reader['name'], reader['card_number'], reader['id'])
        else:
            result = None
        return result

    def get_journal(self, user_id:int = None):
        if user_id:  
            return my_db.query("""
                SELECT books.id as 'book_id', books.title, books.author, books.year,
                users.name, users.card_number, 
                journal.date_taken, journal.date_returned
                FROM journal
                LEFT JOIN books
                ON journal.book_id = books.id
                LEFT JOIN users
                ON journal.user_id = users.id
                WHERE journal.date_returned IS NULL AND journal.user_id = ?
                """, (user_id,))
        else:
            return my_db.query("""
                SELECT books.id as 'book_id', books.title, books.author, books.year,
                users.name, users.card_number, 
                journal.date_taken, journal.date_returned
                FROM journal
                LEFT JOIN books
                ON journal.book_id = books.id
                LEFT JOIN users
                ON journal.user_id = users.id
                WHERE journal.date_returned IS NULL
                """)


    def return_book(self, user_id, book_id):
        my_db.query("UPDATE journal SET date_returned = GETDATE() WHERE book_id = ? AND user_id = ? AND date_returned IS NULL", (book_id, user_id))

    def get_librarians(self):
        return my_db.query("SELECT * FROM users WHERE type = 1")

    def __update_books_pkl(self):
        helpers.write_to_file('Data_files/books.pkl',self.books)

    def __update_readers_pkl(self):
        helpers.write_to_file('Data_files/readers.pkl',self.readers)