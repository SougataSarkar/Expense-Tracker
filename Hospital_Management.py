from tkinter import *
from tkinter import ttk, messagebox

def show_main_window(role):
    global root, entry_name, entry_age, gender_var, gender_menu, entry_disease, entry_doctor, table, entry_search, visible_fields
    root = Tk()
    root.title("Hospital Management System")
    root.geometry("1000x600")
    root.configure(bg="#e9ecef")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#ffffff")
    style.configure("TLabel", background="#ffffff", font=("Segoe UI", 11))
    style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

    # Default fields
    all_fields = ["Name", "Age", "Gender", "Disease", "Doctor"]
    visible_fields = all_fields.copy()

    def refresh_table_columns():
        table['columns'] = visible_fields
        for col in all_fields:
            if col in visible_fields:
                table.heading(col, text=col)
                table.column(col, width=120, anchor="center")
            else:
                table.heading(col, text="")
                table.column(col, width=0)

    def customize_fields():
        custom_win = Tk()
        custom_win.title("Customize Fields")
        custom_win.geometry("300x300")
        vars = {}
        for i, field in enumerate(all_fields):
            vars[field] = BooleanVar(value=field in visible_fields)
            ttk.Checkbutton(custom_win, text=field, variable=vars[field]).pack(anchor="w", padx=20, pady=5)
        def apply():
            visible_fields.clear()
            for field in all_fields:
                if vars[field].get():
                    visible_fields.append(field)
            refresh_table_columns()
            custom_win.destroy()
        ttk.Button(custom_win, text="Apply", command=apply).pack(pady=20)
        custom_win.mainloop()

    # ------------------ TITLE ------------------ #
    header = ttk.Frame(root)
    header.pack(fill=X)
    title = ttk.Label(header, text="Hospital Management System", font=("Segoe UI", 26, "bold"), background="#2c7be5", foreground="white", anchor="center")
    title.pack(fill=X, padx=0, pady=0)
    title.configure(style="TLabel")
    header.configure(style="TFrame")
    title.configure(background="#2c7be5", foreground="white")

    # ------------------ INPUT FRAME ------------------ #
    frame = ttk.Frame(root, style="TFrame")
    frame.place(x=20, y=80, width=320, height=480)

    ttk.Label(frame, text="Patient Name:").place(x=20, y=30)
    entry_name = ttk.Entry(frame, width=25)
    entry_name.place(x=140, y=30)

    ttk.Label(frame, text="Age:").place(x=20, y=80)
    entry_age = ttk.Entry(frame, width=25)
    entry_age.place(x=140, y=80)

    ttk.Label(frame, text="Gender:").place(x=20, y=130)
    gender_var = StringVar(value="Male")
    gender_menu = ttk.Combobox(frame, textvariable=gender_var, values=["Male", "Female", "Other"], width=22, state="readonly")
    gender_menu.place(x=140, y=130)

    ttk.Label(frame, text="Disease:").place(x=20, y=180)
    entry_disease = ttk.Entry(frame, width=25)
    entry_disease.place(x=140, y=180)

    ttk.Label(frame, text="Doctor:").place(x=20, y=230)
    entry_doctor = ttk.Entry(frame, width=25)
    entry_doctor.place(x=140, y=230)

    # Buttons
    ttk.Button(frame, text="Add Patient", command=add_patient).place(x=80, y=300)
    ttk.Button(frame, text="Delete Patient", command=delete_patient).place(x=80, y=350)
    ttk.Button(frame, text="Clear", command=clear_fields).place(x=80, y=400)
    ttk.Button(frame, text="Edit Patient", command=lambda: edit_patient()).place(x=80, y=450)

    # Customize Fields Button
    ttk.Button(root, text="Customize Fields", command=customize_fields).place(x=20, y=570)

    # ------------------ SEARCH ------------------ #
    search_frame = ttk.Frame(root, style="TFrame")
    search_frame.place(x=350, y=80, width=620, height=40)
    ttk.Label(search_frame, text="Search Patient:").place(x=10, y=5)
    entry_search = ttk.Entry(search_frame, width=30)
    entry_search.place(x=130, y=5)
    ttk.Button(search_frame, text="Search", command=search_patient).place(x=350, y=2)

    # ------------------ TABLE ------------------ #
    table_frame = ttk.Frame(root, style="TFrame")
    table_frame.place(x=350, y=130, width=620, height=430)
    scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
    table = ttk.Treeview(table_frame,
                         columns=visible_fields,
                         yscrollcommand=scroll_y.set, show="headings")
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_y.config(command=table.yview)
    for col in visible_fields:
        table.heading(col, text=col)
        table.column(col, width=120, anchor="center")
    table.pack(fill=BOTH, expand=1, padx=10, pady=10)

    # Add logout button
    logout_btn = ttk.Button(root, text="Logout", command=lambda: logout())
    logout_btn.place(x=900, y=20)

    root.mainloop()

