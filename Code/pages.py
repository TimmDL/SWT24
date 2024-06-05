import streamlit as st
import data


def home_page():
    st.title("Library Admin Dashboard")
    st.header("Welcome to the Library Admin Dashboard")
    st.markdown("Use the sidebar to navigate between different sections of the admin dashboard.")


def manage_page():
    st.title("Manage Books and Users")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Manage Books")
        search_query = st.text_input("Search Books")
        filtered_books = [book for book in data.books_data if search_query.lower() in book["Title"].lower()]
        st.write("### Books List")
        st.dataframe(filtered_books)

        st.write("### Add New Book")
        title = st.text_input("Title", key="add_title")
        author = st.text_input("Author", key="add_author")
        genre = st.text_input("Genre", key="add_genre")
        availability = st.selectbox("Availability", ["Available", "Borrowed"], key="add_availability")

        if st.button("Add Book"):
            new_book = {"Title": title, "Author": author, "Genre": genre, "Availability": availability,
                        "BorrowedBy": ""}
            data.books_data.append(new_book)
            data.save_books(data.books_data)
            st.success("Book added successfully!")
            st.experimental_rerun()

        st.write("### Remove Book")
        remove_book_title = st.selectbox("Select Book to Remove", [book["Title"] for book in data.books_data],
                                         key="remove_book")
        if st.button("Remove Book"):
            data.books_data = [book for book in data.books_data if book["Title"] != remove_book_title]
            data.save_books(data.books_data)
            st.success("Book removed successfully!")
            st.experimental_rerun()

    with col2:
        st.subheader("Manage Users")
        search_query = st.text_input("Search Users")
        filtered_users = [user for user in data.customers_data if search_query.lower() in user["Name"].lower()]
        st.write("### Users List")
        st.dataframe(filtered_users)

        st.write("### Add New User")
        customer_id = st.text_input("Customer ID", key="add_user_id")
        name = st.text_input("Name", key="add_user_name")
        email = st.text_input("Email", key="add_user_email")

        if st.button("Add User"):
            new_user = {"CustomerID": customer_id, "Name": name, "Email": email, "BorrowedBooks": []}
            data.customers_data.append(new_user)
            data.save_customers(data.customers_data)
            st.success("User added successfully!")
            st.experimental_rerun()

        st.write("### Remove User")
        remove_user_id = st.selectbox("Select User to Remove", [user["CustomerID"] for user in data.customers_data],
                                      key="remove_user")
        if st.button("Remove User"):
            data.customers_data = [user for user in data.customers_data if user["CustomerID"] != remove_user_id]
            data.save_customers(data.customers_data)
            st.success("User removed successfully!")
            st.experimental_rerun()


