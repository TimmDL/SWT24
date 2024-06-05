import streamlit as st
from pages import home_page, manage_page, lending_records_page
from llm import experimental  # Import the experimental function

# Set the page configuration as the first Streamlit command
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def main():
    st.sidebar.title("Library Admin Dashboard")
    page = st.sidebar.radio("Go to", ["Home", "Manage Books and Users", "Lending Records", "Experimental LLM Interface"])

    if page == "Home":
        home_page()
    elif page == "Manage Books and Users":
        manage_page()
    elif page == "Lending Records":
        lending_records_page()
    elif page == "Experimental LLM Interface":
        experimental()

if __name__ == "__main__":
    main()

# Jane Doe wants to borrow The Great Gatsby