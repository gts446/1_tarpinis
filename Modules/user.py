from Modules.book import Book
from datetime import date
class User:
    def __init__(self, name:str) -> None:
        self.name = name

class Reader(User):
    def __init__(self, name: str, card_number: str) -> None:
        super().__init__(name)
        self.card_number = card_number
        self.books:dict[str,date] = {}

class Librarian(User):
    def __init__(self, name: str, username:str, password:str) -> None:
        super().__init__(name)
        self.username = username
        self.password = password