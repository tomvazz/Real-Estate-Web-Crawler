from tkinter import *
import web_automation

# new GUI window appears when called
def new_window(city, state):
    root1 = Tk()
    root1.title("Advanced Search")
    w1 = 300
    h1 = 330
    ws = root1.winfo_screenwidth()  # width of the screen
    hs = root1.winfo_screenheight()  # height of the screen
    x1 = (ws / 2) - (w1 / 2)
    y1 = (hs / 2) - (h1 / 2)
    root1.geometry('%dx%d+%d+%d' % (w1, h1, x1, y1))
    search_frame = Frame(root1, width=w1, height=h1, bg="gray18")
    search_frame.place(x=0, y=0)

    max_price_entry = Entry(root1, width=19, font=("Futura", 20), bg="gray30", fg="NavajoWhite4")
    max_price_entry.insert(0, "Max Price")
    max_price_entry.place(x=20, y=20)

    min_bed_entry = Entry(root1, width=8, font=("Futura", 20), bg="gray30", fg="NavajoWhite4")
    min_bed_entry.insert(0, "Beds")
    min_bed_entry.place(x=20, y=80)

    min_bath_entry = Entry(root1, width=8, font=("Futura", 20), bg="gray30", fg="NavajoWhite4")
    min_bath_entry.insert(0, "Baths")
    min_bath_entry.place(x=163, y=80)

    house_size_entry = Entry(root1, width=19, font=("Futura", 20), bg="gray30", fg="NavajoWhite4")
    house_size_entry.insert(0, "Min Size (sq ft)")
    house_size_entry.place(x=20, y=140)

    lot_size_entry = Entry(root1, width=19, font=("Futura", 20), bg="gray30", fg="NavajoWhite4")
    lot_size_entry.insert(0, "Min Lot Size (acres)")
    lot_size_entry.place(x=20, y=200)

    # when user has finished entries and clicks "Search"
    def go():
        max_price_p = max_price_entry.get()
        min_bed_p = min_bed_entry.get()
        min_bath_p = min_bath_entry.get()
        min_size_p = house_size_entry.get()
        min_lotsize_p = lot_size_entry.get()

        # calls Selenium web automation to autofill parameters entered by user
        web_automation.auto_fill(city, state, max_price_p, min_bed_p, min_bath_p, min_size_p, min_lotsize_p)

    searchbtn = Button(root1, text="Search", font=("Futura", 20), bg="gray18", fg="gray26", padx=95, pady=8, command=go)
    searchbtn.place(x=20, y=260)

    root1.mainloop()  # running loop