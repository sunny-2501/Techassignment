import pandas as pd
from datetime import datetime, timedelta
from IPython.display import display

# -----------------------------
# 1. Create sample book data
# -----------------------------
books = pd.DataFrame({
    "Book_ID": [101, 102, 103, 104, 105, 106, 107, 108],
    "Title": [
        "Python Basics",
        "Data Science Handbook",
        "Database Management",
        "Clean Code",
        "Machine Learning",
        "Operating Systems",
        "Computer Networks",
        "Web Development"
    ],
    "Author": [
        "Mark Lutz",
        "Jake VanderPlas",
        "Raghu Ramakrishnan",
        "Robert Martin",
        "Tom Mitchell",
        "Silberschatz",
        "Andrew Tanenbaum",
        "Jon Duckett"
    ],
    "Category": [
        "Programming",
        "Data Science",
        "Database",
        "Programming",
        "AI",
        "Systems",
        "Networking",
        "Web"
    ],
    "Year": [2021, 2020, 2019, 2022, 2021, 2018, 2020, 2022],
    "Available": [True, True, True, False, True, True, False, True]
})

# -----------------------------
# 2. Create sample member data
# -----------------------------
members = pd.DataFrame({
    "Member_ID": [1, 2, 3, 4, 5],
    "Member_Name": [
        "Amit Sharma",
        "Priya Verma",
        "Rahul Singh",
        "Neha Gupta",
        "Akash Yadav"
    ],
    "Department": [
        "Information Technology",
        "Computer Science",
        "Information Technology",
        "Data Science",
        "Computer Applications"
    ],
    "Phone": [
        "9876543210",
        "9876543211",
        "9876543212",
        "9876543213",
        "9876543214"
    ]
})

# -----------------------------
# 3. Create issue transaction data
# -----------------------------
transactions = pd.DataFrame({
    "Transaction_ID": [1, 2, 3],
    "Book_ID": [104, 107, 102],
    "Member_ID": [1, 3, 2],
    "Issue_Date": [
        "2026-09-01",
        "2026-09-03",
        "2026-09-05"
    ],
    "Return_Date": [None, None, "2026-09-10"],
    "Status": ["Issued", "Issued", "Returned"]
})

# -----------------------------
# 4. Display all records
# -----------------------------
print("BOOKS")
display(books)

print("MEMBERS")
display(members)

print("TRANSACTIONS")
display(transactions)


# -----------------------------
# 5. Search books
# -----------------------------
def search_books(keyword):
    result = books[
        books["Title"].str.contains(keyword, case=False, na=False) |
        books["Author"].str.contains(keyword, case=False, na=False) |
        books["Category"].str.contains(keyword, case=False, na=False)
    ]

    if result.empty:
        print("No matching books found.")
    else:
        display(result)

print("Search result for 'Python':")
search_books("Python")


# -----------------------------
# 6. Show available books
# -----------------------------
def available_books():
    result = books[books["Available"] == True]

    print("AVAILABLE BOOKS")
    display(result)

available_books()


# -----------------------------
# 7. Add a new book
# -----------------------------
def add_book(book_id, title, author, category, year):
    global books

    if book_id in books["Book_ID"].values:
        print("Book ID already exists.")
        return

    new_book = pd.DataFrame([{
        "Book_ID": book_id,
        "Title": title,
        "Author": author,
        "Category": category,
        "Year": year,
        "Available": True
    }])

    books = pd.concat([books, new_book], ignore_index=True)
    print("Book added successfully.")

add_book(
    109,
    "Artificial Intelligence",
    "Stuart Russell",
    "AI",
    2023
)

display(books)


# -----------------------------
# 8. Add a new member
# -----------------------------
def add_member(member_id, name, department, phone):
    global members

    if member_id in members["Member_ID"].values:
        print("Member ID already exists.")
        return

    new_member = pd.DataFrame([{
        "Member_ID": member_id,
        "Member_Name": name,
        "Department": department,
        "Phone": phone
    }])

    members = pd.concat([members, new_member], ignore_index=True)
    print("Member added successfully.")

add_member(
    6,
    "Rohit Kumar",
    "Information Technology",
    "9876543215"
)

display(members)


