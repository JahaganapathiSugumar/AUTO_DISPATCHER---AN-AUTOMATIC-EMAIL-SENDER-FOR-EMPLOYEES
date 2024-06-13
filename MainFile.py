import csv
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import shortuuid
import mysql.connector as m
import re
import ssl
import smtplib
from email.message import EmailMessage
from tkinter import simpledialog
####################################################################################################################################################
mydb = m.connect(
    host="localhost",
    user="root",
    passwd="jaha@075",
    database="email_information"
)
mycursor = mydb.cursor()
####################################################################################################################################################
all_entries = []
users = []
invalid_users = []
regex = ""
####################################################################################################################################################
num_of_users = 0
prefix = ""
####################################################################################################################################################
email_body = ""
email_subject = ""
####################################################################################################################################################

def all_users_submit():
    try:
        num_of_users = user_count_entry.get()
        num_of_users = int(num_of_users)
        user_count_entry.delete(0, tk.END)
        user_entries(num_of_users)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid integer for the user count.")

####################################################################################################################################################

def user_entries(num_of_users):
    global all_entries, each_user_frame, user_count_frame
    for each_user in range(num_of_users):
        each_user_frame = tk.Frame(window, bg="#f0f0f0")
        each_user_frame.pack(padx=10, pady=5, fill='x')

        each_user_label_name = tk.Label(each_user_frame, text="Enter Name of the User:", bg="#f0f0f0", fg="#000000")
        each_user_label_name.grid(row=0, column=0, padx=5, pady=3)
        each_user_name = tk.Entry(each_user_frame)
        each_user_name.grid(row=0, column=1, padx=5, pady=3)

        each_user_label_email = tk.Label(each_user_frame, text="Enter Email of the User:", bg="#f0f0f0", fg="#000000")
        each_user_label_email.grid(row=1, column=0, padx=5, pady=3)
        each_user_email = tk.Entry(each_user_frame)
        each_user_email.grid(row=1, column=1, padx=5, pady=3)

        each_user_label_type = tk.Label(each_user_frame, text="Select User Type:", bg="#f0f0f0", fg="#000000")
        each_user_label_type.grid(row=2, column=0, padx=5, pady=3)
        each_user_combobox = ttk.Combobox(each_user_frame, values=["client", "project manager", "resident"])
        each_user_combobox.grid(row=2, column=1, padx=5, pady=3)

        all_entries.append({'name': each_user_name, "email": each_user_email, 'type': each_user_combobox})

    submit_button2 = tk.Button(window, text="SUBMIT ALL USERS", command=extract_data, bg="#4caf50", fg="#ffffff", activebackground="#45a049")
    submit_button2.pack(pady=10)

####################################################################################################################################################

def extract_data():
    global users
    messagebox.showinfo("Info", "All the users submitted successfully")
    for user in all_entries:
        user_name = user['name'].get()
        user_email = user['email'].get()
        user_type = user['type'].get()
        if (user_type == "client"):
            prefix = "C"
        elif (user_type == "project manager"):
            prefix = "P"
        elif (user_type == "resident"):
            prefix = "R"
        user_id = prefix + shortuuid.ShortUUID().random(length=5)
        users.append({"user_id": user_id, 'user_name': user_name, 'user_email': user_email, 'user_type': user_type})
    insert_all_user()
    window.destroy()

####################################################################################################################################################

def insert_all_user():
    all_user_file = "all_user.csv"
    with open(all_user_file, "a", newline="") as all_file:
        writer_obj = csv.writer(all_file)
        file_is_empty = os.path.getsize(all_user_file) == 0

        if file_is_empty:
            field = ["id", "name", "email", "user_type"]
            writer_obj.writerow(field)
        for user in users:
            writer_obj.writerow([user['user_id'], user['user_name'], user['user_email'], user['user_type']])

        messagebox.showinfo("info", "Successfully inserted")
    insert_pending_user()

####################################################################################################################################################

def insert_pending_user():
    pending_user_file = "pending_user.csv"
    with open(pending_user_file, "a", newline="") as pending_file:
        writer_obj = csv.writer(pending_file)
        file_is_empty = os.path.getsize(pending_user_file) == 0

        if file_is_empty:
            field = ["id", "name", "email", "user_type"]
            writer_obj.writerow(field)
        for user in users:
            writer_obj.writerow([user['user_id'], user['user_name'], user['user_email'], user['user_type']])
    insert_into_all_and_pending()

####################################################################################################################################################

def insert_into_all_and_pending():
    for i in users:
        mycursor.execute("INSERT INTO all_users(user_id,user_name,user_email,user_type) VALUES(%s,%s,%s,%s)",
                         (i["user_id"], i["user_name"], i["user_email"], i["user_type"]))
        mycursor.execute("INSERT INTO pending_users(user_id,user_name,user_email,user_type) VALUES(%s,%s,%s,%s)",
                         (i["user_id"], i["user_name"], i["user_email"], i["user_type"]))
        mydb.commit()
    

