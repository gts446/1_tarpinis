from Modules.book import Book
from datetime import date
class User:
    def __init__(self, name:str, id:int) -> None:
        self.name = name
        self.id = id

class Reader(User):
    def __init__(self, name: str, card_number: str, id:int) -> None:
        super().__init__(name, id)
        self.card_number = card_number
        self.books:dict[str,date] = {}

class Librarian(User):
    def __init__(self, name: str, username:str, password:str, id:int) -> None:
        super().__init__(name, id)
        self.username = username
        self.password = password