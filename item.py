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
            "Nutella (Rs 250)": {"qty": IntVar(), "price": 250},
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

        Label(billing_menu, text="Total Tax (5%)", font=("Arial Black", 14), bg="#A569BD", fg="white").grid(row=1, column=0, padx=20, pady=1, sticky="w")
        Entry(billing_menu, borderwidth=2, width=18, textvariable=self.total_tax).grid(row=1, column=1, padx=10, pady=7)

        button_frame = Frame(billing_menu, bd=7, relief=GROOVE, bg="#6C3483")
        button_frame.place(x=830, width=500, height=95)

        button_total = Button(button_frame, text="Total Bill", font=("Arial Black", 15), pady=10, bg="#E5B4F3", fg="#6C3483", command=self.total).grid(row=0, column=0, padx=12)
        button_pdf = Button(button_frame, text="Download PDF", font=("Arial Black", 15), pady=10, bg="#E5B4F3", fg="#6C3483", command=self.download_pdf).grid(row=0, column=1, padx=10)
        button_clear = Button(button_frame, text="Clear Field", font=("Arial Black", 15), pady=10, bg="#E5B4F3", fg="#6C3483", command=self.clear).grid(row=0, column=2, padx=10, pady=6)
        button_exit = Button(button_frame, text="Exit", font=("Arial Black", 15), pady=10, bg="#E5B4F3", fg="#6C3483", width=8, command=self.exit_app).grid(row=0, column=3, padx=10, pady=6)

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

        # Adding a catchy header design
        self.txtarea.insert(END, "\n***********************************\n")
        self.txtarea.insert(END, "\t  *** AIT Retail ***\n")
        self.txtarea.insert(END, "***********************************\n")

        # Adding customer and bill details with some spacing
        self.txtarea.insert(END, f"\n Bill No:   {self.bill_no.get()}")
        self.txtarea.insert(END, f"\n Customer:  {self.c_name.get()}")
        self.txtarea.insert(END, f"\n Phone No:  {self.phone.get()}")
        self.txtarea.insert(END, "\n---------------------------------------------")

        # Centered table headers for a cleaner look
        self.txtarea.insert(END, "\n{:<25}{:<10}{:<10}".format("Products", "Qty", "Price"))
        self.txtarea.insert(END, "\n---------------------------------------------")

        # Calculate total for each product and display the product details in a cleaner format
        for product, vars in self.products.items():
            qty = vars["qty"].get()
            price = vars["price"]
            if qty > 0:
                product_total = qty * price
                # Product information with better alignment
                self.txtarea.insert(END, "\n{:<25}{:<10}{:<10}".format(product, qty, product_total))
                total_price += product_total

        # Calculate tax (assuming 5% tax rate) and display the totals
        tax = total_price * 0.05
        total_tax += tax

        self.total_price.set(f"Rs. {total_price}")
        self.total_tax.set(f"Rs. {total_tax}")
        grand_total = total_price + total_tax

        # Design for the total amount section with more spacing and separation
        self.txtarea.insert(END, "\n---------------------------------------------")
        self.txtarea.insert(END, f"\nTotal Price:\t\t   Rs. {total_price}")
        self.txtarea.insert(END, f"\nTotal Tax:\t\t   Rs. {total_tax}")
        self.txtarea.insert(END, f"\nGrand Total:\t\t   Rs. {grand_total}")
        self.txtarea.insert(END, "\n---------------------------------------------")

    def download_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)

        pdf.cell(200, 10, txt="AIT Retail - Customer Bill", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)

        # Adding customer details
        pdf.cell(200, 10, txt=f"Bill No: {self.bill_no.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Customer: {self.c_name.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Phone No: {self.phone.get()}", ln=True)
        pdf.ln(10)

        # Adding the table headers
        pdf.cell(60, 10, txt="Product", border=1)
        pdf.cell(40, 10, txt="Quantity", border=1)
        pdf.cell(40, 10, txt="Price", border=1)
        pdf.ln()

        # Adding the product details to the PDF
        for product, vars in self.products.items():
            qty = vars["qty"].get()
            price = vars["price"]
            if qty > 0:
                product_total = qty * price
                pdf.cell(60, 10, txt=product, border=1)
                pdf.cell(40, 10, txt=str(qty), border=1)
                pdf.cell(40, 10, txt=str(product_total), border=1)
                pdf.ln()

        # Adding totals
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total Price: Rs. {self.total_price.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Total Tax: Rs. {self.total_tax.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Grand Total: Rs. {float(self.total_price.get()[4:]) + float(self.total_tax.get()[4:])}", ln=True)

        # Save PDF
        pdf.output("Customer_Bill.pdf")
        messagebox.showinfo("PDF Saved", "Bill has been saved as PDF!")

    def intro(self):
        self.txtarea.delete(1.0, END)
        self.txtarea.insert(END, "\nWelcome to AIT Retail\n")
        self.txtarea.insert(END, "***********************************\n")
        self.txtarea.insert(END, "\nCustomer Bill Area\n")
        self.txtarea.insert(END, "***********************************\n")

    def clear(self):
        self.txtarea.delete(1.0, END)
        self.intro()

    def exit_app(self):
        response = messagebox.askyesno("Exit", "Do you want to exit?")
        if response > 0:
            self.root.destroy()

# Running the application
root = Tk()
obj = Bill_App(root)
root.mainloop()
