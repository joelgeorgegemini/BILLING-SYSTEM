from tkinter import *
import random
from tkinter import messagebox
from fpdf import FPDF

class Bill_App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="#5B2C6F")
        self.root.title("Billing Software")

        # Title
        title = Label(self.root, text="Billing System", bd=12, relief=RIDGE, font=("Arial Black", 20), bg="#A569BD", fg="white").pack(fill=X)

        # Variables
        # Product Variables with quantity and price
        self.products = {
            "Nutella Choco Spread (Rs 250)": {"qty": IntVar(), "price": 250},
            "Noodles (Rs 20)": {"qty": IntVar(), "price": 20},
            "Lays (Rs 10)": {"qty": IntVar(), "price": 10},
            "Oreo (Rs 20)": {"qty": IntVar(), "price": 20},
            "Chocolate Muffin (Rs 30)": {"qty": IntVar(), "price": 30},
            "Dairy Milk Silk (Rs 60)": {"qty": IntVar(), "price": 60},
            "Namkeen (Rs 15)": {"qty": IntVar(), "price": 15}
        }

        # Total and tax variables
        self.total_price = StringVar()
        self.total_tax = StringVar()

        self.c_name = StringVar()
        self.bill_no = StringVar()
        x = random.randint(1000, 9999)
        self.bill_no.set(str(x))
        self.phone = StringVar()

        # Customer Details Label Frame
        details = LabelFrame(self.root, text="Customer Details", font=("Arial Black", 12), bg="#A569BD", fg="white", relief=GROOVE, bd=10)
        details.place(x=0, y=80, relwidth=1)

        cust_name = Label(details, text="Customer Name", font=("Arial Black", 14), bg="#A569BD", fg="white").grid(row=0, column=0, padx=15)
        cust_entry = Entry(details, borderwidth=4, width=30, textvariable=self.c_name).grid(row=0, column=1, padx=8)

        contact_name = Label(details, text="Contact No.", font=("Arial Black", 14), bg="#A569BD", fg="white").grid(row=0, column=2, padx=10)
        contact_entry = Entry(details, borderwidth=4, width=30, textvariable=self.phone).grid(row=0, column=3, padx=8)

        bill_name = Label(details, text="Bill.No.", font=("Arial Black", 14), bg="#A569BD", fg="white").grid(row=0, column=4, padx=10)
        bill_entry = Entry(details, borderwidth=4, width=30, textvariable=self.bill_no).grid(row=0, column=5, padx=8)

        # Product List Frame with Quantity Counter
        product_frame = LabelFrame(self.root, text="Products", font=("Arial Black", 12), bg="#E5B4F3", fg="#6C3483", relief=GROOVE, bd=10)
        product_frame.place(x=5, y=180, height=380, width=800)

        self.create_product_entries(product_frame)

        # Bill Area
        billarea = Frame(self.root, bd=10, relief=GROOVE, bg="#E5B4F3")
        billarea.place(x=820, y=188, width=520, height=372)

        bill_title = Label(billarea, text="Bill Area", font=("Arial Black", 17), bd=7, relief=GROOVE, bg="#E5B4F3", fg="#6C3483").pack(fill=X)

        scrol_y = Scrollbar(billarea, orient=VERTICAL)
        self.txtarea = Text(billarea, yscrollcommand=scrol_y.set)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)

        # Billing Summary
        billing_menu = LabelFrame(self.root, text="Billing Summary", font=("Arial Black", 12), relief=GROOVE, bd=10, bg="#A569BD", fg="white")
        billing_menu.place(x=0, y=560, relwidth=1, height=137)

        Label(billing_menu, text="Total Price", font=("Arial Black", 14), bg="#A569BD", fg="white").grid(row=0, column=0, padx=20, pady=1, sticky="w")
        Entry(billing_menu, borderwidth=2, width=18, textvariable=self.total_price).grid(row=0, column=1, padx=10, pady=7)

        Label(billing_menu, text="Total Tax", font=("Arial Black", 14), bg="#A569BD", fg="white").grid(row=1, column=0, padx=20, pady=1, sticky="w")
        Entry(billing_menu, borderwidth=2, width=18, textvariable=self.total_tax).grid(row=1, column=1, padx=10, pady=7)

        button_frame = Frame(billing_menu, bd=7, relief=GROOVE, bg="#6C3483")
        button_frame.place(x=830, width=500, height=95)

        button_total = Button(button_frame, text="Total Bill", font=("Arial Black", 15), pady=10, bg="#E5B4F3", fg="#6C3483", command=self.total).grid(row=0, column=0, padx=12)
        button_clear = Button(button_frame, text="Clear Field", font=("Arial Black", 15), pady=10, bg="#E5B4F3", fg="#6C3483", command=self.clear).grid(row=0, column=1, padx=10, pady=6)
        button_exit = Button(button_frame, text="Exit", font=("Arial Black", 15), pady=10, bg="#E5B4F3", fg="#6C3483", width=8, command=self.exit_app).grid(row=0, column=2, padx=10, pady=6)

        self.intro()

    def create_product_entries(self, frame):
        Label(frame, text="Product", font=("Arial Black", 12), bg="#E5B4F3", fg="#6C3483").grid(row=0, column=0, padx=20)
        Label(frame, text="Quantity", font=("Arial Black", 12), bg="#E5B4F3", fg="#6C3483").grid(row=0, column=1, padx=20)

        for i, (product, vars) in enumerate(self.products.items()):
            Label(frame, text=product, font=("Arial", 11), bg="#E5B4F3", fg="#6C3483").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            qty_counter = Spinbox(frame, from_=0, to=100, textvariable=vars["qty"], font=("Arial", 11), width=10)
            qty_counter.grid(row=i+1, column=1, padx=10, pady=5)

    def total(self):
        total_price = 0
        total_tax = 0

        self.txtarea.delete(1.0, END)
        self.txtarea.insert(END, "\tWelcome to AIT Retail\n")
        self.txtarea.insert(END, f"\nBill Number: {self.bill_no.get()}")
        self.txtarea.insert(END, f"\nCustomer Name: {self.c_name.get()}")
        self.txtarea.insert(END, f"\nPhone Number: {self.phone.get()}")
        self.txtarea.insert(END, "\n===================================")
        self.txtarea.insert(END, "\nProducts\t\tQty\tPrice")
        self.txtarea.insert(END, "\n===================================")

        # Calculate total for each product
        for product, vars in self.products.items():
            qty = vars["qty"].get()
            price = vars["price"]
            if qty > 0:
                product_total = qty * price
                self.txtarea.insert(END, f"\n{product}\t\t{qty}\t{product_total}")
                total_price += product_total

        tax = total_price * 0.05  # Assuming 5% tax on total
        total_tax += tax

        self.total_price.set(f"Rs. {total_price}")
        self.total_tax.set(f"Rs. {total_tax}")
        grand_total = total_price + total_tax

        self.txtarea.insert(END, "\n-----------------------------------")
        self.txtarea.insert(END, f"\nTotal Bill : Rs. {grand_total}")
        self.txtarea.insert(END, "\n-----------------------------------")
        self.save_bill(grand_total)

    def save_bill(self, grand_total):
        option = messagebox.askyesno("Save Bill", "Do you want to save the Bill as a PDF?")
        if option > 0:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            bill_data = self.txtarea.get(1.0, END)
            pdf.multi_cell(0, 10, bill_data)
            pdf.output(f"Bill_{self.bill_no.get()}.pdf")
            messagebox.showinfo("Saved", f"Bill No. {self.bill_no.get()} saved successfully as PDF.")
        else:
            return

    def clear(self):
        self.txtarea.delete(1.0, END)
        self.c_name.set("")
        self.phone.set("")
        self.total_price.set("")
        self.total_tax.set("")
        for vars in self.products.values():
            vars["qty"].set(0)

    def exit_app(self):
        option = messagebox.askyesno("Exit", "Do you really want to exit?")
        if option > 0:
            self.root.destroy()

    def intro(self):
        self.txtarea.delete(1.0, END)
        self.txtarea.insert(END, "\tWelcome to AIT Retail\n")
        self.txtarea.insert(END, "\nBill Number:")
        self.txtarea.insert(END, f"\n{self.bill_no.get()}")
        self.txtarea.insert(END, "\n===================================")
        self.txtarea.insert(END, "\nProducts\t\tQty\tPrice")
        self.txtarea.insert(END, "\n===================================")


# Run the application
root = Tk()
obj = Bill_App(root)
root.mainloop()
