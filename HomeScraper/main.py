from tkinter import *
import database
import web_crawler
import email_update
import advanced_search

# house data is displayed in GUI
def insert_values(address_list, price_list, size_list, bed_list, bath_list, address_pc, price_before, price_after):
    # city data entered
    for i in range(len(address_list)):
        if (i > 20):
            break
        # " ".join adds a space between each character to space out
        addresses[i].configure(text=" ".join(address_list[i]))
        sizes[i].configure(text=" ".join(str(size_list[i])) + "   sq. ft")
        beds[i].configure(text=" ".join(str(bed_list[i])))
        baths[i].configure(text=" ".join(str(bath_list[i])))
        prices[i].configure(text="$ " + " ".join(str(price_list[i])))
        divisor = int(price_list[i]/100000)
        if divisor < 24:
            price_visuals[i].configure(text="$ " * divisor)
        else:
            price_visuals[i].configure(text=("$ " * 24) + "...")

    # price history is erased and updated with new location entry, email msg is written
    subject = "HOUSE PRICE CHANGE"
    msg = "Check out these price changes\n"

    for i in range(3):
        address_changes[i].configure(text="")
        old_prices[i].configure(text="")
        new_prices[i].configure(text="")
        changes[i].configure(text="")
    count = 0
    for i in range((len(address_pc)-1), -1, -1):
        address_changes[count].configure(text=" ".join(address_pc[i]))
        old_prices[count].configure(text=" ".join(str(price_before[i])))
        new_prices[count].configure(text=" ".join(str(price_after[i])))
        change = price_after[i]-price_before[i]
        if change < 0:
            changes[count].configure(text=" ".join(str(change)), fg="SpringGreen2")
        else:
            changes[count].configure(text="+ " + " ".join(str(change)), fg="tomato")

        msg = msg + f"ADDRESS: {address_pc[i]}  PREVIOUS PRICE: ${price_before[i]}  CURRENT PRICE: ${price_after[i]}\n"
        msg = msg + f"CHANGE: ${change}\n"

        count += 1
        if count == 3:
            break

    # sends email update, if change in price is recorded
    if count > 0:
        email_update.send_email(subject, msg)


# When the OK Button is pressed
def myClick():
    # retrieves contents of input boxes
    city = city_box.get()
    state = state_box.get()

    # takes care of cities with over one word
    altcity = city
    if " " in city:
        altcity = city.replace(" ", "-")

    # sends link to web_crawler and retrieves data
    h = web_crawler.house_data(
        f"https://www.century21.com/real-estate/{altcity.lower()}-{state.lower()}/LC{state.upper()}{city.upper()}/")
    h.parse_html()
    address_list, city_list, state_list = h.home_address()
    price_list = h.home_pricing()
    size_list = h.home_size()
    bed_list = h.home_bed_count()
    bath_list = h.home_bath_count()

    # database entries
    address_pc, price_before, price_after = database.store_values(address_list, city_list, state_list, price_list, size_list, bed_list, bath_list)

    # updated lists are passed to insert into graphical interface
    insert_values(address_list, price_list, size_list, bed_list, bath_list, address_pc, price_before, price_after)


# mathod called when filter button pressed
def filter():
    city = city_box.get()
    state = state_box.get()
    # new window appears with more advanced search
    advanced_search.new_window(city, state)

# TKINTER GUI SETUP
# starting frame
root = Tk()
root.title("")
w = 1300
h = 900
# to place screen in center
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
master_frame = Frame(root, width=w, height=h, bg="gray40")
master_frame.place(x=0, y=0)

# header
header_frame = Frame(root, width=w, height=80, bg="gray18")
header_frame.place(x=0, y=0)
line1_frame = Frame(root, width=350, height=3, bg="NavajoWhite4")
line1_frame.place(x=230, y=39)
line2_frame = Frame(root, width=350, height=3, bg="NavajoWhite4")
line2_frame.place(x=720, y=39)
title = Label(root, text="EST⌂TES", font=("Futura", 30), fg="NavajoWhite4", bg="gray18")
title.place(x=588, y=17)

# type boxes to enter city and state
citylbl = Label(root, text="CITY", font=("Futura", 50), fg="gray26", bg="gray40")
citylbl.place(x=748, y=120)
statelbl = Label(root, text="STATE", font=("Futura", 50), fg="gray26", bg="gray40")
statelbl.place(x=710, y=190)
city_box = Entry(root, width=9, font=("Futura", 40), bg="gray30", fg="NavajoWhite4")
city_box.place(x=885, y=123)
state_box = Entry(root, width=9, font=("Futura", 40), bg="gray30", fg="NavajoWhite4")
state_box.place(x=885, y=193)