def lending_records_page():

    st.title("Lending Records")

    if "selected_books" not in st.session_state:
        st.session_state.selected_books = []
    if "selected_return_books" not in st.session_state:
        st.session_state.selected_return_books = []
    if "borrow_action" not in st.session_state:
        st.session_state.borrow_action = False
    if "return_action" not in st.session_state:
        st.session_state.return_action = False
    if "confirmation_message" not in st.session_state:
        st.session_state.confirmation_message = ""
    if "confirmation_message_type" not in st.session_state:
        st.session_state.confirmation_message_type = ""
    if "confirm_borrow" not in st.session_state:
        st.session_state.confirm_borrow = False
    if "confirm_return" not in st.session_state:
        st.session_state.confirm_return = False

    def clear_confirmation_message():
        st.session_state.confirmation_message = ""
        st.session_state.confirmation_message_type = ""

    st.subheader("Search and Select Customer")
    search_query = st.text_input("Search by Name or ID")

    if search_query:
        filtered_customers = [user for user in data.customers_data if search_query.lower() in user["Name"].lower() or search_query in user["CustomerID"]]

        if filtered_customers:
            selected_customer_id = st.selectbox("Select Customer", [f"{user['CustomerID']} - {user['Name']}" for user in filtered_customers])
            if selected_customer_id:
                selected_customer_id = selected_customer_id.split(" - ")[0]
                selected_customer = next(user for user in data.customers_data if user["CustomerID"] == selected_customer_id)

                st.write(f"### Selected Customer: {selected_customer['Name']} (Email: {selected_customer['Email']})")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Select Books to Borrow")
                    available_books = [book for book in data.books_data if book["Availability"] == "Available"]
                    st.session_state.selected_books = st.multiselect("Available Books", [book["Title"] for book in available_books])

                    if st.button("Borrow Books"):
                        clear_confirmation_message()
                        if st.session_state.selected_books:
                            st.session_state.confirm_borrow = True
                        else:
                            st.session_state.confirmation_message = "No books selected!"
                            st.session_state.confirmation_message_type = "error"

                with col2:
                    st.subheader("Return Borrowed Books")
                    borrowed_books = selected_customer.get('BorrowedBooks', [])
                    if isinstance(borrowed_books, str):
                        borrowed_books = borrowed_books.split(", ") if borrowed_books else []
                    st.session_state.selected_return_books = st.multiselect("Borrowed Books", borrowed_books)

                    if st.button("Return Books"):
                        clear_confirmation_message()
                        if st.session_state.selected_return_books:
                            st.session_state.confirm_return = True
                        else:
                            st.session_state.confirmation_message = "No books selected for return!"
                            st.session_state.confirmation_message_type = "error"

                st.subheader("Currently Borrowed Books")
                if borrowed_books:
                    for book in borrowed_books:
                        if book:
                            st.write(f"{book}")
                else:
                    st.write("No borrowed books")

                if st.session_state.confirm_borrow:
                    st.write("### Confirm Borrowing")
                    st.write(f"Customer: {selected_customer['Name']} (Email: {selected_customer['Email']})")
                    st.write(f"Books: {', '.join(st.session_state.selected_books)}")
                    if st.button("Confirm Borrow"):
                        borrowed_books = selected_customer.get('BorrowedBooks', [])
                        if isinstance(borrowed_books, str):
                            borrowed_books = borrowed_books.split(", ") if borrowed_books else []
                        for book_title in st.session_state.selected_books:
                            for book in data.books_data:
                                if book["Title"] == book_title:
                                    book["Availability"] = "Borrowed"
                                    book["BorrowedBy"] = selected_customer_id
                                    borrowed_books.append(book_title)
                        selected_customer["BorrowedBooks"] = ", ".join(borrowed_books)
                        data.save_books(data.books_data)
                        data.save_customers(data.customers_data)
                        st.session_state.confirmation_message = "Books borrowed successfully!"
                        st.session_state.confirmation_message_type = "success"
                        st.session_state.confirm_borrow = False
                        st.experimental_rerun()
                    if st.button("Cancel"):
                        st.session_state.confirm_borrow = False

                if st.session_state.confirm_return:
                    st.write("### Confirm Returning")
                    st.write(f"Customer: {selected_customer['Name']} (Email: {selected_customer['Email']})")
                    st.write(f"Books: {', '.join(st.session_state.selected_return_books)}")
                    if st.button("Confirm Return"):
                        borrowed_books = selected_customer.get('BorrowedBooks', [])
                        if isinstance(borrowed_books, str):
                            borrowed_books = borrowed_books.split(", ") if borrowed_books else []
                        for book_title in st.session_state.selected_return_books:
                            borrowed_books.remove(book_title)
                            for book in data.books_data:
                                if book["Title"] == book_title:
                                    book["Availability"] = "Available"
                                    book["BorrowedBy"] = ""
                        selected_customer["BorrowedBooks"] = ", ".join(borrowed_books)
                        data.save_books(data.books_data)
                        data.save_customers(data.customers_data)
                        st.session_state.confirmation_message = "Books returned successfully!"
                        st.session_state.confirmation_message_type = "success"
                        st.session_state.confirm_return = False
                        st.experimental_rerun()
                    if st.button("Cancel"):
                        st.session_state.confirm_return = False

                if st.session_state.confirmation_message:
                    if st.session_state.confirmation_message_type == "success":
                        st.success(st.session_state.confirmation_message)
                    elif st.session_state.confirmation_message_type == "error":
                        st.error(st.session_state.confirmation_message)
        else:
            st.write("No customers found.")
    else:
        st.write("Please enter a search query.")