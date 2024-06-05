import streamlit as st
import json
import data
import time
from ollama import Client

# Function to make a request to the local Ollama server
def query_ollama(prompt):
    client = Client(host='http://localhost:11434')
    response = client.generate(model='phi3', prompt=prompt)
    return response

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

# Helper function to validate JSON structure
def validate_json_structure(json_string):
    try:
        parsed = json.loads(json_string)
        if 'intent' in parsed and 'customer_identifier' in parsed and 'book_identifier' in parsed:
            return parsed
        else:
            return None
    except json.JSONDecodeError:
        return None

# Experimental LLM interface
def experimental():
    st.title("LLM Experimental Interface")
    st.write("Welcome to the LLM interface. You can control the website through text commands.")

    user_input = st.text_area("Enter your command here:")

    if st.button("Submit"):
        if user_input:
            status_placeholder = st.empty()
            progress_bar = st.progress(0)

            status_placeholder.text("Processing command...")

            prompt = (
                f"Convert the following command into a JSON format with keys 'intent', "
                f"'customer_identifier', and 'book_identifier'. Use 'borrow_book' or 'return_book' "
                f"as the intent. Ensure the JSON is properly formatted: {user_input}"
            )
            response = query_ollama(prompt)

            # Debugging print statement
            st.write("### Debugging Response")
            st.write(response)

            # Extract JSON from response
            response_content = response.get('response', '')
            start = response_content.find('```json') + 7
            end = response_content.find('```', start)
            json_string = response_content[start:end].strip()

            # Debugging print statement for extracted JSON
            st.write("### Extracted JSON")
            st.write(json_string)

            # Adjust based on actual response structure
            generated_text = json_string

            progress_bar.progress(50)
            status_placeholder.text("Generating response...")

            st.write("### Generated Text")
            st.write(generated_text)

            for i in range(50, 100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)

            parsed_command = validate_json_structure(generated_text)
            if parsed_command:
                result = execute_command(parsed_command)
                st.write("### LLM Response")
                st.write(result)
            else:
                st.write("### LLM Response")
                st.write(f"Error: Unable to parse the command. Generated text was: {generated_text}")
                st.write("Please ensure your input clearly indicates the customer and book details.")

            progress_bar.progress(100)
            status_placeholder.text("Processing complete.")
        else:
            st.error("Please enter a command.")
