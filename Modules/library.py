import Modules.helpers as helpers
from Modules.book import Book
from Modules.user import Reader, Librarian
from datetime import date
class Library:
    def __init__(self) -> None:
        self.books:dict[str,Book] = helpers.read_from_file('Data_files/books.pkl')
        self.readers:dict[str,Reader] = helpers.read_from_file('Data_files/readers.pkl')
        self.librarians = helpers.read_from_file('Data_files/librarians.pkl')

    
    def add_book(self, book:Book) -> None:
        if book.id in self.books:
            self.books[book.id].quantity += book.quantity
        else:
            self.books[book.id] = book
        self.__update_books_pkl()
    
    def remove_book(self, book_id:str, quantity:int = 0):
            
            """
            Returns:
            int - Number of books that have been removed
            """
            result = 0
            if book_id not in self.books:
                return result
            remaining = self.books[book_id].quantity - self.books[book_id].taken
            if quantity:
                if quantity > remaining:
                    return result
                else:
                    self.books[book_id].quantity -= quantity
                    result = quantity
            else:
                    self.books[book_id].quantity -= remaining
                    result = remaining

            
            self.__update_books_pkl()
            return result
    
    def get_books(self, author:str = "", title:str = "", ids:list = ""):
        return {book_id:book for book_id, book in self.books.items() 
                  if (author=="" or author.lower() in book.author.lower()) and 
                  (title=="" or title.lower() in book.title.lower()) and 
                  (ids=="" or book.id in ids)}
    
    def add_reader(self, reader:Reader):
        if reader.card_number not in self.readers:
            self.readers[reader.card_number] = reader
            helpers.write_to_file('Data_files/readers.pkl', self.readers)
            return True
        else:
            return False
        
    def give_book(self, reader:Reader, book:Book):
        self.readers[reader.card_number].books[book.id] = date.today()
        self.__update_readers_pkl()

        self.books[book.id].taken += 1
        self.__update_books_pkl()

    def __update_books_pkl(self):
        helpers.write_to_file('Data_files/books.pkl',self.books)

    def __update_readers_pkl(self):
        helpers.write_to_file('Data_files/readers.pkl',self.readers)