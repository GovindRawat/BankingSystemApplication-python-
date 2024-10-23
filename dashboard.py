import itertools
from datetime import datetime
from tkinter import messagebox
import customtkinter
import mysql
from CTkTable import CTkTable
from PIL import Image
from customtkinter import *
import connection

colors = ["#070F2B", "#1B1A55", "#535C91"]
# colors = ["#070F2B", "#1B1A55", "#535C91"]
# colors = ["#FF204E","#A0153E","#5D0E41"]
# colors = ["#FAF0E6","#B9B4C7","#5C5470"]
# colors = ["#9290C3", "#535C91", "#1B1A55"]
fonts = 'Century Gothic'


class Dashboard(customtkinter.CTk):
    def __init__(self, username, password):
        # Create the objects dashboard
        super().__init__()
        self.title("Dashboard")
        self.username = username
        self.password = password
        print(self.username)
        self.search_container = None
        self.geometry("856x645+300+120")
        self.resizable(False, False)

        try:
            self.db = connection.Connection().get_connection()
            self.cursor = self.db.cursor()
            self.cursor.execute("select * from acc_details where accno = %s", (self.username,))
            self.result = self.cursor.fetchall()
            self.result = self.result[0]
            for i in self.result:
                print(i)
        except mysql.connector.Error as e:
            print(e)

        # self.set_appearance_mode("dark-blue")

        self.sidebar_frame = CTkFrame(master=self, fg_color=colors[1], width=176, height=650, corner_radius=16,
                                      bg_color=colors[0])
        self.sidebar_frame.pack_propagate(False)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")

        self.person_img_data = Image.open("Images/person_icon.png")
        self.person_img = CTkImage(dark_image=self.person_img_data, light_image=self.person_img_data)
        customtkinter.CTkButton(master=self.sidebar_frame, image=self.person_img, text_color=colors[2],
                                text=f"Account\n{self.result[1]}", fg_color="transparent", font=("Arial Bold", 14),
                                hover_color=colors[0], anchor="NW").pack(anchor="center", ipady=5, pady=(10, 0))

        self.transaction_img_data = Image.open("Images/transaction.png")
        self.transaction_img = CTkImage(dark_image=self.transaction_img_data, light_image=self.transaction_img_data)
        customtkinter.CTkButton(master=self.sidebar_frame, image=self.transaction_img, text_color=colors[2],
                                text="Transactions", fg_color="transparent", font=("Arial Bold", 14),
                                hover_color=colors[0], anchor="w", command=self.transaction).pack(anchor="center",
                                                                                                  ipady=5, pady=(60, 0))

        self.transaction_history_img_data = Image.open("Images/package_icon.png")
        self.transaction_history_img = CTkImage(dark_image=self.transaction_history_img_data,
                                                light_image=self.transaction_history_img_data)

        CTkButton(master=self.sidebar_frame, image=self.transaction_history_img, text="Transaction\nHistory",
                  text_color=colors[2], fg_color="transparent", font=("Arial Bold", 14), hover_color=colors[0],
                  anchor="w", command=self.history).pack(anchor="center", ipady=5, pady=(16, 0))

        self.personal_detail_data = Image.open("Images/list_icon.png")
        self.personal_detail = CTkImage(dark_image=self.personal_detail_data, light_image=self.personal_detail_data)
        CTkButton(master=self.sidebar_frame, image=self.personal_detail, text="Personal\nDetails", text_color=colors[2],
                  fg_color="transparent", font=("Arial Bold", 14), hover_color=colors[0], anchor="w",
                  command=self.personal_details).pack(anchor="center", ipady=5, pady=(16, 0))

        self.deposit_img_data = Image.open("Images/deposit (1).png")
        self.deposit_img = CTKImage(dark_image=self.deposit_img_data, light_image=self.deposit_img_data)
        CTkButton(master=self.sidebar_frame, image=self.deposit_img, text="Deposit", text_color=colors[2],
                  fg_color="transparent",
                  font=("Arial Bold", 14), hover_color=colors[0], anchor="w", command=self.deposit).pack(
            anchor="center", ipady=5, pady=(16, 0))

        self.person_img_data = Image.open("Images/logout_1.png")
        self.person_img = CTkImage(dark_image=self.person_img_data, light_image=self.person_img_data)
        CTkButton(master=self.sidebar_frame, image=self.person_img, text_color="#B53939", text="logout",
                  fg_color="transparent", font=("Arial Bold", 14), hover_color=colors[0], anchor="S",
                  command=self.logout).pack(anchor="center", ipady=15, pady=(200, 0))

        self.main_view = CTkFrame(master=self, fg_color=colors[0], width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(False)
        self.main_view.pack(side="left")

        self.title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=self.title_frame, text=f"Hey, Welcome {self.result[1]} ", font=("Arial Black", 25),
                 text_color=colors[2]).pack(anchor="nw", side="left")

        self.metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))

        self.account_metric = CTkFrame(master=self.metrics_frame, fg_color=colors[1], width=200, height=60)
        self.account_metric.grid_propagate(False)
        self.account_metric.pack(side="left")

        self.logitics_img_data = Image.open("Images/logistics_icon.png")
        self.logistics_img = CTkImage(light_image=self.logitics_img_data, dark_image=self.logitics_img_data,
                                      size=(43, 43))

        CTkLabel(master=self.account_metric, image=self.logistics_img, text="").grid(row=0, column=0, rowspan=2,
                                                                                     padx=(12, 5), )

        CTkLabel(master=self.account_metric, text="Account Type", text_color="white", font=("Arial Black", 15)).grid(
            row=0, column=1, sticky="sw")
        CTkLabel(master=self.account_metric, text=f"{self.result[7]}", text_color="#fff", font=("Arial Black", 17),
                 justify="left").grid(row=1, column=1, sticky="nw", pady=(0, 10))

        self.balance_metric = CTkFrame(master=self.metrics_frame, fg_color=colors[1], width=200, height=60)
        self.balance_metric.grid_propagate(False)
        self.balance_metric.pack(side="left", expand=True, anchor="center")

        self.shipping_img_data = Image.open("Images/shipping_icon.png")
        self.shipping_img = CTkImage(light_image=self.shipping_img_data, dark_image=self.shipping_img_data,
                                     size=(43, 43))

        CTkLabel(master=self.balance_metric, image=self.shipping_img, text="").grid(row=0, column=0, rowspan=2,
                                                                                    padx=(12, 5), )

        CTkLabel(master=self.balance_metric, text="Balance", text_color="#fff", font=("Arial Black", 15)).grid(row=0,
                                                                                                               column=1,
                                                                                                               sticky="sw")
        CTkLabel(master=self.balance_metric, text=f"{self.result[8]}", text_color="#fff", font=("Arial Black", 15),
                 justify="left").grid(row=1, column=1, sticky="nw", pady=(0, 10))
        self.window_count = 0
        if self.window_count == 0:
            self.transaction()
        else:
            pass

    def deposit(self):
        if self.window_count == 1:
            self.transaction_frame.destroy()
        elif self.window_count == 2:
            self.details_frame.destroy()
        elif self.window_count == 3:
            self.table_frame.destroy()

        if self.window_count == 4:
            pass
        else:
            self.window_count = 4
            self.deposit_frame = CTkFrame(master=self.main_view, height=400, fg_color=colors[1], corner_radius=16)
            self.deposit_frame.pack(fill="x", pady=(45, 0), padx=27)

            self.label_transaction = CTkLabel(master=self.deposit_frame, text_color=colors[2],
                                              text="Deposit\nTo Perform any transaction.\nPlease fill the given "
                                                   "details.",
                                              font=("Arial Black", 20))
            self.label_transaction.place(x=150, y=10)

            self.amount_label = CTkLabel(master=self.deposit_frame, text_color=colors[2],
                                         text="Amount to be Deposited",
                                         font=("Arial BLack", 17))
            self.amount_label.place(x=35, y=250)

            self.amount_entry = CTkEntry(master=self.deposit_frame, width=200, font=("Arial Black", 17))
            self.amount_entry.place(x=335, y=250)

            self.Deposit_button = CTkButton(master=self.deposit_frame, text="Deposit", command=self.add_money)
            self.Deposit_button.place(x=225, y=350)

    def add_money(self):
        username = self.username
        print(username)
        db = connection.Connection().get_connection()
        entered_amount = int(self.amount_entry.get())

        cursor = db.cursor()
        query = "SELECT balance FROM acc_details WHERE accno = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        print(result)

        if result is not None:
            current_balance = float(result[0])
            new_balance = current_balance + entered_amount

            update_query = "UPDATE acc_details SET balance = %s WHERE accno = %s"
            cursor.execute(update_query, (new_balance, self.username))
            db.commit()
            cursor.close()

            print("Deposit successful. New balance:", new_balance)
        else:
            print("Account not found or result is None.")

    def transaction(self):
        if self.window_count == 2:
            self.details_frame.destroy()
        elif self.window_count == 3:
            self.table_frame.destroy()
        elif self.window_count == 4:
            self.deposit_frame.destroy()

        if self.window_count == 1:
            pass
        else:
            self.window_count = 1
            self.transaction_frame = CTkFrame(master=self.main_view, height=400, fg_color=colors[1], corner_radius=16)
            self.transaction_frame.pack(fill="x", pady=(45, 0), padx=27)

            self.label_transaction = CTkLabel(master=self.transaction_frame, text_color=colors[2],
                                              text="Transactions\nTo Perfom any transaction.\nPlease fill the given "
                                                   "details.",
                                              font=("Arial Black", 20))
            self.label_transaction.place(x=150, y=10)

            self.sender_label = CTkLabel(master=self.transaction_frame,
                                         text="Enter the Account number\nof the receiver",
                                         text_color=colors[2], font=("Arial Black", 17))
            self.sender_label.place(x=30, y=130)

            self.sender_entry = CTkEntry(master=self.transaction_frame, font=("Arial Black", 17), width=200)
            self.sender_entry.place(x=335, y=140)

            self.amount_label = CTkLabel(master=self.transaction_frame, text_color=colors[2], text="Amount to be "
                                                                                                   "Transferred",
                                         font=("Arial BLack", 17))
            self.amount_label.place(x=35, y=250)

            self.amount_entry = CTkEntry(master=self.transaction_frame, width=200, font=("Arial Black", 17))
            self.amount_entry.place(x=335, y=250)

            self.transfer_button = CTkButton(master=self.transaction_frame, text="Transfer",
                                             command=self.confirm_transaction)
            self.transfer_button.place(x=225, y=350)

    def confirm_transaction(self):
        dt = datetime.now()
        date = dt.date()
        time = dt.time()

        acc_no = self.sender_entry.get()
        amt = float(self.amount_entry.get())
        if acc_no != self.username:
            if amt > 0:
                if amt <= float(self.result[8]):
                    self.cursor.execute("SELECT * from acc_details where accno = %s ", (acc_no,))
                    amount_of_sender = self.cursor.fetchall()
                    print(amount_of_sender)
                    if amount_of_sender == []:
                        messagebox.showerror("Error", "This Account doesn't exist")
                    else:
                        user_data = (amount_of_sender[0])
                        amount_of_sender = str(user_data[8])

                        self.amount_entry.delete(0, END)
                        self.sender_entry.delete(0, END)

                        self.password_of_account = CTkInputDialog(
                            text=f"You are transfering money to {user_data[1]}\nAmount:{amt}\nPlease Enter your account "
                                 f"password to confirm transfer",
                            title="Confirm the transaction",
                            fg_color=colors[1],
                            button_fg_color=colors[0])
                        password_of_account = self.password_of_account.get_input()
                        print(self.password_of_account)

                        if password_of_account == self.password:
                            remaining_balance = float(self.result[8]) - float(amt)
                            print(remaining_balance)

                            self.cursor.execute("update acc_details set balance = %s where accno = %s",
                                                (remaining_balance, self.username,))

                            new_amount = float(amount_of_sender) + float(amt)
                            new_amount = str(new_amount)

                            self.cursor.execute("UPDATE acc_details SET balance = %s WHERE accno = %s",
                                                (new_amount, acc_no,))

                            messagebox.showinfo("Transaction", "Transaction Successful")
                            add_amt = f"+{amt}"
                            minus_amt = f"-{amt}"
                            self.cursor.execute("SELECT * from acc_details where accno = %s ", (acc_no,))
                            trass = self.cursor.fetchall()
                            print(trass)
                            self.cursor.execute(
                                "insert into transaction_history(accno, sender_accno, name ,amount, date , time) values("
                                "%s,%s,%s,%s,%s,%s)",
                                (self.username, acc_no, user_data[1], minus_amt, date, time))
                            self.cursor.execute(
                                "insert into transaction_history(accno, sender_accno, name ,amount, date , time) values("
                                "%s,%s,%s,%s,%s,%s)",
                                (acc_no, self.username, user_data[1], add_amt, date, time))
                            print("history done")
                            self.db.commit()
                            CTkLabel(master=self.balance_metric, text=f"{remaining_balance}", text_color="#fff",
                                     font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw",
                                                                                    pady=(0, 10))
                        else:
                            messagebox.showerror("Error", "Your entered wrong password")
                else:
                    messagebox.showerror("Error", "You have low balance")
            else:
                messagebox.showerror("Error", "please enter correct Account Number")
        else:
            messagebox.showerror("Error", "Please enter correct amount")

    def personal_details(self):
        if self.window_count == 1:
            self.transaction_frame.destroy()
        elif self.window_count == 3:
            self.table_frame.destroy()
        elif self.window_count == 4:
            self.deposit_frame.destroy()

        if self.window_count == 2:
            pass
        else:
            self.window_count = 2
            self.details_frame = CTkFrame(master=self.main_view, height=400, fg_color=colors[1], corner_radius=16)
            self.details_frame.pack(fill="x", pady=(45, 0), padx=27)

            self.name = self.result[1]
            self.email = self.result[5]
            self.acc_no = self.result[0]
            self.dob = self.result[2]
            self.gender = self.result[3]
            self.phone_no = self.result[4]
            self.address = self.result[6]

            self.title_label = CTkLabel(master=self.details_frame, text="Personal Details of the Account holder",
                                        text_color=colors[2], font=("Arial Black", 22))
            self.title_label.grid(row=0, column=0, padx=70, pady=10)

            self.name_label = CTkLabel(master=self.details_frame, text=f"Name :- {self.name}", text_color=colors[2],
                                       font=("Arial Black", 17))
            self.name_label.grid(row=1, column=0, padx=70, pady=10)

            self.email_label = CTkLabel(master=self.details_frame, text=f"Email :- {self.email}",
                                        text_color=colors[2],
                                        font=("Arial Black", 17))
            self.email_label.grid(row=2, column=0, padx=70, pady=10)

            self.dob_label = CTkLabel(master=self.details_frame, text=f"Date Of Birth :- {self.dob}",
                                      text_color=colors[2],
                                      font=("Arial Black", 17))
            self.dob_label.grid(row=3, column=0, padx=70, pady=10)

            self.phone_no_label = CTkLabel(master=self.details_frame, text=f"Phone Number :- {self.phone_no}",
                                           text_color=colors[2],
                                           font=("Arial Black", 17))
            self.phone_no_label.grid(row=4, column=0, padx=70, pady=10)

            self.gender_label = CTkLabel(master=self.details_frame, text=f"Gender :- {self.gender}",
                                         text_color=colors[2],
                                         font=("Arial Black", 17))
            self.gender_label.grid(row=5, column=0, padx=70, pady=10)

            self.account_number_label = CTkLabel(master=self.details_frame, text=f"Account Number :- {self.acc_no}",
                                                 text_color=colors[2],
                                                 font=("Arial Black", 17))
            self.account_number_label.grid(row=6, column=0, padx=70, pady=10)

            self.address_label = CTkLabel(master=self.details_frame, text=f"Address :- {self.address}",
                                          text_color=colors[2],
                                          font=("Arial Black", 17))
            self.address_label.grid(row=7, column=0, padx=70, pady=10)

    def logout(self):
        self.destroy()
        import login
        login = login.Login()
        login.mainloop()

    def history(self):
        if self.window_count == 1:
            self.transaction_frame.destroy()
        elif self.window_count == 2:
            self.details_frame.destroy()
        elif self.window_count == 4:
            self.deposit_frame.destroy()

        if self.window_count == 3:
            pass
        else:
            try:
                self.db = connection.Connection().get_connection()
                self.cursor = self.db.cursor()
                self.cursor.execute("select sender_accno,name,amount,date,time from transaction_history where accno = "
                                    "%s", (self.username,))
                self.data = self.cursor.fetchall()
                for result in self.data:
                    print(result)
            except mysql.connector.Error as e:
                print(e)

            self.table_data = [
                [("Account\nNumber", "Name", "Amount", "Date", "Time")]
            ]
            self.table_data.append(self.data)
            self.table_data = list(itertools.chain(*self.table_data))
            print(self.table_data)
            self.table_frame = CTkFrame(master=self.main_view, fg_color="transparent")
            self.table_frame.pack(expand=True, fill="both", padx=27, pady=21)
            table = CTkTable(master=self.table_frame, values=self.table_data, colors=[colors[1], colors[2]],
                             header_color=colors[1])
            table.edit_row(0, text_color="#fff")
            table.pack(expand=True)
            self.window_count = 3


if __name__ == '__main__':
    dashboard = Dashboard()
    dashboard.mainloop()
