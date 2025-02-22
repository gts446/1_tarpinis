# def generate_path(file_name):
#     script_dir = os.path.dirname(__file__)
#     file_path = os.path.join(script_dir, file_name)

#     return file_path
import pickle
import streamlit as st

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

def mark_session(page):
    if st.session_state['current_page'] != page:
        st.session_state['current_page'] = page
        st.rerun()

def show_messages():
    if st.session_state['messages']:
        for message in st.session_state['messages']:
            if message['status'] == 'warning':
                st.warning(message['text'])
            elif message['status'] == 'success':
                st.success(message['text'])
        st.session_state['messages'] = []