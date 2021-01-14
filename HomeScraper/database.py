import mysql.connector


def store_values(address_list, city_list, state_list, price_list, size_list, bed_list, bath_list):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="---------",
        database="HomeScraperData"
    )

    mycursor = db.cursor()  # use to type real sql queries in "python"

    # Table Creation
    #mycursor.execute("CREATE TABLE house_data (house_id int PRIMARY KEY AUTO_INCREMENT, date_entered DATE NOT NULL, address VARCHAR(75), city VARCHAR(30), state VARCHAR(5), price int UNSIGNED, size int UNSIGNED, bed_count int UNSIGNED, bath_count int UNSIGNED)")
    #mycursor.execute("CREATE TABLE price_history (date_entered DATE NOT NULL, price_id int PRIMARY KEY AUTO_INCREMENT, house_id int UNSIGNED, address VARCHAR(75), price int UNSIGNED)")

    # ensures no repeated entries into house_data
    mycursor.execute(f"SELECT address FROM house_data")
    valid_index = []
    for i in range(len(address_list)):
        valid_index.append(True)
    for x in mycursor:
        if x[0] in address_list:
            index = address_list.index(x[0])
            valid_index[index] = False

    # enters info into house_data table
    for i in range(len(address_list)):
        if valid_index[i]:
            mycursor.execute(f"INSERT INTO house_data (date_entered, address, city, state, price, size, bed_count, bath_count) "
                             f"VALUES (CURDATE(), '{address_list[i]}', '{city_list[i]}', '{state_list[i]}', {price_list[i]}, {size_list[i]}, {bed_list[i]}, {bath_list[i]})")
        db.commit()

    # retrieves house_id's for entered addresses
    house_ids = []
    for i in range(len(address_list)):
        house_ids.append(0)
    mycursor.execute(f"SELECT house_id, address FROM house_data WHERE date_entered = CURDATE()")
    for x in mycursor:
        if x[1] in address_list:
            index = address_list.index(x[1])
            house_ids[index] = x[0]

    # enters info into price_history table along with retrieved house_id's
    for i in range(len(address_list)):
        mycursor.execute(f"INSERT INTO price_history (date_entered, house_id, address, price) "
                         f"VALUES (CURDATE(), {house_ids[i]}, '{address_list[i]}', {price_list[i]})")
        db.commit()

    print("house data")
    mycursor.execute(f"SELECT * FROM house_data")
    for x in mycursor:
        print(x)
    print("")
    print("price history")
    mycursor.execute(f"SELECT * FROM price_history")
    for x in mycursor:
        print(x)

    print("")
    print("price changes")
    mycursor.execute("SELECT * FROM (SELECT house_id, date_entered, address, price, count(*)"
                     " OVER ( partition by house_id ) h_cnt, count(*)"
                     " OVER ( partition by house_id, price ) h_P_cnt "
                     "FROM price_history ORDER BY house_id)"
                     " AS p_c "
                     "WHERE h_cnt != h_P_cnt AND house_id != 0 ORDER BY house_id, date_entered")
    addresses = []
    price_before = []
    price_after = []
    for x in mycursor:
        print(x)
        retrieved_address = x[2]
        retrieved_price = x[3]
        if retrieved_address in address_list:
            if retrieved_address not in addresses:
                addresses.append(retrieved_address)
            index = address_list.index(retrieved_address)
            if retrieved_price != price_list[index] and retrieved_price not in price_before:
                price_before.append(retrieved_price)
                price_after.append(price_list[index])

    for i in range(len(addresses)):
        print(f"{addresses[i]}, {price_before[i]}, {price_after[i]}")

    return addresses, price_before, price_after
