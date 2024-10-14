import Modules.helpers as helpers
from Modules.book import Book
from datetime import date
class Library:
    def __init__(self) -> None:
        self.books:dict[str,Book] = helpers.read_from_file('Data_files/books.pkl')
        self.taken_books = []
        users = helpers.read_from_file('Data_files/users.pkl')
        self.users = {}
        self.users['readers'] = users['readers']
        self.users['librarians'] = users['librarians']

    
    def add_book(self, book:Book) -> None:
        if book.id in self.books:
            self.books[book.id].quantity += book.quantity
        else:
            self.books[book.id] = book
        self.__update_books()
    
    def remove_book(self, book_id:str, quantity:int = 0):
            
            """
            Returns:
            int(>0) - Number of books that have been removed
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

            
            self.__update_books()
            return result
    
    def get_books(self, author:str = "", title:str = "", last_taken:date = None):
        return {book_id:book for book_id, book in self.books.items() 
                  if (author=="" or author.lower() in book.author.lower()) and 
                  (title=="" or title.lower() in book.title.lower())}
    
    def get_taken_books():
        pass

    def take_book(self, book_id:str):
        pass

    def __update_books(self):
        helpers.write_to_file('Data_files/books.pkl',self.books)