####################################################################################################################################################

def retrieve_data():
    mycursor.execute("SELECT user_id,user_name,user_email,user_type FROM pending_users")

    res = mycursor.fetchall()
    data = []
    for i in res:
        data.append(i)

    for each_data in data:
        e_user_id, e_user_name, e_user_email, e_user_type = each_data
        validate_email_for_all(e_user_id, e_user_name, e_user_email, e_user_type)

####################################################################################################################################################

def validate_email_for_all(e_user_id, e_user_name, e_user_email, e_user_type):
    global regex
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(regex, e_user_email):
        send_email_to_all(e_user_id, e_user_name, e_user_email, e_user_type)
    else:
        messagebox.showinfo("info", "Email invalid")
        invalid_users.append((e_user_id, e_user_name, e_user_email, e_user_type))
        prompt_update_invalid_email(e_user_id, e_user_name, e_user_email, e_user_type)

####################################################################################################################################################

def prompt_update_invalid_email(e_user_id, e_user_name, e_user_email, e_user_type):
    update_window = tk.Toplevel(window)
    update_window.title("Update Invalid Email")
    update_window.geometry("400x300")

    tk.Label(update_window, text="Update Email Address").pack(pady=10)

    tk.Label(update_window, text="User ID:").pack()
    tk.Label(update_window, text=e_user_id).pack()

    tk.Label(update_window, text="Name:").pack()
    tk.Label(update_window, text=e_user_name).pack()

    tk.Label(update_window, text="Current Email:").pack()
    email_entry = tk.Entry(update_window)
    email_entry.insert(0, e_user_email)
    email_entry.pack(pady=5)

    def update_email():
        new_email = email_entry.get()
        if re.match(regex, new_email):
            update_database_and_csv(e_user_id, new_email)
            update_window.destroy()
        else:
            messagebox.showerror("Invalid input", "Please enter a valid email address.")

    tk.Button(update_window, text="Update Email", command=update_email).pack(pady=10)

####################################################################################################################################################

def update_database_and_csv(user_id, new_email):

    mycursor.execute("UPDATE all_users SET user_email = %s WHERE user_id = %s", (new_email, user_id))
    mycursor.execute("UPDATE pending_users SET user_email = %s WHERE user_id = %s", (new_email, user_id))
    mydb.commit()

    def update_csv(file_name):
        rows = []
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                if row[0] == user_id:
                    row[2] = new_email
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    update_csv("all_user.csv")
    update_csv("pending_user.csv")

####################################################################################################################################################

