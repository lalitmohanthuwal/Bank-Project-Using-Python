# User Registration Signin Signup with Tkinter
from customer import *
from Services import Bank
import random
import tkinter as tk
from tkinter import messagebox
from DB import db_query  # Add this import

def SignUp():
    signup_window = tk.Toplevel()
    signup_window.title("Bank Account Sign Up")
    signup_window.geometry("400x400")
    
    tk.Label(signup_window, text="Create Username:").pack()
    username_entry = tk.Entry(signup_window)
    username_entry.pack()
    
    tk.Label(signup_window, text="Enter Your Password:").pack()
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.pack()
    
    tk.Label(signup_window, text="Enter Your Name:").pack()
    name_entry = tk.Entry(signup_window)
    name_entry.pack()
    
    tk.Label(signup_window, text="Enter Your Age:").pack()
    age_entry = tk.Entry(signup_window)
    age_entry.pack()
    
    tk.Label(signup_window, text="Enter Your City:").pack()
    city_entry = tk.Entry(signup_window)
    city_entry.pack()
    
    def submit_signup():
        username = username_entry.get()
        password = password_entry.get()
        name = name_entry.get()
        age = age_entry.get()
        city = city_entry.get()
        
        if not all([username, password, name, age, city]):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        temp = db_query(f"SELECT username FROM customers where username = '{username}';")
        if temp:
            messagebox.showerror("Error", "Username already exists!")
            return
            
        while True:
            account_number = random.randint(10000000, 99999999)
            temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
            if not temp:
                break
                
        try:
            cobj = Customer(username, password, name, age, city, account_number)
            cobj.createuser()
            bobj = Bank(username, account_number)
            bobj.create_transaction_table()
            messagebox.showinfo("Success", f"Account created successfully!\nYour Account Number: {account_number}")
            signup_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    tk.Button(signup_window, text="Submit", command=submit_signup).pack(pady=10)
    tk.Button(signup_window, text="Cancel", command=signup_window.destroy).pack()

def SignIn():
    username = None
    
    def on_login():
        nonlocal username
        username = username_entry.get()
        password = password_entry.get()
        
        temp = db_query(f"SELECT username FROM customers where username = '{username}';")
        if not temp:
            messagebox.showerror("Error", "Username not found!")
            return
            
        temp = db_query(f"SELECT password FROM customers where username = '{username}';")
        if temp[0][0] == password:
            messagebox.showinfo("Success", "Login successful!")
            signin_window.destroy()
        else:
            messagebox.showerror("Error", "Wrong password!")
    
    signin_window = tk.Toplevel()
    signin_window.title("Bank Account Sign In")
    signin_window.geometry("300x200")
    
    tk.Label(signin_window, text="Enter Username:").pack()
    username_entry = tk.Entry(signin_window)
    username_entry.pack()
    
    tk.Label(signin_window, text="Enter Password:").pack()
    password_entry = tk.Entry(signin_window, show="*")
    password_entry.pack()
    
    tk.Button(signin_window, text="Login", command=on_login).pack(pady=10)
    tk.Button(signin_window, text="Cancel", command=signin_window.destroy).pack()
    
    # Wait for the window to be destroyed
    signin_window.wait_window()
    
    # Return the username only if login was successful
    temp = db_query(f"SELECT username FROM customers where username = '{username}';") if username else None
    return username if temp else None