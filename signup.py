import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import re
import os
import threading

# Create or connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table for users if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')

bg_image_path = "back1.jpg"

# Function to create a new user
def signup(signup_window, username_entry, password_entry, confirm_password_entry, signup_error_label):
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Password security checks
    if len(password) < 8:
        signup_error_label.config(text="Password must be at least 8 characters long", foreground="red")
        return
    if not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
        signup_error_label.config(text="Password must contain at least one lowercase letter, one uppercase letter, and one digit", foreground="red")
        return
    if password != confirm_password:
        signup_error_label.config(text="Passwords do not match", foreground="red")
        return

    # Check if username already exists
    c.execute('''SELECT * FROM users WHERE username=?''', (username,))
    if c.fetchone():
        signup_error_label.config(text="Username already exists", foreground="red")
        return

    # If all checks pass, insert the new user into the database
    c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    conn.commit()  # Commit changes to the database
    signup_error_label.config(text="Signup successful!", foreground="green")
    # Destroy signup window after successful signup
    signup_window.destroy()
    # Display login window
    show_login_window()

# Function to display the signup window
def show_signup_window():
    signup_window = tk.Toplevel(root)
    signup_window.title("Signup")
    signup_window.state('zoomed')

    signup_frame = ttk.Frame(signup_window)
    signup_frame.pack(expand=True, fill="both")

    # Load and resize background image for signup window
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((signup_window.winfo_screenwidth(), signup_window.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = ttk.Label(signup_frame, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

    ttk.Label(signup_frame, text="Username:", font=("Arial", 18), foreground="white", background="#333333").place(relx=0.4, rely=0.3, anchor="center")
    username_entry = ttk.Entry(signup_frame, font=("Arial", 16))
    username_entry.place(relx=0.6, rely=0.3, anchor="center", width=300)

    ttk.Label(signup_frame, text="Password:", font=("Arial", 18), foreground="white", background="#333333").place(relx=0.4, rely=0.4, anchor="center")
    password_entry = ttk.Entry(signup_frame, show="*", font=("Arial", 16))
    password_entry.place(relx=0.6, rely=0.4, anchor="center", width=300)

    ttk.Label(signup_frame, text="Confirm Password:", font=("Arial", 18), foreground="white", background="#333333").place(relx=0.4, rely=0.5, anchor="center")
    confirm_password_entry = ttk.Entry(signup_frame, show="*", font=("Arial", 16))
    confirm_password_entry.place(relx=0.6, rely=0.5, anchor="center", width=300)

    signup_error_label = ttk.Label(signup_frame, text="", font=("Arial", 14), foreground="green")
    signup_error_label.place(relx=0.5, rely=0.56, anchor="center")

    signup_button = ttk.Button(signup_frame, text="Signup", command=lambda: signup(signup_window, username_entry, password_entry, confirm_password_entry, signup_error_label), style="Colored.TButton")
    signup_button.place(relx=0.5, rely=0.63, anchor="center", width=200, height=50)

    back_button = ttk.Button(signup_frame, text="Back", command=signup_window.destroy, style="Colored.TButton")
    back_button.place(relx=0.03, rely=0.03, anchor="center", width=200, height=50)

# Function to display the login window
def show_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.state('zoomed')

    login_frame = ttk.Frame(login_window)
    login_frame.pack(expand=True, fill="both")

    # Load and resize background image for login window
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((login_window.winfo_screenwidth(), login_window.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = ttk.Label(login_frame, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo
    ttk.Label(login_frame, text="Username:", font=("Arial", 18), foreground="white", background="#333333").place(relx=0.4, rely=0.3, anchor="center")
    username_entry = ttk.Entry(login_frame, font=("Arial", 16))
    username_entry.place(relx=0.6, rely=0.3, anchor="center", width=300)

    ttk.Label(login_frame, text="Password:", font=("Arial", 18), foreground="white", background="#333333").place(relx=0.4, rely=0.4, anchor="center")
    password_entry = ttk.Entry(login_frame, show="*", font=("Arial", 16))
    password_entry.place(relx=0.6, rely=0.4, anchor="center", width=300)

    login_error_label = ttk.Label(login_frame, text="", font=("Arial", 14), foreground="red")
    login_error_label.place(relx=0.5, rely=0.48, anchor="center")

    login_button = ttk.Button(login_frame, text="Login", command=lambda: authenticate(login_window, username_entry.get(), password_entry.get(), login_error_label), style="Colored.TButton")
    login_button.place(relx=0.5, rely=0.56, anchor="center", width=200, height=50)

    back_button = ttk.Button(login_frame,text="Back", command=login_window.destroy, style="Colored.TButton")
    back_button.place(relx=0.03, rely=0.03, anchor="center", width=200, height=50)

# Function to verify login credentials
def authenticate(login_window, username, password, login_error_label):
    if not username or not password:
        login_error_label.config(text="Username and password are required")
    else:
        c.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))

        if c.fetchone():
            login_error_label.config(text="Login successful!", foreground="green")
            login_window.destroy()
            # Start a new thread to open exp.py and show loading window
            loading_window = show_loading_window()
            threading.Thread(target=open_exp, args=(loading_window,)).start()
        else:
            login_error_label.config(text="Invalid username or password")

# Function to open exp.py
def open_exp(loading_window):
    os.system("t.py")
    loading_window.destroy()

# Function to display the loading window
def show_loading_window():
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading")
    loading_window.state('zoomed')

    loading_frame = ttk.Frame(loading_window)
    loading_frame.pack(expand=True, fill="both")

    ttk.Label(loading_frame, text="Loading, please wait...", font=("Arial", 18), foreground="white", background="#333333").place(relx=0.5, rely=0.5, anchor="center")

    return loading_window

# GUI setup
root = tk.Tk()
root.title("Welcome")
root.state('zoomed')

# Load and resize background image for main window
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = ttk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo

# Customizing the style for buttons
style = ttk.Style()
style.configure("Colored.TButton", font=("Arial", 14,"bold"),
                foreground="black",
                background="#FF6F61",
                borderwidth=[0],
                relief=tk.FLAT,
                padding=10)

# Functionality for signup and login buttons will remain the same
signup_button = ttk.Button(root, text="Sign Up", command=show_signup_window, style="Colored.TButton")
signup_button.place(relx=0.67, rely=0.5, anchor=tk.CENTER, width=220, height=60)

login_button = ttk.Button(root, text="Login", command=show_login_window, style="Colored.TButton")
login_button.place(relx=0.3, rely=0.5, anchor=tk.CENTER, width=220, height=60)

root.mainloop()

conn.close()

