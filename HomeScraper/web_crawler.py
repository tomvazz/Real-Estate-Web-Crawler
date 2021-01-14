from bs4 import BeautifulSoup
import requests


class house_data():

    soup = ""

    def __init__(self, link):
        self.link = link

    def parse_html(self):
        # pass in html
        source = requests.get(self.link).text
        self.soup = BeautifulSoup(source, 'lxml')

    # home address is retrieved from site, info is stored in arrays and returned
    def home_address(self):
        addresses = []
        cities = []
        states = []
        for ad in self.soup.find_all("div", class_="property-address-info"):
            not_found = False
            try:
                address_txt = ad.find("div", class_="property-address").text
                city_txt = ad.find("div", class_="property-city").text
            except:
                address_txt = "0"
                city_txt = "0"
                cities.append("0")
                states.append("0")
                not_found = True
            if not not_found:
                address_txt = address_txt.split(" ")
                address_txt = f"{address_txt[15]} {address_txt[16]} {address_txt[17]} {address_txt[18]}"
                if "\n" in address_txt:
                    address_txt = address_txt.replace("\n", "")

                city_txt = city_txt.split(" ")
                city_txt = f"{city_txt[12]} {city_txt[13]} {city_txt[14]} {city_txt[15]}"
                if "\n" in city_txt:
                    city_txt = city_txt.replace("\n", "")
                num_found = False
                for i in range(len(city_txt)):
                    if city_txt[i].isdigit():
                        num_found = True
                        cities.append(city_txt[0:(i-4)])
                        states.append(city_txt[(i-3):(i-1)])
                        break
                if not num_found:
                    cities.append("0")
                    states.append("0")

            addresses.append(f"{address_txt}, {city_txt}")
        return addresses, cities, states

    # home price is retrieved from site, info is stored in array and returned
    def home_pricing(self):
        prices = []
        for p in self.soup.find_all("div", class_="property-card-primary-info"):
            not_found = False
            try:
                price_txt = p.find("a", class_="listing-price").text
            except:
                price_txt = 0
                not_found = True
            if not not_found:
                price_txt = price_txt.replace(",", "")
                start_index = 0
                end_index = 0
                start_index_collected = False
                for i in range(len(price_txt)):
                    if price_txt[i].isdigit() and not start_index_collected:
                        start_index = i
                        start_index_collected = True
                    if start_index_collected and not price_txt[i].isdigit():
                        end_index = i
                        break
                price_txt = price_txt[start_index:end_index]
            prices.append(int(price_txt))
        return prices

    # home size in square feet is retrieved from site, info is stored in array and returned
    def home_size(self):
        sizes = []
        for s in self.soup.find_all("div", class_="property-card-primary-info"):
            not_found = False
            try :
                size_txt = s.find("div", class_="property-sqft").text
            except :
                size_txt = 0
                not_found = True
            if not not_found:
                start_index = 0
                end_index = 0
                start_index_collected = False
                for i in range(len(size_txt)):
                    if size_txt[i].isdigit() and not start_index_collected:
                        start_index = i
                        start_index_collected = True
                    if size_txt[i] == "s":
                        end_index = i-1
                        break
                size_txt = size_txt[start_index:end_index]
                size_txt = size_txt.replace(",", "")
            sizes.append(int(size_txt))
        return sizes

    # bed count is retrieved from site, info is stored in array and returned
    def home_bed_count(self):
        beds = []
        for b in self.soup.find_all("div", class_="property-card-primary-info"):
            not_found = False
            try:
                bed_txt = b.find("div", class_="property-beds").text
            except:
                bed_txt = 0
                not_found = True
            if not not_found:
                for i in range(len(bed_txt)):
                    if bed_txt[i].isdigit():
                        if bed_txt[i+1].isdigit():
                            bed_txt = f"{bed_txt[i]}{bed_txt[i+1]}"
                        else:
                            bed_txt = bed_txt[i]
                        break
            beds.append(int(bed_txt))
        return beds

    # bath count is retrieved from site, info is stored in array and returned
    def home_bath_count(self):
        baths = []
        for b in self.soup.find_all("div", class_="property-card-primary-info"):
            not_found = False
            try:
                bath_txt = b.find("div", class_="property-baths").text
            except:
                bath_txt = 0
                not_found = True
            if not not_found:
                for i in range(len(bath_txt)):
                    if bath_txt[i].isdigit():
                        if bath_txt[i+1].isdigit():
                            bath_txt = f"{bath_txt[i]}{bath_txt[i+1]}"
                        else:
                            bath_txt = bath_txt[i]
                        break
            baths.append(int(bath_txt))
        return baths