# "OK" and "Filter" buttons
ok_button = Button(root, text="OK", font=("Futura", 40), bg="gray18", fg="NavajoWhite4", padx=20, pady=27, command=myClick)
ok_button.place(x=1138, y=122)
advanced_btn = Button(root, text="Filter", font=("Futura", 20), bg="gray18", fg="gray26", padx=29, pady=5, command=filter)
advanced_btn.place(x=1138, y=219)

# Home Retrieval Display
results_frame = Frame(root, width=1200, height=460, bg="gray18")
results_frame.place(x=50, y=300)
numlbl = Label(root, text="No.", font=("Futura", 20), fg="NavajoWhite4", bg="gray18")
numlbl.place(x=80, y=310)
addresslbl = Label(root, text="Address", font=("Futura", 20), fg="NavajoWhite4", bg="gray18")
addresslbl.place(x=160, y=310)
sizelbl = Label(root, text="Size", font=("Futura", 20), fg="NavajoWhite4", bg="gray18")
sizelbl.place(x=600, y=310)
bedslbl = Label(root, text="Beds", font=("Futura", 20), fg="NavajoWhite4", bg="gray18")
bedslbl.place(x=700, y=310)
bathslbl = Label(root, text="Baths", font=("Futura", 20), fg="NavajoWhite4", bg="gray18")
bathslbl.place(x=800, y=310)
pricelbl = Label(root, text="Price", font=("Futura", 20), fg="NavajoWhite4", bg="gray18")
pricelbl.place(x=900, y=310)

# Labels set for display
numbers = []
for i in range(20):
    numbers.append(Label(root, text=str(i+1), font=("Futura", 10), fg="gray60", bg="gray18"))
    numbers[i].place(x=80, y=(343+(20*i)))

addresses = []
for i in range(20):
    addresses.append(Label(root, text="", font=("Futura", 10), fg="blanched almond", bg="gray18"))
    addresses[i].place(x=160, y=(343+(20*i)))

sizes = []
for i in range(20):
    sizes.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    sizes[i].place(x=600, y=(343+(20*i)))

beds = []
for i in range(20):
    beds.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    beds[i].place(x=700, y=(343+(20*i)))

baths = []
for i in range(20):
    baths.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    baths[i].place(x=800, y=(343+(20*i)))

prices = []
for i in range(20):
    prices.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    prices[i].place(x=900, y=(343+(20*i)))

price_visuals = []
for i in range(20):
    price_visuals.append(Label(root, text="", font=("Futura", 10), fg="PaleGreen2", bg="gray18"))
    price_visuals[i].place(x=1000, y=(343+(20*i)))

# Price Change Display
price_frame = Frame(root, width=640, height=150, bg="gray18")
price_frame.place(x=50, y=115)

price_frame_heading = Frame(root, width=640, height=32, bg="gray30")
price_frame_heading.place(x=50, y=115)

price_change = Label(root, text="PRICE CHANGE", font=("Futura", 15), fg="gray18", bg="gray30")
price_change.place(x=80, y=118)

address_changelbl = Label(root, text="Address", font=("Futura", 15), fg="NavajoWhite4", bg="gray18")
address_changelbl.place(x=80, y=150)

old_pricelbl = Label(root, text="OP", font=("Futura", 15), fg="NavajoWhite4", bg="gray18")
old_pricelbl.place(x=420, y=150)

new_pricelbl = Label(root, text="NP", font=("Futura", 15), fg="NavajoWhite4", bg="gray18")
new_pricelbl.place(x=510, y=150)

plus_minuslbl = Label(root, text="+/-", font=("Futura", 15), fg="NavajoWhite4", bg="gray18")
plus_minuslbl.place(x=600, y=150)

address_changes = []
for i in range(3):
    address_changes.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    address_changes[i].place(x=80, y=(180+(23*i)))

old_prices = []
for i in range(3):
    old_prices.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    old_prices[i].place(x=420, y=(180+(23*i)))

new_prices = []
for i in range(3):
    new_prices.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    new_prices[i].place(x=510, y=(180+(23*i)))

changes = []
for i in range(3):
    changes.append(Label(root, text="", font=("Futura", 10), fg="gray60", bg="gray18"))
    changes[i].place(x=600, y=(180+(23*i)))


root.mainloop() # GUI running loop
