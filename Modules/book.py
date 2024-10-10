class Book:
    def __init__(self, id:str, author:str, title:str, year:int, genre:str, qty:int) -> None:
        self.author:str = author
        self.title:str = title
        self.year:int = year
        self.genre:str = genre
        self.quantity:int = qty
        self.available:int = qty
        self.id = id