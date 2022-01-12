from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import os
import sys

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)
    password = "".join(password_list)

    input_password.delete(0, END)
    input_password.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = input_website.get()
    email = input_email.get()
    pasword = input_password.get()

    if website == "" or email == "" or pasword == 0:
        messagebox.showinfo(title="OOPS", message="No empty fields please!")
    else:
        is_ok = messagebox.askokcancel(
            title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {pasword} \nSave your data?")

        if is_ok:
            with open(resource_path("./data.txt"), "a") as data:
                data.write(f"{website} | {email} | {pasword}\n")

            input_website.delete(0, END)
            input_email.delete(0, END)
            input_email.insert(0, "zaharia.ioan@gmail.com")
            input_password.delete(0, END)

    update_passwords_list()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50)


# *
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


my_path = resource_path("./logo.png")
# *

canvas = Canvas()
canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file=my_path)
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

# labels
label_website = Label(text="Website:")
label_website.config(pady=15)
label_website.grid(column=0, row=1)
label_email = Label(text="Email/Username:")
label_email.grid(column=0, row=2)
label_password = Label(text="Password:")
label_password.config(pady=15)
label_password.grid(column=0, row=3)

# inputs
input_website = Entry(width=35)
input_website.grid(column=1, row=1, columnspan=2, sticky="EW")
input_website.focus()
input_email = Entry(width=35)
input_email.grid(column=1, row=2, columnspan=2, sticky="EW")
input_email.insert(0, "zaharia.ioan@gmail.com")
input_password = Entry(width=21)
input_password.grid(column=1, row=3,  sticky="EW")

# buttons
button_generate_pass = Button(
    text="Generate Password", command=generate_password)
button_generate_pass.grid(column=2, row=3, sticky="EW")
button_add = Button(text="Add", width=36, command=save_data)
button_add.grid(column=1, row=4, columnspan=2, sticky="EW")

list_label = Label(text="Click to copy password")
list_label.grid(column=1, row=5, columnspan=2, pady=10)

# passwords list


def update_passwords_list():
    global passwords
    global passwords_list
    global toggle_password_list
    passwords = []
    passwords_list = Listbox(window, width=100, height=10)
    passwords_list.grid(column=0, row=6, columnspan=3)
    # passwords_list.configure(yscrollcommand=scroolbar.set)

    with open(resource_path("./data.txt"), "r") as data:
        lines = data.readlines()
        for password in lines:
            passwords.append(password)
            passwords_list.insert(END, password)

    def copy_password(event):
        index = passwords_list.curselection()[0]
        password = passwords[index]
        pyperclip.copy(password.rsplit(' ', 1)[1])

    passwords_list.bind("<<ListboxSelect>>", copy_password)


scroolbar = Scrollbar(window)
scroolbar.grid(column=3, row=6, rowspan=3)
# scroolbar.configure(command=passwords_list.yview)


update_passwords_list()


window.mainloop()
