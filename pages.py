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
            readers = my_library.get_readers(card_number)
            if readers:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'reader'
                st.session_state['card_number'] = card_number
                st.session_state['user_id'] = readers[card_number].id
                st.session_state['name'] = readers[card_number].name
                st.rerun()
            else:
                st.error("Invalid card number")
        else:

            librarians = md.helpers.users_to_dict(my_library.get_librarians(),1)
           # st.write(my_library.get_librarians())
            if username in librarians and password == librarians[username]['password']:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = 'librarian'
                st.session_state['username'] = username
                st.session_state['name'] = librarians[username]['name']
                st.rerun()
            else:
                st.error("Invalid credentials")

def show_sidebar():
    st.sidebar.write(f"Hello, {st.session_state['name']}")
    st.sidebar.write('MENU:')

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
                        number_deleted = my_library.remove_old_books(days)
                        st.info(f"{number_deleted} books have been removed")         


        headers = ["Nr.", "Author", "Title","Genre", "Year", "Qty", "Avail.", "Last taken", "Number taken", "Remove"]
        col_widths = [1, 3, 3, 3, 1, 1, 1, 2, 1, 1]

        cols = st.columns(col_widths)
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")
        i = 1
        books = my_library.get_books(author, title)
        if books:
            for book in books.values():
                col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(col_widths)
                col1.markdown(i)
                col2.markdown(book.author)
                col3.markdown(book.title)
                col4.markdown(book.genre)
                col5.markdown(book.year)
                col6.markdown(book.quantity)
                col7.markdown(book.quantity-book.taken)
                if book.last_taken:
                    col8.markdown(f"{(date.today() - book.last_taken).days} days ago")
                else:
                    col8.markdown("N/A")
                col9.markdown(book.taken)
                if col10.button("", key=book.id, icon=":material/delete:"):
                    my_library.remove_book(book.id)
                    st.rerun()
                i +=1
        else:
            st.write("Bo books found")

def create_book(my_library:md.Library):
    with st.form("add-book"):
        st.write("Add new book")
        title = st.text_input('Title')
        author = st.text_input('Author')
        year = st.number_input('Year',1900,2024)
        genres = {genre['id']:genre for genre in my_library.get_genres()}
        genre = st.selectbox('Genre',[genre['id'] for genre in genres.values()], format_func=lambda id: genres[id]['name'])
        quantity = st.number_input('Quantity',1,20)
        if st.form_submit_button('Add'):
            if not title or not author or not year or not genre or not quantity:
                st.error("Please fill all fields")
            elif year > 2024 or year < 1900:
                st.error("Year must be between 1900 and 2024")
            elif quantity < 1 or quantity > 20:
                st.error("Quantity must be between 1900 and 2024")
            else:
                my_library.add_book(md.Book(None, author, title, int(year),genre, quantity))
                st.success("Book successfuly added")

def add_reader(my_library:md.Library):
    readers = my_library.get_readers()
    if readers:
        for reader in readers.values():
            st.write(f"{reader.name} - {reader.card_number}")
    else:
        st.write("There are no readers yet.")
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

    journal = my_library.get_journal()
    if journal:
        headers = ["Nr.", "Book Title", "Book Author","Reader(card_number)", "Taken"]
        col_widths = [1, 3, 3, 3, 1]
        cols = st.columns(col_widths)
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")
        i = 1
        for entry in journal:
            col1, col2, col3, col4, col5 = st.columns(col_widths)
            col1.markdown(i)
            col2.markdown(entry['title'])
            col3.markdown(entry['author'])
            col4.markdown(f"{entry['name']}({entry['card_number']})")
            duration = date.today() - entry['date_taken']
            if duration.days > 30:
                col5.markdown(f'<span style="color:red">{duration.days} days ago</span>',unsafe_allow_html=True)
            else:
                col5.markdown(f'<span style="color:green">{duration.days} days ago</span>',unsafe_allow_html=True)
            i +=1
    else:
        st.write("There are no taken books")

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
                can_take = True
                my_journal = my_library.get_journal(st.session_state['user_id'])
                if my_journal:
                    for entry in my_journal:
                        if book.id == entry['book_id']:
                            st.session_state['messages'].append({'status':'warning','text':'You already have a copy of this book'})
                            can_take = False
                            break
                        duration = date.today() - entry['date_taken']
                        if duration.days > 30:
                            can_take = False
                            st.session_state['messages'].append({'status':'warning','text':'You have overdue books. Return them before taking new books'})
                            break
                if can_take:
                    my_library.give_book(st.session_state['user_id'], book.id)
                    st.session_state['messages'].append({'status':'success','text':'Book successfully taken'})
                st.rerun()

def show_my_books(my_library: md.Library):
    headers = ["Nr.", "Author", "Title", "Year", "Taken", "Action"]
    col_widths = [1, 3, 3, 1, 1, 1]

    cols = st.columns(col_widths)
    for col, header in zip(cols, headers):
        col.write(f"**{header}**")
    i = 1
    my_journal = my_library.get_journal(st.session_state['card_number'])
    if my_journal:
        for book in my_journal:
            col1, col2, col3, col4, col5, col6 = st.columns(col_widths)
            col1.markdown(i)
            col2.markdown(book['author'])
            col3.markdown(book['title'])
            col4.markdown(book['year'])
            duration = date.today() - book['date_taken']
            if duration.days > 30:
                col5.markdown(f'<span style="color:red">{duration.days} days ago</span>',unsafe_allow_html=True)
            else:
                col5.markdown(f'<span style="color:green">{duration.days} days ago</span>',unsafe_allow_html=True)
            i +=1
            if col6.button("Return", key=book_id):
                my_library.return_book(my_library.readers[st.session_state['card_number']], books[book_id])
                st.session_state['messages'].append({'status':'success','text':'Book successfully returned'})
                st.rerun()
    else:
        st.write("No taken books")
