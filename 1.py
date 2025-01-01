import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Global variable to hold the uploaded dataset
data = None


# Function to upload dataset
def upload_data():
    global data
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            if file_path.endswith(".csv"):
                data = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                data = pd.read_excel(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format!")
                return
            display_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")


# Function to display the uploaded dataset in the dashboard
def display_data(data):
    if data is not None:
        # Clear previous table
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Create a treeview to display data
        tree = ttk.Treeview(table_frame, columns=list(data.columns), show="headings", height=10)
        tree.pack(fill=tk.BOTH, expand=True)

        # Define column headings
        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        # Insert data rows
        for _, row in data.iterrows():
            tree.insert("", tk.END, values=row.tolist())
    else:
        messagebox.showinfo("Info", "No data to display!")

# Monthly Sales Analysis with chart
def monthly_sales_analysis():
    if data is not None:
        try:
            monthly_sales = data.groupby("Month")["Sales"].sum()
            monthly_sales.plot(kind='bar', title="Monthly Sales Analysis", color="skyblue")
            plt.xlabel("Month")
            plt.ylabel("Total Sales")
            plt.tight_layout()
            plt.show()
        except KeyError:
            messagebox.showerror("Error", "Data must have 'Month' and 'Sales' columns.")
    else:
        messagebox.showinfo("Info", "Please upload a dataset first!")


# Price Analysis with chart
def price_analysis():
    if data is not None:
        try:
            avg_price = data.groupby("Product")["Price"].mean()
            avg_price.plot(kind='bar', title="Price Analysis", color="lightgreen")
            plt.xlabel("Product")
            plt.ylabel("Average Price")
            plt.tight_layout()
            plt.show()
        except KeyError:
            messagebox.showerror("Error", "Data must have 'Product' and 'Price' columns.")
    else:
        messagebox.showinfo("Info", "Please upload a dataset first!")


# Weekly Sales Analysis with chart
def weekly_sales_analysis():
    if data is not None:
        try:
            weekly_sales = data.groupby("Week")["Sales"].sum()
            weekly_sales.plot(kind='line', title="Weekly Sales Analysis", color="orange", marker="o")
            plt.xlabel("Week")
            plt.ylabel("Total Sales")
            plt.grid()
            plt.tight_layout()
            plt.show()
        except KeyError:
            messagebox.showerror("Error", "Data must have 'Week' and 'Sales' columns.")
    else:
        messagebox.showinfo("Info", "Please upload a dataset first!")


# Product Preference Analysis with chart
def product_preference_analysis():
    if data is not None:
        try:
            product_preference = data["Product"].value_counts()
            product_preference.plot(kind='pie', title="Product Preference Analysis", autopct='%1.1f%%', startangle=140)
            plt.ylabel("")
            plt.tight_layout()
            plt.show()
        except KeyError:
            messagebox.showerror("Error", "Data must have a 'Product' column.")
    else:
        messagebox.showinfo("Info", "Please upload a dataset first!")


# Distribution of Total Sales with chart
def distribution_of_sales():
    if data is not None:
        try:
            data["Sales"].plot(kind='hist', bins=10, title="Distribution of Total Sales", color="purple", alpha=0.7)
            plt.xlabel("Sales")
            plt.ylabel("Frequency")
            plt.tight_layout()
            plt.show()
        except KeyError:
            messagebox.showerror("Error", "Data must have a 'Sales' column.")
    else:
        messagebox.showinfo("Info", "Please upload a dataset first!")


# Login Form
def login():
    login_window = tk.Tk()
    login_window.title("Sampath Food City Login")
    login_window.geometry("400x250")
    login_window.configure(bg="#d8f3dc")

    # Create labels and entry fields
    tk.Label(login_window, text="Username", bg="#d8f3dc", font=("Arial", 12)).pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password", bg="#d8f3dc", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    # Check credentials
    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "password":
            login_window.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    # Login button
    tk.Button(login_window, text="Login", command=check_login, bg="#40916c", fg="white", font=("Arial", 12), width=10).pack(pady=20)

    login_window.mainloop()


# Open dashboard after successful login
def open_dashboard():
    global root, table_frame

    # Main window for the dashboard
    root = tk.Tk()
    root.title("Sampath Food City Sales Data Dashboard")
    root.geometry("800x600")
    root.configure(bg="#d8f3dc")

    # Frame for buttons
    button_frame = tk.Frame(root, bg="#d8f3dc")
    button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Buttons
    buttons = [
        ("Upload Dataset", upload_data),
        ("Monthly Sales Analysis", monthly_sales_analysis),
        ("Price Analysis", price_analysis),
        ("Weekly Sales Analysis", weekly_sales_analysis),
        ("Product Preference Analysis", product_preference_analysis),
        ("Distribution of Total Sales", distribution_of_sales),
    ]

    for text, command in buttons:
        btn = tk.Button(button_frame, text=text, command=command, bg="#40916c", fg="white", width=25, font=("Arial",12), relief="flat")
        btn.pack(anchor="w", pady=10)

    # Frame for displaying data
    table_frame = tk.Frame(root, bg="white")
    table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Run the dashboard
    root.mainloop()


# Call the login function when the program starts
login()
