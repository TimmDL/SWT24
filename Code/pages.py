import streamlit as st
import pandas as pd
from data import books_df, customers_df, save_books_data, save_customers_data


def home_page():
    st.title("Library Admin Dashboard")
    st.header("Welcome to the Library Admin Dashboard")
    st.markdown("Use the sidebar to navigate between different sections of the admin dashboard.")


def manage_page():
    st.title("Manage Books and Users")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Manage Books")
        st.write("### Books List")
        st.dataframe(books_df.style.set_properties(**{'background-color': 'lightgray'}))

        st.write("### Add New Book")
        title = st.text_input("Title", key="add_title")
        author = st.text_input("Author", key="add_author")
        genre = st.text_input("Genre", key="add_genre")
        availability = st.selectbox("Availability", ["Available", "Borrowed"], key="add_availability")

        if st.button("Add Book"):
            new_book = {"Title": title, "Author": author, "Genre": genre, "Availability": availability}
            books_df.loc[len(books_df)] = new_book
            save_books_data()
            st.success("Book added successfully!")
            st.experimental_rerun()

        st.write("### Remove Book")
        remove_book_title = st.selectbox("Select Book to Remove", books_df["Title"].tolist(), key="remove_book")
        if st.button("Remove Book"):
            books_df.drop(books_df[books_df["Title"] == remove_book_title].index, inplace=True)
            save_books_data()
            st.success("Book removed successfully!")
            st.experimental_rerun()

    with col2:
        st.subheader("Manage Users")
        st.write("### Users List")
        st.dataframe(customers_df.style.set_properties(**{'background-color': 'lightgray'}))

        st.write("### Add New User")
        customer_id = st.number_input("Customer ID", min_value=1, step=1, key="add_user_id")
        name = st.text_input("Name", key="add_user_name")
        email = st.text_input("Email", key="add_user_email")

        if st.button("Add User"):
            new_user = {"CustomerID": customer_id, "Name": name, "Email": email, "BorrowedBooks": ""}
            customers_df.loc[len(customers_df)] = new_user
            save_customers_data()
            st.success("User added successfully!")
            st.experimental_rerun()

        st.write("### Remove User")
        remove_user_id = st.selectbox("Select User to Remove", customers_df["CustomerID"].tolist(), key="remove_user")
        if st.button("Remove User"):
            customers_df.drop(customers_df[customers_df["CustomerID"] == remove_user_id].index, inplace=True)
            save_customers_data()
            st.success("User removed successfully!")
            st.experimental_rerun()


def lending_records_page():
    st.title("Lending Records")

    st.subheader("Select Customer")
    customer_id = st.selectbox("Customer ID", customers_df["CustomerID"].tolist())
    selected_customer = customers_df[customers_df["CustomerID"] == customer_id]

    if not selected_customer.empty:
        st.write(
            f"Selected Customer: {selected_customer.iloc[0]['Name']} (Email: {selected_customer.iloc[0]['Email']})")

        st.subheader("Select Books to Borrow")
        available_books = books_df[books_df["Availability"] == "Available"]
        selected_books = st.multiselect("Available Books", available_books["Title"].tolist())

        if st.button("Borrow Books"):
            if selected_books:
                borrowed_books = selected_customer.iloc[0].get('BorrowedBooks', '')
                if pd.isna(borrowed_books):
                    borrowed_books = ''
                borrowed_books_list = borrowed_books.split(", ") if borrowed_books else []
                for book in selected_books:
                    books_df.loc[books_df["Title"] == book, "Availability"] = "Borrowed"
                    borrowed_books_list.append(book)
                customers_df.loc[customers_df["CustomerID"] == customer_id, "BorrowedBooks"] = ", ".join(
                    borrowed_books_list)
                save_books_data()
                save_customers_data()
                st.success("Books borrowed successfully!")
                st.experimental_rerun()
            else:
                st.error("No books selected!")

        st.subheader("Borrowed Books")
        borrowed_books = selected_customer.iloc[0].get('BorrowedBooks', '')
        if pd.isna(borrowed_books):
            borrowed_books = ''
        if borrowed_books:
            borrowed_books_list = borrowed_books.split(", ")
            for book in borrowed_books_list:
                if book:
                    st.write(f"{book}")
        else:
            st.write("No borrowed books")
