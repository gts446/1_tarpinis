import Modules as md
import pages
import streamlit as st
import pandas as pd


my_library = md.Library()


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = ""
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

md.helpers.show_messages()


    

if not st.session_state['logged_in']:
    user_type = st.selectbox("Vartotojo tipas",['Skaitytojas', 'Bibliotekininkas'])
    if user_type == "Skaitytojas":
        card_number = st.text_input('Korteles numeris')
    else:
        username = st.text_input('Username')
        password = st.text_input('Password', type="password")
    if st.button('Prisijungti'):
        if user_type == "Skaitytojas":
            if card_number in my_library.readers:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'reader'
                st.session_state['card_number'] = card_number
                st.session_state['name'] = my_library.readers[card_number].name
                st.rerun()
            else:
                st.error("Invalid card number")
        else:
            if username in my_library.librarians and password == my_library.librarians[username].password:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'librarian'
                st.session_state['username'] = username
                st.session_state['name'] = my_library.librarians[username].name
                st.rerun()
            else:
                st.error("Invalid credentials")
    
else:

    st.sidebar.write(f"Sveiki, {st.session_state['name']}")
    st.sidebar.write('MENU:')
    if st.session_state['user_type'] == 'librarian':

        page = 'show-books'
        if st.sidebar.button("Show books") or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.show_books(my_library)

        page = 'add-book'
        if st.sidebar.button("Add book") or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.create_book(my_library)
        
        page = 'add-reader'
        if st.sidebar.button("Add reader") or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.add_reader(my_library)
        
        page = 'taken-books'
        if st.sidebar.button("Show taken books") or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.taken_books(my_library)


    else:
        page = 'show-books-reader'
        if st.sidebar.button("Show library books") or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.show_books_reader(my_library)

        page = 'show-my-books'
        if st.sidebar.button("Show my books") or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.show_my_books(my_library)

    if st.sidebar.button('Logout'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()