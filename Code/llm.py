import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import data


# Load the model and tokenizer
@st.cache_resource
def load_model():
    MODEL_NAME = "microsoft/Phi-3-medium-128k-instruct"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)


chatbot = load_model()


# Function to find a customer by ID or name
def find_customer(identifier):
    if identifier.isdigit():
        return next((c for c in data.customers_data if c['CustomerID'] == identifier), None)
    else:
        return next((c for c in data.customers_data if c['Name'] == identifier), None)


# Function to find a book by title or ISBN
def find_book(identifier):
    if identifier.replace('-', '').isdigit():
        return next((b for b in data.books_data if b['ISBN'] == identifier), None)
    else:
        return next((b for b in data.books_data if b['Title'] == identifier), None)


# Function to execute commands based on LLM output
def execute_command(parsed_command):
    intent = parsed_command.get('intent')
    customer_identifier = parsed_command.get('customer_identifier')
    book_identifier = parsed_command.get('book_identifier')

    if intent == 'borrow_book':
        return borrow_book(customer_identifier, book_identifier)
    elif intent == 'return_book':
        return return_book(customer_identifier, book_identifier)
    else:
        return "Command not recognized."


# Function to borrow a book
def borrow_book(customer_identifier, book_identifier):
    customer = find_customer(customer_identifier)
    book = find_book(book_identifier)

    if customer and book and book['Availability'] == "Available":
        book["Availability"] = "Borrowed"
        book["BorrowedBy"] = customer["CustomerID"]
        if isinstance(customer["BorrowedBooks"], list):
            customer["BorrowedBooks"].append(book["Title"])
        else:
            customer["BorrowedBooks"] = [book["Title"]]

        data.save_books(data.books_data)
        data.save_customers(data.customers_data)
        return f"{customer['Name']} has borrowed {book['Title']}."
    else:
        return "Error: Customer or book not found, or book is not available."


# Function to return a book
def return_book(customer_identifier, book_identifier):
    customer = find_customer(customer_identifier)
    book = find_book(book_identifier)

    if customer and book and book['Availability'] == "Borrowed":
        book["Availability"] = "Available"
        book["BorrowedBy"] = ""
        if isinstance(customer["BorrowedBooks"], list):
            customer["BorrowedBooks"].remove(book["Title"])
        else:
            customer["BorrowedBooks"] = []

        data.save_books(data.books_data)
        data.save_customers(data.customers_data)
        return f"{customer['Name']} has returned {book['Title']}."
    else:
        return "Error: Customer or book not found, or book is not currently borrowed."


# Experimental LLM interface
def experimental():
    st.title("LLM Experimental Interface")

    # Instructions for the user
    st.write("Welcome to the LLM interface. You can control the website through text commands.")

    # Text input for user commands
    user_input = st.text_area("Enter your command here:")

    if st.button("Submit"):
        if user_input:
            # Process the command through the LLM model
            response = chatbot(user_input, max_length=200)
            generated_text = response[0]['generated_text']

            # Example of parsed_command structure:
            # parsed_command = {
            #     "intent": "borrow_book",
            #     "customer_identifier": "101",
            #     "book_identifier": "978-3-16-148410-0"
            # }

            # Convert the string response to a dictionary
            import ast
            try:
                parsed_command = ast.literal_eval(generated_text)
                result = execute_command(parsed_command)
                st.write("### LLM Response")
                st.write(result)
            except (SyntaxError, ValueError):
                st.write("### LLM Response")
                st.write("Error: Unable to parse the command.")
        else:
            st.error("Please enter a command.")