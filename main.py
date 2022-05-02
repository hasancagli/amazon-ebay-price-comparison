from selenium import webdriver
import time
import itertools

browser = webdriver.Firefox()


def get_ebay_data(product):
    browser.get("https://www.ebay.com")

    search_bar = browser.find_element_by_xpath("//*[@id='gh-ac']")
    search_button = browser.find_element_by_xpath("//*[@id='gh-btn']")
    search_bar.send_keys(product)
    search_button.click()

    results = browser.find_elements_by_class_name("s-item")
    # First item is returning a null value
    if(results[0].find_elements_by_class_name("s-item__price")[0].get_attribute('textContent') == "$20.00"):
        results.pop(0)
    results_dict = {}
    counter = 0
    for i in range(len(results)):
        name = results[i].find_elements_by_class_name(
            "s-item__title")[0].get_attribute('textContent')
        price = results[i].find_elements_by_class_name(
            "s-item__price")[0].get_attribute('textContent')
        link = results[i].find_elements_by_tag_name(
            "a")[0].get_attribute('href')

        counter += 1
        results_dict[str(counter)] = {
            "name": name, "price": price, "link": link}

    return results_dict


def get_amazon_data(product):

    browser.get('https://www.amazon.com')
    search_bar = browser.find_element_by_xpath(
        '//*[@id="twotabsearchtextbox"]')
    search_button = browser.find_element_by_xpath(
        '//*[@id="nav-search-submit-button"]')

    search_bar.send_keys(product)
    search_button.click()

    items = browser.find_elements_by_xpath(
        '//div[contains(@class, "s-result-item s-asin")]')

    results_dict = {}
    counter = 0
    for i in range(len(items)):
        item = items[i]
        name = item.find_elements_by_xpath(
            './/span[contains(@class, "a-text-normal")]')
        link = item.find_elements_by_xpath(
            './/a[@class="a-link-normal s-no-outline"]')
        price = item.find_elements_by_xpath('.//span[@class="a-offscreen"]')

        if(len(name) > 0 and len(link) > 0 and len(price) > 0):
            name = name[0].get_attribute('textContent')
            link = link[0].get_attribute('href')
            price = price[0].get_attribute('textContent')

            counter += 1
            results_dict[str(counter)] = {"name": name,
                                          "price": price, "link": link}

    return results_dict


def sort_product_list(product_list):
    new_list = {}
    for x, y in product_list.items():
        name = y['name']
        price = y['price']
        link = y['link']

        # On ebay data, some values are ranging
        price = price.replace(' to ', "")
        price = price.replace(',', '')
        price = price.replace('$', '')[0:4]
        price = float(price)

        new_value = {'name': name, 'price': price, 'link': link}
        new_list[x] = new_value

    sorted_list = {k: v for k, v in sorted(
        new_list.items(), key=lambda item: item[1]['price'])}

    return sorted_list


def print_results(ebay, amazon):
    first_ten_amazon = dict(itertools.islice(amazon.items(), 10))
    first_ten_ebay = dict(itertools.islice(ebay.items(), 10))

    print("Top Results From Ebay: \n")
    for x, y in first_ten_ebay.items():
        print(x + "-)\nName: " +
              y['name'] + "\nPrice: " + y['price'] + "\nLink: " + y['link'])

    print("\nTop Results From Amazon: \n")
    for x, y in first_ten_amazon.items():
        print(x + "-)\nName: " +
              y['name'] + "\nPrice: " + y['price'] + "\nLink: " + y['link'])

    sorted_amazon = sort_product_list(first_ten_amazon)
    sorted_ebay = sort_product_list(first_ten_ebay)

    sorted_first_three_amazon = dict(
        itertools.islice(sorted_amazon.items(), 3))
    sorted_first_three_ebay = dict(itertools.islice(sorted_ebay.items(), 3))

    counter = 0
    print("\nCheapest Ones on Ebay:")
    for x, y in sorted_first_three_ebay.items():
        counter += 1
        print(str(counter) + "-)\nName: " +
              y['name'] + "\nPrice: " + "$" + str(y['price']) + "\nLink: " + y['link'])

    counter = 0
    print("\nCheapest Ones on Amazon:")
    for x, y in sorted_first_three_amazon.items():
        counter += 1
        print(str(counter) + "-)\nName: " +
              y['name'] + "\nPrice: " + "$" + str(y['price']) + "\nLink: " + y['link'])


product = str(input("What you want to search for: "))

ebay_data = get_ebay_data(product)
amazon_data = get_amazon_data(product)

browser.close()

print_results(ebay_data, amazon_data)
