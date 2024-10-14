import Modules as md
import streamlit as st
from datetime import date, timedelta

def show_books(my_library: md.Library):
    col1, col2, col3 = st.columns([1,1,1], vertical_alignment='bottom')

    with col1:
        author = st.text_input("Author")

    with col2:
        title = st.text_input("Title")

    with col3:
        with st.form("oldbooks"):
            days = st.number_input('Days:',value=365)
            if st.form_submit_button("Delete old books",use_container_width=True):
                try: 
                    days = abs(int(days))
                except:
                    st.error("Enter a number")
                
                if isinstance(days,int):
                    datepoint = date.today() - timedelta(days=days)
                    number_deleted = 0
                    for book in my_library.books.values():
                        if book.last_date_taken <= datepoint:
                            number_deleted += my_library.remove_book(book.id)
                    st.info(f"{number_deleted} books have been removed")         


    headers = ["Nr.", "Author", "Title", "Year", "Qty", "Avail.", "Last taken", "Remove"]
    col_widths = [1, 3, 3, 1, 1, 1, 2, 1]

    cols = st.columns(col_widths)
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")
    i = 1
    for book in my_library.get_books(author, title).values():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(col_widths)
        col1.write(i)
        col2.write(book.author)
        col3.write(book.title)
        col4.write(book.year)
        col5.write(book.quantity)
        col6.write(book.quantity-book.taken)
        col7.write(f"{(date.today() - book.last_date_taken).days} days ago")
        if col8.button("", key=book.id, icon=":material/delete:"):
            my_library.remove_book(book.id)
            st.rerun()
        i +=1

def create_book(my_library:md.Library):
    with st.form("add-book"):
        st.write("Add new book")
        title = st.text_input('Title')
        author = st.text_input('Author')
        year = st.number_input('Year',1900,2024)
        genre = st.selectbox('Genre',md.helpers.genres())
        quantity = st.number_input('Quantity',1,20)
        if st.form_submit_button('Add'):
            if not title or not author or not year or not genre or not quantity:
                st.error("Please fill all fields")
            else:
                my_library.add_book(md.Book(author, title, int(year),genre, quantity))
                st.success("Book successfuly added")

def remove_books(my_library:md.Library):
    headers = ["Nr.", "Author", "Title", "Year", "Qty", "Avail.", "Last taken"]
    col_widths = [1, 3, 3, 1, 1, 1, 2]

    cols = st.columns(col_widths)
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")
    i = 1
    for book in my_library.get_books().values():
        col1, col2, col3, col4, col5, col6, col7 = st.columns(col_widths)
        col1.write(i)
        col2.write(book.author)
        col3.write(book.title)
        col4.write(book.year)
        col5.write(book.quantity)
        col6.write(book.available)
        col7.write(f"{(date.today() - book.last_date_taken).days} days ago")
        i +=1