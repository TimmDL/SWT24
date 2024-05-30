import streamlit as st
from pages import home_page, manage_page, lending_records_page


def main():
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    st.sidebar.title("Library Admin Dashboard")
    page = st.sidebar.radio("Go to", ["Home", "Manage Books and Users", "Lending Records"])

    if page == "Home":
        home_page()
    elif page == "Manage Books and Users":
        manage_page()
    elif page == "Lending Records":
        lending_records_page()


if __name__ == "__main__":
    main()
