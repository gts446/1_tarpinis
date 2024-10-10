import helpers
from book import Book
class Library:
    def __init__(self, books:list[Book]) -> None:
        self.books:dict[str,Book] = helpers.read_from_file('Data_files/books.pkl')
        self.taken_books = []

    
    def add_book(self, book:Book) -> None:
        book_id = helpers.generate_book_id(book.author, book.title, book.year)
        if book_id in self.books:
            self.books[book_id].quantity += book.quantity
        else:
            self.books[book_id] = book
        self.__update_books()
    
    def remove_book(self, book_id:str, quantity:int = 0):
            
            """
            Returns:
            True - Book(s) has been successfully removed
            0 - Book was not found
            int(>0) - Book was found but remaining quantity is less than defined
            """
            if book_id in self.books:
                if quantity:
                    if quantity > self.books[book_id].quantity:
                        return self.books[book_id].quantity
                    elif quantity == self.books[book_id].quantity:
                        del self.books[book_id]
                    else:
                        self.books[book_id].quantity -= quantity
                else:
                     del self.books[book_id]
            else:
                 return 0
            
            self.__update_books()
            return True
    
    def get_books(self, author:str = "", title:str = ""):
        return {book_id:book for book_id, book in self.books 
                  if (author=="" or author == book.author) and (title=="" or author == book.title)}
    
    def get_taken_books():
        pass

    def take_book(self, book_id:str):
        pass

    def __update_books(self):
        helpers.write_to_file('Data_files/books.pkl',self.books)