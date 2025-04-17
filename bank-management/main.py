from login import *
from Services import *
import tkinter as tk
from tkinter import messagebox

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("500x400")
        
        self.user = None
        self.account_number = None
        self.bobj = None
        
        self.create_welcome_screen()
        
    def create_welcome_screen(self):
        self.clear_window()
        
        tk.Label(self.root, text="Welcome to Our Bank", font=("Arial", 20)).pack(pady=20)
        
        tk.Button(self.root, text="Sign Up", command=self.handle_signup, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Sign In", command=self.handle_signin, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20, height=2).pack(pady=10)
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def handle_signup(self):
        SignUp()
        
    def handle_signin(self):
        self.user = SignIn()
        if self.user:
               temp = db_query(f"SELECT account_number FROM customers WHERE username = '{self.user}';")
        if temp:
         self.account_number = temp[0][0]
        self.bobj = Bank(self.user, self.account_number)
        self.create_banking_screen()
                
    def create_banking_screen(self):
        self.clear_window()
        
        tk.Label(self.root, text=f"Welcome {self.user.capitalize()}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Account Number: {self.account_number}", font=("Arial", 12)).pack(pady=5)
        
        tk.Button(self.root, text="Balance Enquiry", command=self.balance_enquiry, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Cash Deposit", command=self.deposit_screen, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Cash Withdraw", command=self.withdraw_screen, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Fund Transfer", command=self.transfer_screen, width=20, height=2).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.logout, width=20, height=2).pack(pady=5)
        
    def balance_enquiry(self):
        temp = db_query(f"SELECT balance FROM customers WHERE username = '{self.user}';")
        messagebox.showinfo("Balance", f"Your current balance is: {temp[0][0]}")
        
    def deposit_screen(self):
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Deposit Money")
        
        tk.Label(deposit_window, text="Enter Amount to Deposit:").pack(pady=10)
        amount_entry = tk.Entry(deposit_window)
        amount_entry.pack(pady=5)
        
        def submit_deposit():
            try:
                amount = int(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                    
                self.bobj.deposit(amount)
                mydb.commit()
                messagebox.showinfo("Success", f"Amount {amount} deposited successfully!")
                deposit_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
                
        tk.Button(deposit_window, text="Deposit", command=submit_deposit).pack(pady=10)
        tk.Button(deposit_window, text="Cancel", command=deposit_window.destroy).pack()
        
    def withdraw_screen(self):
        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title("Withdraw Money")
        
        tk.Label(withdraw_window, text="Enter Amount to Withdraw:").pack(pady=10)
        amount_entry = tk.Entry(withdraw_window)
        amount_entry.pack(pady=5)
        
        def submit_withdraw():
            try:
                amount = int(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                    
                self.bobj.withdraw(amount)
                mydb.commit()
                messagebox.showinfo("Success", f"Amount {amount} withdrawn successfully!")
                withdraw_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
                
        tk.Button(withdraw_window, text="Withdraw", command=submit_withdraw).pack(pady=10)
        tk.Button(withdraw_window, text="Cancel", command=withdraw_window.destroy).pack()
        
    def transfer_screen(self):
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Fund Transfer")
        
        tk.Label(transfer_window, text="Receiver Account Number:").pack(pady=5)
        receive_entry = tk.Entry(transfer_window)
        receive_entry.pack(pady=5)
        
        tk.Label(transfer_window, text="Amount to Transfer:").pack(pady=5)
        amount_entry = tk.Entry(transfer_window)
        amount_entry.pack(pady=5)
        
        def submit_transfer():
            try:
                receive = int(receive_entry.get())
                amount = int(amount_entry.get())
                
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                    
                self.bobj.fundtransfer(receive, amount)
                mydb.commit()
                messagebox.showinfo("Success", f"Amount {amount} transferred successfully!")
                transfer_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                
        tk.Button(transfer_window, text="Transfer", command=submit_transfer).pack(pady=10)
        tk.Button(transfer_window, text="Cancel", command=transfer_window.destroy).pack()
        
    def logout(self):
        self.user = None
        self.account_number = None
        self.bobj = None
        self.create_welcome_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()