# -----------------------------
# 9. Issue a book
# -----------------------------
def issue_book(book_id, member_id):
    global books, transactions

    if book_id not in books["Book_ID"].values:
        print("Book does not exist.")
        return

    if member_id not in members["Member_ID"].values:
        print("Member does not exist.")
        return

    book_index = books.index[books["Book_ID"] == book_id][0]

    if books.loc[book_index, "Available"] is not True:
        print("Book is not available.")
        return

    next_transaction_id = (
        transactions["Transaction_ID"].max() + 1
        if not transactions.empty else 1
    )

    issue_date = datetime.today().strftime("%Y-%m-%d")

    new_transaction = pd.DataFrame([{
        "Transaction_ID": next_transaction_id,
        "Book_ID": book_id,
        "Member_ID": member_id,
        "Issue_Date": issue_date,
        "Return_Date": None,
        "Status": "Issued"
    }])

    transactions = pd.concat(
        [transactions, new_transaction],
        ignore_index=True
    )

    books.loc[book_index, "Available"] = False
    print("Book issued successfully.")

issue_book(103, 4)

display(books)
display(transactions)


# -----------------------------
# 10. Return a book
# -----------------------------
def return_book(book_id):
    global books, transactions

    active_transaction = transactions[
        (transactions["Book_ID"] == book_id) &
        (transactions["Status"] == "Issued")
    ]

    if active_transaction.empty:
        print("No active issue found for this book.")
        return

    transaction_index = active_transaction.index[0]
    book_index = books.index[books["Book_ID"] == book_id][0]

    transactions.loc[transaction_index, "Return_Date"] = (
        datetime.today().strftime("%Y-%m-%d")
    )
    transactions.loc[transaction_index, "Status"] = "Returned"
    books.loc[book_index, "Available"] = True

    print("Book returned successfully.")

return_book(104)

display(books)
display(transactions)


# -----------------------------
# 11. Member borrowing history
# -----------------------------
def member_history(member_id):
    result = transactions[
        transactions["Member_ID"] == member_id
    ].merge(
        books[["Book_ID", "Title", "Author"]],
        on="Book_ID",
        how="left"
    )

    if result.empty:
        print("No borrowing history found.")
    else:
        display(result)

print("Borrowing history of Member 1:")
member_history(1)


# -----------------------------
# 12. Category-wise book count
# -----------------------------
category_summary = (
    books.groupby("Category")
    .size()
    .reset_index(name="Book_Count")
    .sort_values("Book_Count", ascending=False)
)

print("CATEGORY-WISE BOOK COUNT")
display(category_summary)


# -----------------------------
# 13. Most borrowed books
# -----------------------------
borrowed_summary = (
    transactions.groupby("Book_ID")
    .size()
    .reset_index(name="Borrow_Count")
    .merge(
        books[["Book_ID", "Title"]],
        on="Book_ID",
        how="left"
    )
    .sort_values("Borrow_Count", ascending=False)
)

print("MOST BORROWED BOOKS")
display(borrowed_summary)


# -----------------------------
# 14. Active issued books
# -----------------------------
active_issues = transactions[
    transactions["Status"] == "Issued"
].merge(
    books[["Book_ID", "Title"]],
    on="Book_ID",
    how="left"
).merge(
    members[["Member_ID", "Member_Name"]],
    on="Member_ID",
    how="left"
)

print("CURRENTLY ISSUED BOOKS")
display(active_issues)


# -----------------------------
# 15. Library summary report
# -----------------------------
summary = pd.DataFrame({
    "Metric": [
        "Total books",
        "Available books",
        "Issued books",
        "Total members",
        "Total transactions",
        "Returned books"
    ],
    "Value": [
        len(books),
        int(books["Available"].sum()),
        int((books["Available"] == False).sum()),
        len(members),
        len(transactions),
        int((transactions["Status"] == "Returned").sum())
    ]
})

print("LIBRARY SUMMARY")
display(summary)


# -----------------------------
# 16. Save data as CSV files
# -----------------------------
books.to_csv("books.csv", index=False)
members.to_csv("members.csv", index=False)
transactions.to_csv("transactions.csv", index=False)

print("books.csv, members.csv and transactions.csv saved successfully.")