import random    
import string
import tkinter as tk
from tkinter import messagebox
import sqlite3
from turtle import window_height

def create_database():
    """
    Create the SQLite database and the passwords table if they do not exist.
    """
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_password(name, password):
    """
    Save the password to the SQLite database.
    
    Parameters:
    name (str): The name of the password.
    password (str): The generated password.
    """
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (name, password) VALUES (?, ?)', (name, password))
    conn.commit()
    conn.close()

def retrieve_passwords():
    """
    Retrieve all saved passwords from the SQLite database.
    
    Returns:
    list: A list of tuples containing the id, name, and password.
    """
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, password FROM passwords')
    passwords = cursor.fetchall()
    conn.close()
    return passwords

def update_password(password_id, new_name, new_password):
    """
    Update the name and password in the SQLite database.
    
    Parameters:
    password_id (int): The ID of the password to update.
    new_name (str): The new name of the password.
    new_password (str): The new password.
    """
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE passwords SET name = ?, password = ? WHERE id = ?', (new_name, new_password, password_id))
    conn.commit()
    conn.close()

def delete_password(password_id):
    """
    Delete the password from the SQLite database.
    
    Parameters:
    password_id (int): The ID of the password to delete.
    """
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
    conn.commit()
    conn.close()

def display_passwords():
    """
    Display the saved passwords in a new window with options to edit or delete them.
    """
    passwords = retrieve_passwords()
    display_window = tk.Toplevel(root)
    display_window.title("Saved Passwords")
    display_window.geometry("600x700")
    font_style = ("Times New Roman", 18)
        

    listbox = tk.Listbox(display_window, font=font_style, width=50, height=20)
    listbox.pack(pady=10)

    for password_id, name, password in passwords:
        listbox.insert(tk.END, f"ID: {password_id} - Name: {name} - Password: {password}")

    def on_edit():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            password_id, name, password = passwords[index]
            edit_window = tk.Toplevel(display_window)
            edit_window.title("Edit Password")
            edit_window.geometry("400x300")

            tk.Label(edit_window, text="Edit Name:", font=font_style).pack(pady=10)
            entry_name = tk.Entry(edit_window, font=font_style)
            entry_name.insert(0, name)
            entry_name.pack(pady=5)

            tk.Label(edit_window, text="Edit Password:", font=font_style).pack(pady=10)
            entry_password = tk.Entry(edit_window, font=font_style)
            entry_password.insert(0, password)
            entry_password.pack(pady=5)

            def save_changes():
                new_name = entry_name.get()
                new_password = entry_password.get()
                if new_name and new_password:
                    update_password(password_id, new_name, new_password)
                    messagebox.showinfo("Password Updated", "Password updated successfully")
                    edit_window.destroy()
                    display_window.destroy()
                    display_passwords()
                else:
                    messagebox.showerror("Invalid Input", "Name and password cannot be empty")

            tk.Button(edit_window, text="Save Changes", command=save_changes, font=font_style).pack(pady=10)

    def on_delete():
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            password_id, name, password = passwords[index]
            if messagebox.askyesno("Delete Password", f"Are you sure you want to delete the password for {name}?"):
                delete_password(password_id)
                messagebox.showinfo("Password Deleted", "Password deleted successfully")
                display_window.destroy()
                display_passwords()

    tk.Button(display_window, text="Edit Selected", command=on_edit, font=font_style).pack(pady=5)
    tk.Button(display_window, text="Delete Selected", command=on_delete, font=font_style).pack(pady=5)

def generate_password(length=10, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    """
    Generate a random password based on user preferences.
    
    Parameters:
    length (int): The length of the password to be generated. Default is 10.
    use_upper (bool): Whether to include uppercase letters. Default is True.
    use_lower (bool): Whether to include lowercase letters. Default is True.
    use_digits (bool): Whether to include digits. Default is True.
    use_special (bool): Whether to include special characters. Default is True.
    
    Returns:
    str: A randomly generated password.
    """
    characters = ''
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    if not characters:
        raise ValueError("No character types selected")
    
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def generate_password_ui():
    """
    Generate a password based on the user-specified length and preferences from the UI.
    """
    try:
        length = int(entry_length.get())
        use_upper = var_upper.get()
        use_lower = var_lower.get()
        use_digits = var_digits.get()
        use_special = var_special.get()
        
        password = generate_password(length, use_upper, use_lower, use_digits, use_special)
        messagebox.showinfo("Generated Password", f"Generated password: {password}")
        
        if messagebox.askyesno("Save Password", "Do you want to save this password?"):
            save_password_ui(password)
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def save_password_ui(password):
    """
    Prompt the user to enter a name for the password and save it to the database.
    """
    save_window = tk.Toplevel(root)
    save_window.title("Save Password")
    save_window.geometry("400x200")
    font_style = ("Times New Roman", 18)

    tk.Label(save_window, text="Enter a name for the password:", font=font_style).pack(pady=10)
    entry_name = tk.Entry(save_window, font=font_style)
    entry_name.pack(pady=5)

    def save():
        name = entry_name.get()
        if name:
            save_password(name, password)
            messagebox.showinfo("Password Saved", f"Password saved as: {name}")
            save_window.destroy()
        else:
            messagebox.showerror("Invalid Input", "Password name cannot be empty")

    tk.Button(save_window, text="Save", command=save, font=font_style).pack(pady=10)

def main():
    global root, entry_length, var_upper, var_lower, var_digits, var_special
    root = tk.Tk()
    root.title("Password Generator")

    window_width = 600
    window_height = 500
    screen_width = root.winfo_screenwidth()  
    screen_height = root.winfo_screenheight() 
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.state('zoomed')  

    font_style = ("Times New Roman", 24)

    tk.Label(root, text="Enter the desired length for the password:", font=font_style).pack(pady=10)
    entry_length = tk.Entry(root, font=font_style)
    entry_length.pack(pady=5)

    var_upper = tk.BooleanVar(value=True)
    var_lower = tk.BooleanVar(value=True)
    var_digits = tk.BooleanVar(value=True)
    var_special = tk.BooleanVar(value=True)

    tk.Checkbutton(root, text="Include Uppercase Letters", variable=var_upper, font=font_style).pack(anchor='w')
    tk.Checkbutton(root, text="Include Lowercase Letters", variable=var_lower, font=font_style).pack(anchor='w')
    tk.Checkbutton(root, text="Include Digits", variable=var_digits, font=font_style).pack(anchor='w')
    tk.Checkbutton(root, text="Include Special Characters", variable=var_special, font=font_style).pack(anchor='w')

    tk.Button(root, text="Generate Password", command=generate_password_ui, font=font_style).pack(pady=10)
    tk.Button(root, text="Show Saved Passwords", command=display_passwords, font=font_style).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_database()
    main()


if __name__ == "__main__":
    create_database()
    main()