def logout():
    root.destroy()
    show_login_window()

user_db = {
    "Admin": {"admin1": {"username": "admin", "password": "admin"}},
    "Staff": {"staff1": {"username": "staff", "password": "staff"}},
    "Patient": {"patient1": {"username": "patient", "password": "patient"}}
}

def show_registration_window():
    reg_win = Tk()
    reg_win.title("Register - Hospital Management System")
    reg_win.geometry("400x400")
    reg_win.configure(bg="#e9ecef")
    ttk.Label(reg_win, text="Register", font=("Segoe UI", 20, "bold")).pack(pady=20)
    ttk.Label(reg_win, text="Role:").pack(pady=5)
    reg_role_var = StringVar(value="Patient")
    reg_role_menu = ttk.Combobox(reg_win, textvariable=reg_role_var, values=["Patient", "Staff", "Admin"], state="readonly", width=27)
    reg_role_menu.pack(pady=5)
    ttk.Label(reg_win, text="User ID:").pack(pady=5)
    reg_id_entry = ttk.Entry(reg_win, width=30)
    reg_id_entry.pack(pady=5)
    ttk.Label(reg_win, text="Username:").pack(pady=5)
    reg_username_entry = ttk.Entry(reg_win, width=30)
    reg_username_entry.pack(pady=5)
    ttk.Label(reg_win, text="Password:").pack(pady=5)
    reg_password_entry = ttk.Entry(reg_win, width=30, show="*")
    reg_password_entry.pack(pady=5)

    def register():
        role = reg_role_var.get()
        user_id = reg_id_entry.get()
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        if not user_id or not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return
        if user_id in user_db[role]:
            messagebox.showerror("Error", "User ID already exists.")
            return
        user_db[role][user_id] = {"username": username, "password": password}
        messagebox.showinfo("Success", f"{role} registered successfully!")
        reg_win.destroy()

    ttk.Button(reg_win, text="Register", command=register).pack(pady=20)
    reg_win.mainloop()

def show_login_window():
    login_win = Tk()
    login_win.title("Login - Hospital Management System")
    login_win.geometry("400x400")
    login_win.configure(bg="#e9ecef")
    ttk.Label(login_win, text="Login", font=("Segoe UI", 20, "bold")).pack(pady=20)
    ttk.Label(login_win, text="Role:").pack(pady=5)
    role_var = StringVar(value="Patient")
    role_menu = ttk.Combobox(login_win, textvariable=role_var, values=["Patient", "Staff", "Admin"], state="readonly", width=27)
    role_menu.pack(pady=5)
    ttk.Label(login_win, text="User ID:").pack(pady=5)
    id_entry = ttk.Entry(login_win, width=30)
    id_entry.pack(pady=5)
    ttk.Label(login_win, text="Username:").pack(pady=5)
    username_entry = ttk.Entry(login_win, width=30)
    username_entry.pack(pady=5)
    ttk.Label(login_win, text="Password:").pack(pady=5)
    password_entry = ttk.Entry(login_win, width=30, show="*")
    password_entry.pack(pady=5)

    def authenticate():
        role = role_var.get()
        user_id = id_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        # Try login by user ID
        if user_id in user_db[role]:
            user = user_db[role][user_id]
            if user["password"] == password:
                login_win.destroy()
                show_main_window(role)
                return
        # Try login by username
        for uid, user in user_db[role].items():
            if user["username"] == username and user["password"] == password:
                login_win.destroy()
                show_main_window(role)
                return
        messagebox.showerror("Login Failed", "Invalid credentials or role.")

    ttk.Button(login_win, text="Login", command=authenticate).pack(pady=20)
    ttk.Button(login_win, text="Register", command=lambda: [login_win.destroy(), show_registration_window()]).pack(pady=5)
    login_win.mainloop()

show_login_window()

# ------------------ DATA STORAGE ------------------ #

patients = []

# ------------------ FUNCTIONS ------------------ #

def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    disease = entry_disease.get()
    doctor = entry_doctor.get()

    if name == "" or age == "":
        messagebox.showerror("Error", "Name and Age are required")
        return

    data = (name, age, gender, disease, doctor)
    patients.append(data)

    table.insert("", END, values=data)

    clear_fields()


