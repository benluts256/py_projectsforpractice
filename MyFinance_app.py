import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import hashlib
# ======================================================
# SECTION 1: DATABASE LOGIC
# ======================================================



def init_db():
    """Initializes the database and creates the tables if they don't exist."""
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    # Existing transactions table
    cur.execute("""CREATE TABLE IF NOT EXISTS transactions 
                   (id INTEGER PRIMARY KEY, type TEXT, category TEXT, amount REAL)""")
    # Users table
    cur.execute("""CREATE TABLE IF NOT EXISTS users 
                   (username TEXT PRIMARY KEY, password TEXT)""")
    conn.commit()
    conn.close()

def hash_password(password):
    """Turns a password into a secure gibberish string."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        conn = sqlite3.connect("finance.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # User already exists
    finally:
        conn.close()

def check_login(username, password):
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    user = cur.fetchone()
    conn.close()
    return user is not None

def add_transaction(trans_type, category, amount):
    """Adds a new transaction to the database."""
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (type, category, amount) VALUES (?, ?, ?)", 
                (trans_type, category, amount))
    conn.commit()
    conn.close()

def delete_transaction(trans_id):
    """Deletes a transaction by ID."""
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
    conn.commit()
    conn.close()

def get_summary():
    """Fetches expenses grouped by category for the pie chart."""
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = cur.fetchall()
    conn.close()
    return data

def get_recent_transactions():
    """Fetches the 15 most recent transactions for the table."""
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("SELECT id, type, category, amount FROM transactions ORDER BY id DESC LIMIT 15")
    data = cur.fetchall()
    conn.close()
    return data


# ======================================================
# SECTION 2: GUI APPLICATION
# ======================================================

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Login")
        self.root.geometry("300x250")

        tk.Label(root, text="Login or Register", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(root, text="Username").pack()
        self.user_entry = tk.Entry(root)
        self.user_entry.pack(pady=5)

        tk.Label(root, text="Password").pack()
        self.pass_entry = tk.Entry(root, show="*") # Hides password typing
        self.pass_entry.pack(pady=5)

        self.btn_login = tk.Button(root, text="Login", command=self.login, width=15)
        self.btn_login.pack(pady=5)

        self.btn_reg = tk.Button(root, text="Register", command=self.register, width=15)
        self.btn_reg.pack(pady=5)

    def login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if check_login(u, p):
            self.root.destroy() # Close the login window
            # The Main execution block will now continue to FinanceApp
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if u and p:
            if register_user(u, p):
                messagebox.showinfo("Success", "Account created! You can now login.")
            else:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showwarning("Warning", "Fields cannot be empty.")




class FinanceApp:
    
    
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Dashboard")
        icon_data = """a1LAwjzIRRqBVKzdQScBZomDRgvW1gi0mPkb0B5uLeO+/wN3/+q8Xt++bCtR+/bHjtrXf6W2+8xd9aej9bXYVJgZVtT8yx8kBVfbVfhZUedSIiIic4BVgiIiLr39LqLBiHWVWgha2auXJS7OC+e3e587t3c8c3bxh8AaIH1z7ndHfmVNue/oKn5+edf5a96Pyzsgc/9XH5uVNtc362w26yW0yqsOlG7EwgC4boYThMwZZSho3DmBRU5U2THkXbDJzk0vuDCDsDg/lwxy3f8t/+/BXl7XPz4YbPXl7ccNNt5Z07d8e75hbK+8fXRCMNXXebSWFrYP8KKwVWIiIisiIFWCIiIhvLZGUWjAOtybbDOtCypJZDCziI3H53eRdw23XfGXwxtXbZfMfW7LRWk1MuuTg//fEXuYe2mvb8Sx+Xn3XB2eZcN4hnbtthtzdPMemowgPzVRtigDiIDKuqLVVurT3WpEdB3qzuPwO0SLOqPNCLLNwXh71evGv2Pv/dL141vPOe+8rb7tsdb/rEl4rb9+zz9923K94Top8hzaqyQJaqqtwWRo8EAtBn/7CqblTVo0NEREQOSAGWiIjIxhaXvIXFodZEpZapWg/Jq89PQTS795X7gF133Vdc84FPxY8AAVxr85Q9ybm47ZEPdqc84RHunE6bc8861Zz5tMe6MzdPmTOaOaefcprd0jzFmFE40o1palcdXwygGEZCVMh1tBmTAirnwLWqdr96CYD2ROA4jHTviYOZ+bizP+Sum24Pd3z5an/3YMh3774/3Pq5K/w9c924a6G/sKcowp6q0C+vHisuve+2MV4RMDCurFq6QuByj0cRERGRg1KAJSIicuKZDBEm2w6XVmvZFIOYOuhqkupzHMQ4uxBmgD2XXVXedNlVxeeoQgpj7OZmg22ZM5uffLE9+SFn2bPaTU6b7pjTLn2UO/nMU8xp7aY5pdHglDNOMZvzk22bLF1rak8jrVQ32Uw2YDxzqWQUeJ1I6nvCGCAzWGfIrIGsutvqcKo5EU6VQC/6++8OC/PdeH9/YHbOd+POr1/v7/v2nWFnf8i9M/Pxri9dFe6+d3fYW3pmhkXcWw1WN0AOpo6+HNhtYOvHTR1YDRg/lpZrAzzB7ikRERE5FhRgiYiIyEpVWpNtiEtma5nJ6q18PDAeE2MM/QG7Ie761OXh5k9dHovxdZkczLQ1TDlH56IH220PP8+e1mmZkxs52zsts/2Si+y2M081J3daZnszZ0eemW2n7TCdTdvpMGWbuIh1Jv02qGp94sqRSUEaRl83s8WYbkGAYCGa9P2jH4n7X8WhMEveMZPvx1QJZbLqik21/RkpcLJLrmh0qcKojHHzXRmhNJ599O74bugt9JkpCvb0BuyZnY+7vnFj2HXbPWFfUbCnP4y7d+3j3suv8bv2zcdZ7+kB8xAXqltYt/zVNXIWTKe6fyfb/SYDq6Vh1UqPIREREZGjRgGWiIiILCeu8H49s2hptVb9flW1Nfp81WI2aleMEH2IzISSfd+40d/5jRvLqxg3FlK1prXTKnW0gOb5Z9qph5wz2Do9Zbe0GmzJc7M5z9i0Y6vddPEF2abtm81Up22mWw2zKcuZyh3TzjHlrGlv22Kyk7bZhmubBk1ynG3QMJkpI42GXTzuHlLfHRO3KC65xcvtlUWfj/vXIQVgkwVnA8NYUMYhw1gszMThPfeHYlgy8D52vWehKJkfDuN8b8D83EJYuO2uMHf9d8r50jNblswOhnG2148z9+8JM9fc5GcXerFPmi/Vh9iDOJjYmmpwv6nmU0VSWGW2plhtURi1NKRarpJKQZWIiIisCgVYIiIicjgOFGDUcY9ZcmHxx2bJ102D1J44+f2RVFs1hMgtd/r7brmz9Gm1RKrL6FfZKiTLSPO76vczINu2xeZnnuram6ZMs92k1chNK89N05qYRx9ya8msITeGrH6/2uLMGlzdqjgxyavewjKOWzBjjJRADBEfI0WMlDFShkARAkV0g9IHMxwWsT8Yxn63F/t7ZuLgljt8v2rZq5v+ivHbWL+d3McuXUx9YbxdplUFf8tVSpUToRXsH1AtHaiukEpERETWDAVYIiIicrQsV6lTM8u8v1IV15L368CrHhq+qJ1xya+eDL5SwrV3JoS9M77apli3xVVhjVmp2uhILXM74uRsMTvx/kr7pgG2scz+DRPvT1ZMLf2e5T6evH8m68tERERE1jQFWCIiInI8rNSSOGmyggv2b9ozK3zNTIRAy4VBVIERjIaR73e9rPC5Qwl5JqvGVmwsXOF9v8LXDvft4eznQ/26iIiIyJqhAEtERETWigc6EHyF0GrF71np43iQ6zjc27Jc+HWwjw+0P0REREROWAqwREREZL07nKqjQ3EkrXWT1VgiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiI/8/fwh5OTOdbtsAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMTEtMDZUMDk6MjA6MjkrMDA6MDDlzEWPAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTExLTAxVDEzOjE0OjM2KzAwOjAwZNM0GgAAAABJRU5ErkJggg== """
        try:
            img_obj = tk.PhotoImage(data=icon_data.strip())
            self.root.iconphoto(False, img_obj)
        except Exception as e:
            print(f"Icon Error: {e}")
            
        self.root.geometry("900x650")

        
        # Top Frame: Contains Inputs (Left) and Chart (Right)
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame_left = tk.Frame(self.frame_top, padx=20, pady=20)
        self.frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_right = tk.Frame(self.frame_top, padx=20, pady=20)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Bottom Frame: Contains the Table
        self.frame_bottom = tk.Frame(root, padx=20, pady=20)
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # --- WIDGETS: Input Section (Left) ---
        tk.Label(self.frame_left, text="Add New Transaction", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        tk.Label(self.frame_left, text="Type:").pack(anchor="w")
        self.type_var = tk.StringVar(value="Expense")
        self.type_menu = ttk.Combobox(self.frame_left, textvariable=self.type_var, values=["Income", "Expense"], state="readonly")
        self.type_menu.pack(fill=tk.X, pady=5)

        tk.Label(self.frame_left, text="Category (e.g., Food, Rent):").pack(anchor="w")
        self.cat_entry = tk.Entry(self.frame_left)
        self.cat_entry.pack(fill=tk.X, pady=5)

        tk.Label(self.frame_left, text="Amount (Shs.):").pack(anchor="w")
        self.amount_entry = tk.Entry(self.frame_left)
        self.amount_entry.pack(fill=tk.X, pady=5)

        self.btn_add = tk.Button(self.frame_left, text="Add Transaction", command=self.add_entry, bg="blue", fg="white", font=("Arial", 10, "bold"))
        self.btn_add.pack(pady=20, fill=tk.X)

        # --- WIDGETS: Chart Section (Right) ---
        # Create the figure once
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- WIDGETS: History Table (Bottom) ---
        tk.Label(self.frame_bottom, text="Recent History", font=("Arial", 12, "bold")).pack(anchor="w")

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.frame_bottom)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview
        self.tree = ttk.Treeview(self.frame_bottom, columns=("ID", "Type", "Category", "Amount"), 
                                 show="headings", height=8, yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.config(command=self.tree.yview)

        # Define Columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Category", width=200, anchor="w")
        self.tree.column("Amount", width=100, anchor="e")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Delete Button
        self.btn_delete = tk.Button(self.frame_bottom, text="Delete Selected", command=self.delete_entry, bg="red", fg="white")
        self.btn_delete.pack(pady=5, anchor="e")

        # --- INITIAL LOAD ---
        self.update_chart()
        self.update_table()

    # --- LOGIC FUNCTIONS ---

    def add_entry(self):
        try:
            t_type = self.type_var.get()
            cat = self.cat_entry.get()
            amt_str = self.amount_entry.get()

            if not cat or not amt_str:
                raise ValueError("All fields are required.")
            
            amt = float(amt_str)

            # Add to DB
            add_transaction(t_type, cat, amt)
            
            # Clear Inputs
            self.cat_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            
            # Refresh UI
            messagebox.showinfo("Success", "Transaction Added!")
            self.update_chart()
            self.update_table()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid Input: {e}")

    def delete_entry(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return

        # Confirm Deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")
        if confirm:
            for item in selected_item:
                # Get the ID from the selected row values
                record_id = self.tree.item(item, "values")[0]
                delete_transaction(record_id)
            
            self.update_chart()
            self.update_table()

    def update_chart(self):
        self.ax.clear()
        
        data = get_summary() # Returns list like [('Food', 100.0), ('Rent', 500.0)]
        
        if data:
            categories = [item[0] for item in data]
            amounts = [item[1] for item in data]
            
            self.ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
            self.ax.set_title("Expenses Breakdown")
        else:
            self.ax.text(0.5, 0.5, "No Expenses Yet", ha='center')

        self.canvas.draw()

    def update_table(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insert new data
        rows = get_recent_transactions()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

# ======================================================
# SECTION 3: MAIN EXECUTION
# ======================================================


if __name__ == "__main__":
    init_db()
    
    # 1. Start with the Login Screen
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
    main_root = tk.Tk()
    app = FinanceApp(main_root)
    main_root.mainloop()