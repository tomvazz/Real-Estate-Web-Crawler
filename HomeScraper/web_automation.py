from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import web_crawler
import database

# Chromedriver opens Century21 Real Estate site and automatically enters filters entered by user
def auto_fill(city, state, max_price_p, min_bed_p, min_bath_p, min_size_p, min_lotsize_p):
    driver = webdriver.Chrome("/Users/tomvazhekatt/Documents/Drivers/chromedriver")
    driver.get("https://www.century21.com")
    time.sleep(1)

    search_box = driver.find_element_by_xpath('//*[@id="searchText"]')
    search_box.clear()
    search_box.send_keys(f"{city}, {state}")
    time.sleep(1)

    search_btn = driver.find_element_by_xpath('//*[@id="free-text-search-button"]')
    search_btn.click()
    time.sleep(3)

    price_btn = driver.find_element_by_xpath('//*[@id="filter-price"]/span')
    price_btn.click()
    max_input = driver.find_element_by_xpath('//*[@id="filter-price"]/div[2]/input[2]')
    try:
        send_max = int(max_price_p)
        max_input.send_keys(send_max)
        max_input.send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        pass


    beds_btn = driver.find_element_by_xpath('//*[@id="filter-beds"]/span')
    beds_btn.click()
    try:
        send_beds = int(min_bed_p)
        if send_beds <= 6:
            bedcnt = driver.find_element_by_xpath(f'//*[@id="filter-beds"]/div[2]/div[{send_beds+1}]')
            bedcnt.click()
    except:
        pass
    time.sleep(1)

    baths_btn = driver.find_element_by_xpath('//*[@id="filter-baths"]/span')
    baths_btn.click()
    try:
        send_baths = int(min_bath_p)
        if send_baths <= 6:
            bathcnt = driver.find_element_by_xpath(f'//*[@id="filter-baths"]/div[2]/div[{send_baths+1}]')
            bathcnt.click()
    except:
        pass
    time.sleep(1)

    filter_btn = driver.find_element_by_xpath('//*[@id="filter-more"]/span')
    filter_btn.click()
    min_size = driver.find_element_by_xpath('//*[@id="filters-expanded-more"]/div[2]/div[1]/div[1]/input[1]')
    try:
        send_size = int(min_size_p)
        min_size.send_keys(send_size)
    except:
        pass
    lot_min_size = driver.find_element_by_xpath('//*[@id="filters-expanded-more"]/div[2]/div[1]/div[2]/input[1]')
    try:
        send_lotsize = int(min_lotsize_p)
        lot_min_size.send_keys(send_lotsize)
    except:
        pass
    time.sleep(1)
    apply_btn = driver.find_element_by_xpath('//*[@id="filterApplyButton"]')
    apply_btn.click()

    live_url = driver.current_url
    print(live_url)

    # sends current link after automated filter entries to web_crawler and retrieves data to then store in database
    h = web_crawler.house_data(live_url)
    h.parse_html()
    address_list, city_list, state_list = h.home_address()
    price_list = h.home_pricing()
    size_list = h.home_size()
    bed_list = h.home_bed_count()
    bath_list = h.home_bath_count()

    # database entries retrieved from web_crawler
    database.store_values(address_list, city_list, state_list, price_list, size_list, bed_list, bath_list)