def clear_fields():
    entry_name.delete(0, END)
    entry_age.delete(0, END)
    entry_disease.delete(0, END)
    entry_doctor.delete(0, END)
    gender_var.set("Male")


def delete_patient():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a record to delete")
        return

    for item in selected:
        table.delete(item)


def search_patient():
    keyword = entry_search.get()

    for item in table.get_children():
        values = table.item(item)["values"]

        if keyword.lower() in str(values).lower():
            table.selection_set(item)
            table.focus(item)
            return

    messagebox.showinfo("Not Found", "Patient not found")


# ------------------ TITLE ------------------ #

header = ttk.Frame(root)
header.pack(fill=X)
title = ttk.Label(header, text="Hospital Management System", font=("Segoe UI", 26, "bold"), background="#2c7be5", foreground="white", anchor="center")
title.pack(fill=X, padx=0, pady=0)
title.configure(style="TLabel")
header.configure(style="TFrame")
title.configure(background="#2c7be5", foreground="white")

# ------------------ INPUT FRAME ------------------ #

frame = ttk.Frame(root, style="TFrame")
frame.place(x=20, y=80, width=320, height=480)

ttk.Label(frame, text="Patient Name:").place(x=20, y=30)
entry_name = ttk.Entry(frame, width=25)
entry_name.place(x=140, y=30)

ttk.Label(frame, text="Age:").place(x=20, y=80)
entry_age = ttk.Entry(frame, width=25)
entry_age.place(x=140, y=80)

ttk.Label(frame, text="Gender:").place(x=20, y=130)
gender_var = StringVar(value="Male")
gender_menu = ttk.Combobox(frame, textvariable=gender_var, values=["Male", "Female", "Other"], width=22, state="readonly")
gender_menu.place(x=140, y=130)

ttk.Label(frame, text="Disease:").place(x=20, y=180)
entry_disease = ttk.Entry(frame, width=25)
entry_disease.place(x=140, y=180)

ttk.Label(frame, text="Doctor:").place(x=20, y=230)
entry_doctor = ttk.Entry(frame, width=25)
entry_doctor.place(x=140, y=230)

# Buttons
ttk.Button(frame, text="Add Patient", command=add_patient).place(x=80, y=300)
ttk.Button(frame, text="Delete Patient", command=delete_patient).place(x=80, y=350)
ttk.Button(frame, text="Clear", command=clear_fields).place(x=80, y=400)
ttk.Button(frame, text="Edit Patient", command=lambda: edit_patient()).place(x=80, y=450)

# Edit/Update patient logic
def edit_patient():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a record to edit")
        return
    item = selected[0]
    values = table.item(item)["values"]
    entry_name.delete(0, END)
    entry_name.insert(0, values[0])
    entry_age.delete(0, END)
    entry_age.insert(0, values[1])
    gender_var.set(values[2])
    entry_disease.delete(0, END)
    entry_disease.insert(0, values[3])
    entry_doctor.delete(0, END)
    entry_doctor.insert(0, values[4])

    def update():
        new_data = (entry_name.get(), entry_age.get(), gender_var.get(), entry_disease.get(), entry_doctor.get())
        table.item(item, values=new_data)
        clear_fields()
        update_btn.destroy()
        messagebox.showinfo("Success", "Patient record updated!")

    update_btn = ttk.Button(frame, text="Update Patient", command=update)
    update_btn.place(x=200, y=450)

# ------------------ SEARCH ------------------ #

Label(root, text="Search Patient:",
      bg="#f0f4f7",
      font=("Arial", 11)).place(x=350, y=90)

entry_search = Entry(root, width=30)
entry_search.place(x=470, y=90)

Button(root, text="Search",
       bg="#007bff",
       fg="white",
       command=search_patient).place(x=670, y=86)

# ------------------ TABLE ------------------ #

table_frame = Frame(root, bg="white")
table_frame.place(x=350, y=130, width=620, height=430)

scroll_y = Scrollbar(table_frame, orient=VERTICAL)

table = ttk.Treeview(table_frame,
                     columns=("Name", "Age", "Gender", "Disease", "Doctor"),
                     yscrollcommand=scroll_y.set)

scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(command=table.yview)

table.heading("Name", text="Name")
table.heading("Age", text="Age")
table.heading("Gender", text="Gender")
table.heading("Disease", text="Disease")
table.heading("Doctor", text="Doctor")

table["show"] = "headings"

table.column("Name", width=120)
table.column("Age", width=50)
table.column("Gender", width=80)
table.column("Disease", width=150)
table.column("Doctor", width=120)

table.pack(fill=BOTH, expand=1)

root.mainloop()