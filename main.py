from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)
browser.get("https://www.amazon.it/gp/bestsellers/pc")

# create json file if it doesn't exist
with open("data.json", "w") as f:
    json.dump([], f)

# open json file
with open("data.json", "r") as file:
    data = json.load(file)

# default value
isNextActive = True

json_objects = []
items = []

while isNextActive:
    
    while len(items) != 50:
        browser.execute_script("window.scrollBy(0,1500)")

        time.sleep(2)

        elem_list = browser.find_element(By.CSS_SELECTOR, "div.p13n-desktop-grid")

        items = elem_list.find_elements(By.CLASS_NAME, "p13n-grid-content")

        print(len(items))


    for item in items:
            title = item.find_element(By.CLASS_NAME, "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1").text
            print("Title: ",title)
            price = item.find_element(By.CLASS_NAME, "_cDEzb_p13n-sc-price_3mJ9Z").text
            print("Price: ",price)
            prod_link = item.find_element(By.CLASS_NAME, "a-link-normal").get_attribute("href")
            print("Product URL: ",prod_link)
            prod_image = item.find_element(By.CLASS_NAME, "p13n-product-image").get_attribute("src")
            print("Image URL",prod_image)
            print("")
            # create new json object with scraped data
            new_data = {"Title": str(title), "Price":str(price), "Product URL:":str(prod_link), "Iamge URL":str(prod_image)}
            # append json obj to array
            json_objects.append(new_data)

    items = []

    # check disabled button text
    button_text = browser.find_element(By.CLASS_NAME, 'a-disabled').text
    print(button_text)

    if button_text == "Pagina successiva→":
        print('disabled button found')
        isNextActive = False
        print(len(json_objects))
        data.extend(json_objects)
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
    else:
        browser.find_element(By.CLASS_NAME, "a-last").click()
        print('disabled button not found')




    