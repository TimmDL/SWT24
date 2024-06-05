import json
import os

# Define the paths to the JSON files using relative paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
books_file_path = os.path.join(base_dir, 'Data', 'books.json')
customers_file_path = os.path.join(base_dir, 'Data', 'customers.json')

# Load data from JSON files
def load_books():
    with open(books_file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)

def load_customers():
    with open(customers_file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)

# Save data to JSON files
def save_books(data):
    with open(books_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_customers(data):
    with open(customers_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

books_data = load_books()
customers_data = load_customers()