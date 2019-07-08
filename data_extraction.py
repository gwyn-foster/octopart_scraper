import re
import csv
import selenium
import random
from selenium import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome('../BarcodeScanning/chromedriver')

readFile = open("barcodes.rtf", "r")
#input = raw_input("Scan the barcode now ")

#random locations
randClicks = ['product-overview','qty','priced-in','additionalPackaging','nptReference']


## Get product number
pn_p = re.compile('(?<=\[\)>06P)(.+)(?=1P)')

pn2_p = re.compile('(?<=P)(.+)(?<=-ND)')
pn3_p = re.compile('(?<=06P1P)(.+)(?=6PXP)')

## Manufacterer Part Number
mpn_p = re.compile('(?<=1P)(.+)(?=K1K)')
mpn2_p = re.compile('(?<=1P)(.+)(?=9D)')
mpn3_p = re.compile('(?<=1P)(.+)(?=Q)')
## Quanitity
q_p = re.compile('(?=Q[^A-Z])(.+)(?=11Z)')
q2_p = re.compile('(?<=Q)(.+)(?=13Z)')
q3_p = re.compile('(?<=Q)(.+)(?=11K)')
q4_p = re.compile('(?<=Q)(.+)(?=V00)')



with open('inventory_data.csv', mode='w') as inventory:
    inventory_writer = csv.writer(inventory, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in readFile:
        if "K" in line:
            if "[)>06P1P" in line: ## Texas Instruments
                time = random.randint(5,20)

                driver.implicitly_wait(time)
                input = line
                product_number = pn3_p.findall(input)
                m_product_number = product_number
                quantity = q4_p.findall(input)
                page = 'https://octopart.com/manufacturers/texas-instruments'
            elif "[)>06P" in line:
                time = random.randint(5, 35)

                driver.implicitly_wait(time)
                input = line
                product_number = pn_p.findall(input)
                m_product_number = mpn_p.findall(input)
                quantity = q_p.findall(input)
                page = 'https://octopart.com/distributors/digi-key'
            elif "[)>06J" in line: ## Old digikey barcode
                time = random.randint(5, 35)

                driver.implicitly_wait(time)
                input = line
                product_number = pn2_p.findall(input)
                m_product_number = mpn2_p.findall(input)
                quantity = q2_p.findall(input)
                page = 'https://octopart.com/distributors/digi-key'
            elif ">[)>06K" in line: ##Mouser item
                time = random.randint(5, 35)
                driver.implicitly_wait(time)
                input = line
                m_product_number = mpn3_p.findall(input)
                product_number = m_product_number
                quantity = q3_p.findall(input)
                page = 'https://octopart.com/distributors/mouser'
            print(product_number[0])
            driver.get(page)
            search_box = driver.find_element_by_xpath("//input[@class='search-input']")
            search_box.send_keys(product_number)
            search_button = driver.find_element_by_xpath("//button[@class='search-button']")
            search_button.click()
            try:
                elem = driver.find_element_by_xpath("//div[@class='nrf-alert']")
            except NoSuchElementException:
                specs_button = driver.find_element_by_xpath("//button[@value='serp-grid']")
                specs_button.click()
                time = random.randint(5, 35)
                driver.implicitly_wait(time)
                cat_name = driver.find_elements_by_xpath("//div[@class='fa fa-angle-right']/span[@class='category-crumb']")
                if not cat_name:
                    cat_name = driver.find_elements_by_xpath("//span[@class='category-name']")

                category = [z.text for z in cat_name]
                attribute_names = driver.find_elements_by_xpath("//tr[@class='matrix-row-col-names']/th")
                item_attributes = driver.find_elements_by_xpath("//div[@class='small']")
                time = random.randint(5, 35)
                driver.implicitly_wait(time)
                attributes = [x.text for x in item_attributes]

                attribute_title =[y.text for y in attribute_names]
                attribute_title_string = ','.join(attribute_title)
                title_list = attribute_title_string.split(',')
                new_titles = title_list[3:]
                print(category)
                print (new_titles)
                print(attributes, '\n')
                box = "/"
                if category:
                    if "Resistors" in category[0]:
                        cat_index = new_titles.index("Resistance")
                        val = attributes[cat_index]
                        box = "8,9"
                    elif "Capacitor" in category[0]:
                        if "Capacitance" in attribute_title_string:
                            cat_index = new_titles.index("Capacitance")
                            val = attributes[cat_index]
                            box = "1,2"
                        else:
                            val = "/"
                            box = "1/2"
                    elif "Inductor" in category[0]:
                        if "Inductor" in attribute_title_string:
                            cat_index = new_titles.index("Inductance")
                            val = attributes[cat_index]
                            box = "7"
                        else:
                            val = "/"
                            box = "7"
                    elif "Crystal" in category[0]:
                        cat_index = new_titles.index("Frequency")
                        val = attributes[cat_index]
                        box = "4"
                    elif "Connector" in category[0]:
                        box = "3"
                        val = "/"
                    elif "Header" in category[0]:
                        box = "3"
                        val = "/"
                    elif "Diode" in category[0]:
                        box = "4"
                        val = "/"
                    elif "Switching" in category[0]:
                        box = "5"
                        val = "/"
                    elif "Audio" in category[0]:
                        box = "5"
                        val = "/"
                    elif "Transistor" in category[0] or "Speaker" in category[0] or "MOSFET" in category[0] or "Switch" in category[0]:
                        box = "10"
                        val = "/"
                    elif "LED" in category[0]:
                        box = "10"
                        if "Illumination Color" in attribute_title_string:
                            colour_index = new_titles.index("Illumination Color")
                            val = attributes[colour_index]
                        else:
                            val = "/"
                    else:
                        val = "/"
                else:
                    category ="/"
                    val = "/"
                if "Case/Package" in attribute_title_string:
                    footprint_index = new_titles.index("Case/Package")
                    if footprint_index:
                        footprint = attributes[footprint_index]
                else:
                    footprint = "/"
                if "Number of Pins" in attribute_title_string:
                    pin_index = new_titles.index("Number of Pins")
                    pins = attributes[pin_index]
                else:
                    pins = "/"
                if "Lead Pitch" in attribute_title_string:
                    pitch_index = new_titles.index("Lead Pitch")
                    pitch = attributes[pitch_index]
                elif "Pitch" in attribute_title_string:
                    pitch_index = new_titles.index("Pitch")
                    pitch = attributes[pitch_index]
                else:
                    pitch="/"
                if "Zener Diode" in attribute_title_string:
                    z_rating_index = new_titles.index("Zener Voltage")
                    val = attributes[z_rating_index]
                if "Power Rating" in attribute_title_string:
                    p_rating_index = new_titles.index("Power Rating")
                    p_rating = attributes[p_rating_index]
                else:
                    p_rating = "/"
                if "Max Voltage Rating (AC)" in attribute_title_string:
                    v_rating_index = new_titles.index("Max Voltage Rating (AC)")
                    v_rating = attributes[v_rating_index]
                elif "Voltage Rating (DC)" in attribute_title_string:
                    v_rating_index = new_titles.index("Voltage Rating (DC)")
                    v_rating = attributes[v_rating_index]
                elif "Voltage Rating" in attribute_title_string:
                    v_rating_index = new_titles.index("Voltage Rating")
                    v_rating = attributes[v_rating_index]
                else:
                    v_rating = "/"
                if "Max Current Rating" in attribute_title_string:
                    c_rating_index = new_titles.index("Max Current Rating")
                    c_rating = attributes[c_rating_index]
                elif "Current Rating" in attribute_title_string:
                    c_rating_index = new_titles.index("Current Rating")
                    c_rating = attributes[c_rating_index]
                else:
                    c_rating = "/"

            inventory_writer.writerow([box,category[0],product_number[0],m_product_number[0],val,v_rating,c_rating,p_rating,footprint,pitch,"/",quantity[0], pins])
readFile.close()
inventory.close()
