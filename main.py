import Modules as md
import pages
import streamlit as st
import pandas as pd


my_library = md.Library()


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

    

if not st.session_state['logged_in']:
    user_type = st.selectbox("Vartotojo tipas",['Skaitytojas', 'Bibliotekininkas'])
    if user_type == "Skaitytojas":
        card_number = st.text_input('Korteles numeris')
    else:
        username = st.text_input('Username')
        password = st.text_input('Password', type="password")
    if st.button('Prisijungti'):
        if user_type == "Skaitytojas":
            if card_number in my_library.users['readers']:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'reader'
                st.session_state['card_number'] = card_number
                st.session_state['name'] = my_library.users['readers'][card_number].name
                st.rerun()
            else:
                st.error("Invalid card number")
        else:
            if username in my_library.users['librarians'] and password == my_library.users['librarians'][username].password:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'librarian'
                st.session_state['username'] = username
                st.session_state['name'] = my_library.users['librarians'][username].name
                st.rerun()
            else:
                st.error("Invalid credentials")
    
else:
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = ""
    st.sidebar.write(f"Sveiki, {st.session_state['name']}")
    st.sidebar.write('MENU:')
    if st.session_state['user_type'] == 'librarian':
        if st.sidebar.button("Show books") or st.session_state['current_page'] == 'show-books':
            md.helpers.mark_session('show-books')
            pages.show_books(my_library)

        if st.sidebar.button("Add book") or st.session_state['current_page'] == 'add-book':
            md.helpers.mark_session('add-book')
            pages.create_book(my_library)
            
        if st.sidebar.button("Remove unused books") or st.session_state['current_page'] == 'remove-books':
            md.helpers.mark_session('remove-books')
            pages.remove_books(my_library)