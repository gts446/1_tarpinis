# def generate_path(file_name):
#     script_dir = os.path.dirname(__file__)
#     file_path = os.path.join(script_dir, file_name)

#     return file_path

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