def send_email_to_all(e_user_id, e_user_name, e_user_email, e_user_type):
    email_sender = "jahaganapathi1@gmail.com"
    email_password = "xuerbuuzgebekyhz"
    email_receiver = e_user_email

    if (e_user_type == "client"):
        email_subject = "Welcome to Tech solution pvt. ltd. - Important Information Inside!"
        email_body = f"""Dear {e_user_name},\n
We are excited to welcome you to our Company Our team is dedicated to providing you with the best service and support to meet your needs. 

As a valued client, we want to ensure that you have all the necessary information to get started. Below are some important details:

1. **Account Manager:** Your dedicated account manager is john, and they will be your primary point of contact. You can reach them at Account Manager's Email or Account Manager's Phone Number.

2. **Client Portal:** Access your client portal at ts.com using your login credentials. Here, you can view your account details, track progress, and more.

3. **Support:** For any support inquiries, please contact our support team at techsolution@gmail.com . We are here to help you 24/7.

Thank you for choosing Tech solution pvt. ltd. We look forward to a successful partnership.
"""

    elif (e_user_type == "project manager"):
        email_subject = "Team Meeting - Project Updates and Next Steps"
        email_body = f"""Hi {e_user_name},\n
I hope this email finds you well. I wanted to provide an update on our current projects and discuss the next steps.

1. **Project A:** We have successfully completed phase 1 and are moving on to phase 2. The team has done an excellent job staying on schedule. We will need your input on the final deliverables.

2. **Project B:** We encountered a minor setback due to issue, but we have implemented a solution and are back on track. We should discuss any potential impacts on the timeline.

3. **Next Steps:** Let's schedule a team meeting to review our progress and address any concerns. Please let me know your availability for a meeting this week.

Thank you for your leadership and support. I look forward to our continued success.
"""

    elif (e_user_type == "resident"):
        email_subject = "Welcome to [Community Name]!"
        email_body = f"""Dear {e_user_name},\n
Welcome to [Community Name]! We are thrilled to have you as part of our community. 

To help you settle in, here are some key details:

1. **Community Manager:** Your community manager is Manager's Name. If you have any questions or need assistance, feel free to reach out to them at [Manager's Email] or [Manager's Phone Number].

2. **Resident Portal:** Access your resident portal at Portal URL using your login credentials. Here, you can submit maintenance requests, view community updates, and more.

3. **Emergency Contact:** For any emergencies, please contact our emergency hotline at Emergency Phone Number.

We hope you enjoy your new home. If you have any questions or need assistance, please do not hesitate to reach out.
"""

    em = EmailMessage()
    em['from'] = email_sender
    em["To"] = email_receiver
    em['Subject'] = email_subject
    em.set_content(email_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    log_sent_email(e_user_id, e_user_name, e_user_email, e_user_type, email_subject, email_body)

   
    mycursor.execute("DELETE FROM pending_users WHERE user_id = %s", (e_user_id,))
    mydb.commit()

    mycursor.execute("INSERT INTO sent_users(user_id,user_name,user_email,user_type) VALUES(%s,%s,%s,%s)",
                     (e_user_id, e_user_name, e_user_email, e_user_type))
    mydb.commit()

    update_csv("all_user.csv", e_user_id, e_user_email)
    update_csv("pending_user.csv", e_user_id, e_user_email)

  
    messagebox.showinfo("Success", f"Email successfully sent to {e_user_name} ({e_user_email}).")
#####################################################################################################################################################################
def update_csv(file_name, user_id, new_email):
    rows = []
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        for row in rows:
            if row[0] == user_id:
                row[2] = new_email
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
####################################################################################################################################################

def log_sent_email(user_id, user_name, user_email, user_type, subject, body):
    sent_email_file = "sent_emails.csv"
    with open(sent_email_file, "a", newline="") as sent_file:
        writer_obj = csv.writer(sent_file)
        file_is_empty = os.path.getsize(sent_email_file) == 0

        if file_is_empty:
            field = ["id", "name", "email", "user_type", "subject", "body"]
            writer_obj.writerow(field)
        writer_obj.writerow([user_id, user_name, user_email, user_type, subject, body])

####################################################################################################################################################

def view_sent_emails():
    sent_email_file = "sent_emails.csv"
    if os.path.exists(sent_email_file):
        with open(sent_email_file, "r") as sent_file:
            reader = csv.reader(sent_file)
            emails = list(reader)
            display_sent_emails(emails)
    else:
        messagebox.showinfo("Info", "No sent emails to display.")

####################################################################################################################################################

def display_sent_emails(emails):
    emails_window = tk.Toplevel(window)
    emails_window.title("Sent Emails")
    emails_window.geometry("800x600")

    emails_frame = tk.Frame(emails_window)
    emails_frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(emails_frame, columns=("ID", "Name", "Email", "User Type", "Subject", "Body"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("User Type", text="User Type")
    tree.heading("Subject", text="Subject")
    tree.heading("Body", text="Body")
    tree.pack(fill=tk.BOTH, expand=True)

    for email in emails:
        tree.insert("", tk.END, values=email)

####################################################################################################################################################

def on_submit():
    num_of_users = int(user_count_entry.get())
    user_entries(num_of_users)

####################################################################################################################################################

def driver():
        action = action_combobox.get()
        if action == "1":
            num_of_users_entry = simpledialog.askinteger("Number of Users", "Enter the number of users :", parent=window)
            if num_of_users_entry is not None and num_of_users_entry > 0:
                user_entries(num_of_users_entry)
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid number of users.")
        elif action == "2":
            retrieve_data()
        elif action == "3":
            view_sent_emails()
        elif action == "4":
            return 
        else:
            messagebox.showerror("Invalid Action", "Please select a valid action (1, 2, 3, or 4).")



window = tk.Tk()
window.title("User Entry Form")
window.config(bg="#e0e0e5")

frame = tk.Frame(window, bg="#e0e0e0")
frame.pack()

action_frame = tk.LabelFrame(frame, text="Select Action", bg="#ffffff", fg="#030202")
action_frame.grid(row=0, column=0, padx=20, pady=20)

action_label = tk.Label(action_frame, text="Choose Action (1: Get Users, 2: Send Emails, 3: Generate Report):", bg="#ffffff", fg="#030202")
action_label.grid(row=0, column=0, padx=5, pady=5)

action_combobox = ttk.Combobox(action_frame, values=["1", "2", "3","4"])
action_combobox.grid(row=0, column=1, padx=5, pady=5)

submit_action_button = tk.Button(action_frame, text="SUBMIT", command=driver, bg="#2196f3", fg="#ffffff", activebackground="#1e88e5")
submit_action_button.grid(row=1, column=0)

num_of_users_frame = tk.LabelFrame(frame, text="ALL USER COUNT", bg="#ffffff", fg="#030202")
user_count_label = tk.Label(num_of_users_frame, text="Total Number Of Users:", bg="#ffffff", fg="#030202")
user_count_label.grid(row=0, column=0, padx=5, pady=5)

user_count_entry = tk.Entry(num_of_users_frame)
user_count_entry.grid(row=0, column=1, padx=5, pady=5)

submit_button1 = tk.Button(num_of_users_frame, text="SUBMIT", command=all_users_submit, bg="#2196f3", fg="#ffffff", activebackground="#1e88e5")
submit_button1.grid(row=1, column=0, columnspan=2, pady=10)


window.mainloop()
