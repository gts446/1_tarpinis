import Modules as md
import streamlit as st
from datetime import date, timedelta


def show_login(my_library: md.Library):
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
        col1.markdown(i)
        col2.markdown(book.author)
        col3.markdown(book.title)
        col4.markdown(book.year)
        col5.markdown(book.quantity)
        col6.markdown(book.quantity-book.taken)
        col7.markdown(f"{(date.today() - book.last_date_taken).days} days ago")
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

def add_reader(my_library:md.Library):
    for user in my_library.readers.values():
        st.write(f"{user.name} - {user.card_number}")
    with st.form("reader"):
        name = st.text_input("Name")
        card_number = st.text_input("Card number")
        if st.form_submit_button("Create"):
            if name and card_number:
                reader = md.Reader(name, card_number)
                if my_library.add_reader(reader):
                    st.success(f"Reader **{name}** card successfully created")
                else:
                    st.warning(f"Reader card **{card_number}** already exists")
            else:
                st.warning("Please fill all fields")

def show_taken_books(my_library:md.Library):

    books = my_library.get_books()
    for reader in my_library.readers.values():
        if not reader.books:
            continue
        st.write(reader.name)
        headers = ["Nr.", "Book Title", "Book Author", "Taken"]
        col_widths = [1, 3, 3, 1]
        cols = st.columns(col_widths)
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")
        i = 1
        for book_id, date_taken in reader.books.items():
            col1, col2, col3, col4 = st.columns(col_widths)
            col1.markdown(i)
            col2.markdown(books[book_id].title)
            col3.markdown(books[book_id].author)
            duration = date.today() - date_taken
            if duration.days > 30:
                col4.markdown(f'<span style="color:red">{duration.days} days ago</span>',unsafe_allow_html=True)
            else:
                col4.markdown(f'<span style="color:green">{duration.days} days ago</span>',unsafe_allow_html=True)
            i +=1

def show_books_reader(my_library: md.Library):
    col1, col2 = st.columns([1,1])

    with col1:
        author = st.text_input("Author")

    with col2:
        title = st.text_input("Title")        


    headers = ["Nr.", "Author", "Title", "Year", "Avail.", "Action"]
    col_widths = [1, 3, 3, 1, 1, 1]

    cols = st.columns(col_widths)
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")
    i = 1
    for book in my_library.get_books(author, title).values():

        col1, col2, col3, col4, col5, col6 = st.columns(col_widths)
        col1.markdown(i)
        col2.write(book.author)
        col3.write(book.title)
        col4.markdown(book.year)
        remaining = book.quantity-book.taken
        if remaining == 0:
            col5.markdown(f'<span style="color:red">{remaining}</span>',unsafe_allow_html=True)
        else:
            col5.markdown(f'<span style="color:green">{remaining}</span>',unsafe_allow_html=True)
        i +=1
        if remaining > 0:
            if col6.button("Take", key=book.id):
                if book.id in my_library.readers[st.session_state['card_number']].books:
                    st.session_state['messages'].append({'status':'warning','text':'You already have a copy of this book'})
                else:
                    allow_takeaway = True
                    for book_id, date_taken in my_library.readers[st.session_state['card_number']].books.items():
                        duration = date.today() - date_taken
                        if duration.days > 30:
                            allow_takeaway = False
                            break
                    if allow_takeaway:
                        my_library.give_book(my_library.readers[st.session_state['card_number']], book)
                        st.session_state['messages'].append({'status':'success','text':'Book successfully taken'})
                    else:
                        st.session_state['messages'].append({'status':'warning','text':'You have overdue books. Return them before taking new books'})
                st.rerun()

def show_my_books(my_library: md.Library):
    headers = ["Nr.", "Author", "Title", "Year", "Taken", "Action"]
    col_widths = [1, 3, 3, 1, 1, 1]

    cols = st.columns(col_widths)
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")
    i = 1
    books = my_library.get_books()
    for book_id, date_taken in my_library.readers[st.session_state['card_number']].books.items():
        col1, col2, col3, col4, col5, col6 = st.columns(col_widths)
        col1.markdown(i)
        col2.write(books[book_id].author)
        col3.write(books[book_id].title)
        col4.markdown(books[book_id].year)
        duration = date.today() - date_taken
        if duration.days > 30:
            col5.markdown(f'<span style="color:red">{duration.days} days ago</span>',unsafe_allow_html=True)
        else:
            col5.markdown(f'<span style="color:green">{duration.days} days ago</span>',unsafe_allow_html=True)
        i +=1
        if col6.button("Return", key=book_id):
            my_library.return_book(my_library.readers[st.session_state['card_number']], books[book_id])
            st.session_state['messages'].append({'status':'success','text':'Book successfully returned'})
            st.rerun()