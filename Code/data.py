import pandas as pd

# Load data from CSV files
books_df = pd.read_csv("Data/books.csv")
customers_df = pd.read_csv("Data/customers.csv")

# Ensure the BorrowedBooks column exists and is a string
if "BorrowedBooks" not in customers_df.columns:
    customers_df["BorrowedBooks"] = ""

# Save data to CSV files
def save_books_data():
    books_df.to_csv("books.csv", index=False)

def save_customers_data():
    customers_df.to_csv("customers.csv", index=False)
