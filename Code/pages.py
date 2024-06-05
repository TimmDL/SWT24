import streamlit as st
import pandas as pd
import data

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def home_page():
    st.title("Library Admin Dashboard")
    st.header("Welcome to the Library Admin Dashboard")
    st.markdown("Use the sidebar to navigate between different sections of the admin dashboard.")


def manage_page():
    st.title("Manage Books and Customers")

    if "confirm_add_book" not in st.session_state:
        st.session_state.confirm_add_book = False
    if "confirm_remove_book" not in st.session_state:
        st.session_state.confirm_remove_book = False
    if "confirm_add_customer" not in st.session_state:
        st.session_state.confirm_add_customer = False
    if "confirm_remove_customer" not in st.session_state:
        st.session_state.confirm_remove_customer = False
    if "confirmation_message" not in st.session_state:
        st.session_state.confirmation_message = ""
    if "confirmation_message_type" not in st.session_state:
        st.session_state.confirmation_message_type = ""

    def clear_confirmation_message():
        st.session_state.confirmation_message = ""
        st.session_state.confirmation_message_type = ""

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Manage Books")
        search_query_books = st.text_input("Search Books (by Title, Author, Genre, or ISBN)")

        filtered_books = [book for book in data.books_data if
                          search_query_books.lower() in book["Title"].lower() or
                          search_query_books.lower() in book["Author"].lower() or
                          search_query_books.lower() in book["Genre"].lower() or
                          search_query_books in book.get("ISBN", "")]

        filter_option_books = st.radio("Filter Books", ("All", "Available", "Borrowed"), horizontal=True)
        if filter_option_books == "Available":
            filtered_books = [book for book in filtered_books if book["Availability"] == "Available"]
        elif filter_option_books == "Borrowed":
            filtered_books = [book for book in filtered_books if book["Availability"] == "Borrowed"]

        st.write("### Books List")
        st.dataframe(filtered_books, use_container_width=True)

        st.write("### Add New Book")
        title = st.text_input("Title", key="add_title")
        author = st.text_input("Author", key="add_author")
        genre = st.text_input("Genre", key="add_genre")
        isbn = st.text_input("ISBN", key="add_isbn")

        if st.button("Add Book"):
            if not title or not author or not genre or not isbn:
                st.error("All fields must be filled out to add a book.")
            else:
                st.session_state.confirm_add_book = True

        if st.session_state.confirm_add_book:
            st.write("### Confirm Adding Book")
            st.write(f"Title: {title}")
            st.write(f"Author: {author}")
            st.write(f"Genre: {genre}")
            st.write(f"ISBN: {isbn}")
            if st.button("Confirm Add Book"):
                new_book = {"Title": title, "Author": author, "Genre": genre, "ISBN": isbn, "Availability": "Available", "BorrowedBy": ""}
                data.books_data.append(new_book)
                data.save_books(data.books_data)
                st.session_state.confirmation_message = "Book added successfully!"
                st.session_state.confirmation_message_type = "success"
                st.session_state.confirm_add_book = False
                st.experimental_rerun()
            if st.button("Cancel"):
                st.session_state.confirm_add_book = False

        st.write("### Remove Book")
        remove_search_query_books = st.text_input("Search Book to Remove (by Title, Author, Genre, or ISBN)", key="remove_search_query_books")

        filtered_remove_books = [book for book in data.books_data if
                                remove_search_query_books.lower() in book["Title"].lower() or
                                remove_search_query_books.lower() in book["Author"].lower() or
                                remove_search_query_books.lower() in book["Genre"].lower() or
                                remove_search_query_books in book.get("ISBN", "")]

        remove_book_title = st.selectbox("Select Book to Remove", ["" if remove_search_query_books == "" else book["Title"] for book in filtered_remove_books], key="remove_book")

        if st.button("Remove Book"):
            if remove_book_title:
                st.session_state.confirm_remove_book = True
            else:
                st.error("No book selected for removal!")

        if st.session_state.confirm_remove_book:
            st.write("### Confirm Removing Book")
            st.write(f"Book: {remove_book_title}")
            if st.button("Confirm Remove Book"):
                data.books_data = [book for book in data.books_data if book["Title"] != remove_book_title]
                data.save_books(data.books_data)
                st.session_state.confirmation_message = "Book removed successfully!"
                st.session_state.confirmation_message_type = "success"
                st.session_state.confirm_remove_book = False
                st.experimental_rerun()
            if st.button("Cancel"):
                st.session_state.confirm_remove_book = False

    with col2:
        st.subheader("Manage Customers")
        search_query_customers = st.text_input("Search Customers (by Name or ID)")

        filtered_customers = [customer for customer in data.customers_data if
                              search_query_customers.lower() in customer["Name"].lower() or
                              search_query_customers in customer["CustomerID"]]

        filter_option_customers = st.radio("Filter Customers", ("All", "With Borrowed Books", "Without Borrowed Books"), horizontal=True)
        if filter_option_customers == "With Borrowed Books":
            filtered_customers = [customer for customer in filtered_customers if customer.get("BorrowedBooks")]
        elif filter_option_customers == "Without Borrowed Books":
            filtered_customers = [customer for customer in filtered_customers if not customer.get("BorrowedBooks")]

        for customer in filtered_customers:
            if isinstance(customer.get("BorrowedBooks"), list):
                customer["BorrowedBooks"] = ", ".join(customer["BorrowedBooks"])

        st.write("### Customers List")
        st.dataframe(filtered_customers, use_container_width=True)

        st.write("### Add New Customer")
        customer_id = st.text_input("Customer ID", key="add_customer_id")
        name = st.text_input("Name", key="add_customer_name")
        email = st.text_input("Email", key="add_customer_email")
        address = st.text_input("Address", key="add_customer_address")

        if st.button("Add Customer"):
            if not customer_id or not name or not email or not address:
                st.error("All fields must be filled out to add a customer.")
            else:
                st.session_state.confirm_add_customer = True

        if st.session_state.confirm_add_customer:
            st.write("### Confirm Adding Customer")
            st.write(f"Customer ID: {customer_id}")
            st.write(f"Name: {name}")
            st.write(f"Email: {email}")
            st.write(f"Address: {address}")
            if st.button("Confirm Add Customer"):
                new_customer = {"CustomerID": customer_id, "Name": name, "Email": email, "Address": address, "BorrowedBooks": []}
                data.customers_data.append(new_customer)
                data.save_customers(data.customers_data)
                st.session_state.confirmation_message = "Customer added successfully!"
                st.session_state.confirmation_message_type = "success"
                st.session_state.confirm_add_customer = False
                st.experimental_rerun()
            if st.button("Cancel"):
                st.session_state.confirm_add_customer = False

        st.write("### Remove Customer")
        remove_search_query_customers = st.text_input("Search Customer to Remove (by Name or ID)", key="remove_search_query_customers")

        filtered_remove_customers = [customer for customer in data.customers_data if
                                    remove_search_query_customers.lower() in customer["Name"].lower() or
                                    remove_search_query_customers in customer["CustomerID"]]

        remove_customer_id = st.selectbox("Select Customer to Remove", ["" if remove_search_query_customers == "" else f"{customer['CustomerID']} - {customer['Name']}" for customer in filtered_remove_customers], key="remove_customer")

        if st.button("Remove Customer"):
            if remove_customer_id:
                st.session_state.confirm_remove_customer = True
            else:
                st.error("No customer selected for removal!")

        if st.session_state.confirm_remove_customer:
            st.write("### Confirm Removing Customer")
            st.write(f"Customer: {remove_customer_id}")
            if st.button("Confirm Remove Customer"):
                customer_id = remove_customer_id.split(" - ")[0]
                data.customers_data = [customer for customer in data.customers_data if customer["CustomerID"] != customer_id]
                data.save_customers(data.customers_data)
                st.session_state.confirmation_message = "Customer removed successfully!"
                st.session_state.confirmation_message_type = "success"
                st.session_state.confirm_remove_customer = False
                st.experimental_rerun()
            if st.button("Cancel"):
                st.session_state.confirm_remove_customer = False

    if st.session_state.confirmation_message:
        if st.session_state.confirmation_message_type == "success":
            st.success(st.session_state.confirmation_message)
        elif st.session_state.confirmation_message_type == "error":
            st.error(st.session_state.confirmation_message)


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

                st.subheader("Currently Borrowed Books")
                if borrowed_books:
                    for book in borrowed_books:
                        if book:
                            st.write(f"{book}")
                else:
                    st.write("No borrowed books")

                if st.session_state.confirmation_message:
                    if st.session_state.confirmation_message_type == "success":
                        st.success(st.session_state.confirmation_message)
                    elif st.session_state.confirmation_message_type == "error":
                        st.error(st.session_state.confirmation_message)
        else:
            st.write("No customers found.")
    else:
        st.write("Please enter a search query.")

