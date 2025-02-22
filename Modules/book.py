import hashlib
from datetime import date
class Book:
    def __init__(self, author:str, title:str, year:int, genre:str, qty:int) -> None:
        self.author:str = author
        self.title:str = title
        self.year:int = year
        self.genre:str = genre
        self.quantity:int = qty
        self.taken:int = 0
        self.last_date_taken:date = date.today()
        self.is_deleted:bool = False
        self.id = self.__generate_book_id(author, title,year)
    
    def __generate_book_id(self,author, title, year):

        name = ''.join([author,title,str(year)])

        return hashlib.md5(name.encode()).hexdigest()