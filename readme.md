# Web Scraping with Selenium and Beautiful Soup

### Build with:
- Python
- Pandas
- Selenium
- Beautiful Soup

<br>

In this project I used Selenium and Beautiful Soup to scrap available information about restaurants in Krakow (Poland) on TripAdvisor website.

<br>

The crawler starts scraping on the main page https://www.tripadvisor.com/Restaurants-g274772-Krakow_Lesser_Poland_Province_Southern_Poland.html. It collects all the individual links the restaurant pages and then it opens each one of them to collect all the available info such as:
```
rank
name
link
rating
number of reviews
address
phone number
website link
menu link
price range symbol
price range
cuisines
special diets
meals
features
about
```
0 represents missing data in any of the categories listed above.
