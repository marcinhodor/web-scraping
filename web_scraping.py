## Config

# number of restaurants to be captured -> total number = NUM_iter X 30
NUM_iter = 2

## Initialize libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

## Functions
# find next button
def find_next_button(soup):
    return soup.find('a', {'class': 'next'})

def get_links_to_restaurants(soup):
    row_list = []

    link_tags = soup.findAll('a', {'class': '_15_ydu6b'})

    for tag in link_tags:
        try:    
            link = 'https://www.tripadvisor.com' + tag.attrs['href']
            text = tag.get_text().replace('. ', '.')
            rank, name = text.split('.', 1)
            row_list.append({'rank': rank, 'name': name, 'link': link})
        except:
            pass
    return row_list

def get_page_elements(soup):
    rating = None
    num_of_reviews = None
    address = None
    phone_number = None
    website_link = None
    menu_link = None
    price_range_symbol = None
    price_range = None
    cuisines = None
    special_diets = None
    meals = None
    features = None
    about = None

     # ratings
    rating = soup.find('span', {'class': 'r2Cf69qf'})
    try:
        rating = rating.get_text().replace(u'\xa0', u' ')
        rating = float(rating)
    except:
        rating = 0

    #  reviews
    reviews = soup.find('span', {'class': 'reviews_header_count'})
    try:
        reviews = reviews.get_text().replace('(', '').replace(')', '').replace(',', '')
        num_of_reviews = int(reviews)
    except:
        num_of_reviews = 0

    # addresses
    address = soup.find('a', {'class': '_15QfMZ2L', 'href': '#MAPVIEW'})
    try:
        address = address.get_text()
    except:
        address = 0

    # phone numbers
    phone_number = soup.find('span', {'class': '_15QfMZ2L'})
    try:
        phone_number = phone_number.get_text()
    except:
        phone_number = 0

    # website links
    website_link = soup.find('a', {'class': '_2wKz--mA _15QfMZ2L'})
    try:
        website_link = website_link.attrs['href']
    except:
        website_link = 0

    # menu links
    menu_link = soup.findAll('a', {'class': '_2wKz--mA _15QfMZ2L'})
    try:
        menu_link = menu_link[1].attrs['href']
    except:
        menu_link = 0

    # price range symbols
    price_range_symbol = soup.find('a', {'class': '_2mn01bsa'})
    try:
        price_range_symbol = price_range_symbol.get_text()
    except:
        price_range_symbol = 0

    # price ranges
    range1 = soup.find('div', {'class': '_1XLfiSsv'})
    range2 = soup.find('div', {'class': '_60ofm15k'})
    
    if range1:
        range1_text = range1.get_text()
        range1_text = range1_text.replace(u'\xa0', u' ')
        if 'PLN' in range1_text:
            price_range = range1_text
        else:
            price_range = 0
    elif range2:
        range2_text = range2.get_text()
        range2_text = range2_text.replace(u'\xa0', u' ')
        if 'PLN' in range2_text:
            price_range = range2_text
        else:
            price_range = 0
    else:
        price_range = 0

    # cuisines
    cuisines_soup = soup.find('div', text='CUISINES')
    try:
        cuisines_soup2 = cuisines_soup.nextSibling
        cuisines = cuisines_soup2.get_text()
    except:
        cuisines = 0

    # special diets
    special_diets_soup = soup.find('div', text='Special Diets')
    try:
        special_diets_soup2 = special_diets_soup.nextSibling
        special_diets = special_diets_soup2.get_text()
    except:
        special_diets = 0

    # meals
    meals_soup = soup.find('div', text='Meals')
    try:
        meals_soup2 = meals_soup.nextSibling
        meals = meals_soup2.get_text()
    except:
        meals = 0

    # features
    features_soup = soup.find('div', text='FEATURES')
    try:
        features_soup2 = features_soup.nextSibling
        features = features_soup2.get_text()
    except:
        features = 0

    # about
    about_soup1 = soup.find('div', {'class': '_2D5jETbG'})
    about_soup2 = soup.find('div', {'class': '_3tRlph6J'})

    if about_soup1:
        about = about_soup1.get_text()
    elif about_soup2:
        about = about_soup2.get_text()
    else:
        about = 0

    return {'rating': rating, 'num_of_reviews': num_of_reviews, 'address': address, \
    'phone_number': phone_number, 'website_link': website_link, 'menu_link': menu_link, \
    'price_range_symbol': price_range_symbol, 'price_range': price_range, 'cuisines': cuisines, \
    'special_diets': special_diets, 'meals': meals, 'features': features, 'about': about}

def iterate_over_pages(links_to_restaurants):
    # open new tab
    driver.execute_script("window.open('');")
    # switch to the new window
    driver.switch_to.window(driver.window_handles[1])

    rows_list = []

    for link in links_to_restaurants:
        driver.get(link['link'])
        try:
            driver.find_element_by_class_name("_3xJIW2mF").click()
        except:
            pass
        content = driver.page_source
        soup = BeautifulSoup(content)
        elements_dict = get_page_elements(soup)
        rows_list.append(elements_dict)

    # close new tab
    driver.close()
    # switching to old tab
    driver.switch_to.window(driver.window_handles[0])

    return rows_list

def process_main_page(soup):
    # accept cookies
    try:
        driver.find_element_by_id("_evidon-accept-button").click()
    except:
        pass

    next_button = find_next_button(soup)

    return [get_links_to_restaurants(soup), next_button]


## Open main page and get links
url = 'https://www.tripadvisor.com/Restaurants-g274772-Krakow_Lesser_Poland_Province_Southern_Poland.html'

# open main page with restaurants list
driver.get(url)

# parse html
content = driver.page_source
soup = BeautifulSoup(content)
links_to_restaurants, next_button = process_main_page(soup)


iterations = 1
while next_button and NUM_iter > iterations:
    iterations = iterations + 1
    driver.get('https://www.tripadvisor.com' + next_button.attrs['href'])
    content = driver.page_source
    soup = BeautifulSoup(content)
    new_links_to_restaurants, next_button = process_main_page(soup)
    links_to_restaurants = links_to_restaurants + new_links_to_restaurants

## Create DataFrame
df_1 = pd.DataFrame(links_to_restaurants)

## Iterate over links to get page elements
rows_list =  iterate_over_pages(links_to_restaurants)

## Create DataFrame with restaurant details
df_2 = pd.DataFrame(rows_list)

## Merge DataFrames
df = df_1.merge(df_2, left_index=True, right_index=True)

## Export to Excel
df.to_excel('trip_advisor_krakow_data.xlsx', encoding='utf-8', index=False)