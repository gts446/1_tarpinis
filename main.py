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
    pages.show_login(my_library)

else:
    pages.show_sidebar()
    if st.session_state['user_type'] == 'librarian':

        page = 'show-books'
        if st.sidebar.button("Show books", use_container_width=True) or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.show_books(my_library)

        page = 'add-book'
        if st.sidebar.button("Add book", use_container_width=True) or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.create_book(my_library)
        
        page = 'add-reader'
        if st.sidebar.button("Add reader", use_container_width=True) or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.add_reader(my_library)
        
        page = 'taken-books'
        if st.sidebar.button("Show taken books", use_container_width=True) or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.show_taken_books(my_library)


    else:
        page = 'show-books-reader'
        if st.sidebar.button("Show library books", use_container_width=True) or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.show_books_reader(my_library)

        page = 'show-my-books'
        if st.sidebar.button("Show my books", use_container_width=True) or st.session_state['current_page'] == page:
            md.helpers.mark_session(page)
            pages.show_my_books(my_library)

    if st.sidebar.button('Logout'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()