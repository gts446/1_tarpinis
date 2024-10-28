import hashlib
from datetime import date
class Book:
    def __init__(self, id:int, author:str, title:str, year:int, genre:int, qty:int, last_taken:date = None, taken:int = 0) -> None:
        self.author:str = author
        self.title:str = title
        self.year:int = year
        self.genre:int = genre
        self.quantity:int = qty
        self.taken:int = taken
        self.last_taken:date = last_taken
        self.is_deleted:bool = False
        self.id = id