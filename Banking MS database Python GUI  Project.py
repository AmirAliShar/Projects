import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector as sql

# Initialize main window
root = tk.Tk()
root.geometry("600x400")
root.config(bg="lightblue")

# Title Label
title_label = tk.Label(root, text="WELCOME TO BANK MANAGEMENT SYSTEM", bg="lightblue", font=("Arial", 24))
title_label.pack(pady=20)


# Database connection setup
def db_connect():
    return sql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="SemPro"
    )


# Execute SQL query and handle fetch/select operations based on query type
def db_query(query, params=None, fetch=False):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        connection.commit()
    finally:
        cursor.close()
        connection.close()


# Create normalized tables if not exists
def create_tables():
    db_query('''
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT,
            city VARCHAR(255)
        )
    ''')

    db_query('''
        CREATE TABLE IF NOT EXISTS user_credentials (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            customer_id INT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')

    db_query('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            account_number BIGINT UNIQUE,
            balance DECIMAL(10, 2) DEFAULT 0,
            timedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            remarks VARCHAR(255),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    ''')

    db_query('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT,
            transaction_type ENUM('Deposit', 'Withdraw', 'Transfer'),
            amount DECIMAL(10, 2),
            transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    ''')


# Sign Up function
def sign_up():
    def register_user():
        name = entry_name.get()
        age = entry_age.get()
        city = entry_city.get()
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password or not name or not age or not city:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        # Check if the username exists
        temp = db_query("SELECT username FROM user_credentials WHERE username = %s", (username,), fetch=True)
        if temp:
            messagebox.showerror("Error", "Username already exists!")
        else:
            # Insert customer record
            db_query('''
                INSERT INTO customers (name, age, city)
                VALUES (%s, %s, %s)
            ''', (name, age, city))

            # Get the customer ID
            customer_id = \
            db_query("SELECT id FROM customers WHERE name = %s AND age = %s AND city = %s", (name, age, city),
                     fetch=True)[0][0]

            account_number = random.randint(10000000, 99999999)
            # Insert user credentials
            db_query('''
                INSERT INTO user_credentials (username, password, customer_id)
                VALUES (%s, %s, %s)
            ''', (username, password, customer_id))

            # Insert account record
            db_query('''
                INSERT INTO accounts (customer_id, account_number, remarks)
                VALUES (%s, %s, 'Account created')
            ''', (customer_id, account_number))

            messagebox.showinfo("Success", f"Account Created! Your account number is {account_number}")
            sign_up_window.destroy()

    # Sign Up Window
    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign Up")

    tk.Label(sign_up_window, text="Name").pack()
    entry_name = tk.Entry(sign_up_window)
    entry_name.pack()

    tk.Label(sign_up_window, text="Age").pack()
    entry_age = tk.Entry(sign_up_window)
    entry_age.pack()

    tk.Label(sign_up_window, text="City").pack()
    entry_city = tk.Entry(sign_up_window)
    entry_city.pack()

    tk.Label(sign_up_window, text="Create Username").pack()
    entry_username = tk.Entry(sign_up_window)
    entry_username.pack()

    tk.Label(sign_up_window, text="Password").pack()
    entry_password = tk.Entry(sign_up_window, show="*")
    entry_password.pack()

    tk.Button(sign_up_window, text="Sign Up", command=register_user).pack()


# Sign In function
def sign_in():
    def verify_user():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        # Verify if the username exists
        temp = db_query("SELECT username FROM user_credentials WHERE username = %s", (username,), fetch=True)
        if not temp:
            messagebox.showerror("Error", "Username does not exist!")
            return

        # Verify the password
        temp_pass = db_query("SELECT password, customer_id FROM user_credentials WHERE username = %s", (username,),
                             fetch=True)
        if temp_pass[0][0] == password:
            messagebox.showinfo("Success", "Signed in successfully!")
            sign_in_window.destroy()
            show_banking_services(temp_pass[0][1])  # Pass customer_id to services
        else:
            messagebox.showerror("Error", "Incorrect password!")

    # Sign In Window
    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")

    tk.Label(sign_in_window, text="Enter Username").pack()
    entry_username = tk.Entry(sign_in_window)
    entry_username.pack()

    tk.Label(sign_in_window, text="Enter Password").pack()
    entry_password = tk.Entry(sign_in_window, show="*")
    entry_password.pack()

    tk.Button(sign_in_window, text="Sign In", command=verify_user).pack()


# Banking Services
def show_banking_services(customer_id):
    def balance_enquiry():
        result = db_query("SELECT balance FROM accounts WHERE customer_id = %s", (customer_id,), fetch=True)
        balance = result[0][0]
        messagebox.showinfo("Balance Enquiry", f"Your current balance is: {balance}")

    def cash_deposit():
        def deposit_amount():
            amount = entry_amount.get()
            if not amount.isdigit():
                messagebox.showerror("Error", "Enter a valid number")
                return
            account_id = db_query("SELECT id FROM accounts WHERE customer_id = %s", (customer_id,), fetch=True)[0][0]
            db_query("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
            db_query("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Deposit', %s)",
                     (account_id, amount))
            messagebox.showinfo("Success", "Amount Deposited Successfully")
            deposit_window.destroy()

        deposit_window = tk.Toplevel(root)
        deposit_window.title("Deposit Cash")
        tk.Label(deposit_window, text="Enter Amount").pack()
        entry_amount = tk.Entry(deposit_window)
        entry_amount.pack()
        tk.Button(deposit_window, text="Deposit", command=deposit_amount).pack()

    def cash_withdraw():
        def withdraw_amount():
            amount = entry_amount.get()
            if not amount.isdigit():
                messagebox.showerror("Error", "Enter a valid number")
                return
            account_id = db_query("SELECT id FROM accounts WHERE customer_id = %s", (customer_id,), fetch=True)[0][0]
            db_query("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
            db_query("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Withdraw', %s)",
                     (account_id, amount))
            messagebox.showinfo("Success", "Amount Withdrawn Successfully")
            withdraw_window.destroy()

        withdraw_window = tk.Toplevel(root)
        withdraw_window.title("Withdraw Cash")
        tk.Label(withdraw_window, text="Enter Amount").pack()
        entry_amount = tk.Entry(withdraw_window)
        entry_amount.pack()
        tk.Button(withdraw_window, text="Withdraw", command=withdraw_amount).pack()

    def fund_transfer():
        def transfer_amount():
            receiver_acc = entry_receiver.get()
            amount = entry_amount.get()

            if not receiver_acc.isdigit() or not amount.isdigit():
                messagebox.showerror("Error", "Enter valid numbers")
                return

            receiver_acc = int(receiver_acc)
            amount = int(amount)

            # Update balances
            account_id_sender = \
            db_query("SELECT id FROM accounts WHERE customer_id = %s", (customer_id,), fetch=True)[0][0]
            db_query("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id_sender))

            db_query("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, receiver_acc))

            # Record transaction
            db_query("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Transfer', %s)",
                     (account_id_sender, amount))

            messagebox.showinfo("Success", "Amount Transferred Successfully")
            transfer_window.destroy()

        transfer_window = tk.Toplevel(root)
        transfer_window.title("Transfer Funds")

        tk.Label(transfer_window, text="Enter Receiver's Account Number").pack()
        entry_receiver = tk.Entry(transfer_window)
        entry_receiver.pack()

        tk.Label(transfer_window, text="Enter Amount").pack()
        entry_amount = tk.Entry(transfer_window)
        entry_amount.pack()

        tk.Button(transfer_window, text="Transfer", command=transfer_amount).pack()

    def delete_account():
        if messagebox.askyesno("Delete Account", "Are you sure you want to delete your account? This action is permanent."):
            db_query("DELETE FROM accounts WHERE customer_id = %s", (customer_id,))
            db_query("DELETE FROM user_credentials WHERE customer_id = %s", (customer_id,))
            db_query("DELETE FROM customers WHERE id = %s", (customer_id,))
            messagebox.showinfo("Success", "Account Deleted Successfully")

    services_window = tk.Toplevel(root)
    services_window.title("Banking Services")
    tk.Button(services_window, text="Balance Enquiry", command=balance_enquiry).pack(pady=10)
    tk.Button(services_window, text="Cash Deposit", command=cash_deposit).pack(pady=10)
    tk.Button(services_window, text="Cash Withdraw", command=cash_withdraw).pack(pady=10)
    tk.Button(services_window, text="Fund Transfer", command=fund_transfer).pack(pady=10)
    tk.Button(services_window, text="Delete Account", command=delete_account).pack(pady=10)


# Main buttons for sign up and sign in
tk.Button(root, text="Sign Up", command=sign_up, font=("Arial", 16), bg="lightblue").pack(pady=10)
tk.Button(root, text="Sign In", command=sign_in, font=("Arial", 16), bg="lightblue").pack(pady=10)

# Initialize database
create_tables()

# Start the main event loop
root.mainloop()
