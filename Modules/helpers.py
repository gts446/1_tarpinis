# def generate_path(file_name):
#     script_dir = os.path.dirname(__file__)
#     file_path = os.path.join(script_dir, file_name)

#     return file_path
import pickle

def write_to_file(file, data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

def read_from_file(file):
    with open(file, 'rb') as f:   
        return pickle.load(f)
    

import hashlib

def generate_book_id(author, title, year):

    name = ''.join(author,title,year)

    id = hashlib.md5(name.encode()).hexdigest()

    return name

def genres():
    return sorted(["Fiction",
        "Non-fiction",
        "Mystery",
        "Thriller",
        "Fantasy",
        "Science Fiction",
        "Romance",
        "Historical Fiction",
        "Biography",
        "Self-help",
        "Graphic Novel",
        "Poetry",
        "Horror",
        "Adventure",
        "Young Adult",
        "Children's Literature",
        "Classics",
        "Crime",
        "Dystopian",
        "Humor",
        "Memoir",
        "Philosophy",
        "Spirituality",
        "Science",
        "Travel",
        "Western",
        "Drama",
        "Mythology",
        "Short Stories",
        "Psychology"])