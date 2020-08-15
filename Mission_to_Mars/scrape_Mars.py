
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
import time
import requests


executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


def scrape_all():
# 1.......Get Mars news
    marsUrl = "https://mars.nasa.gov/news/"
    browser.visit(marsUrl)
    
# scrape page into soup
    html = browser.html
    marsSoup = bs(html, "html.parser")

# update below variables
    listItems = marsSoup.find('div', class_='list_text')
    news_title = listItems.find_all('a')[0].text
    news_p = marsSoup.find('div', class_='article_teaser_body').text

# print(news_title)
# print(news_p)


# 2.......Get featured image
    spaceUrl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(spaceUrl)


# Parse the resulting html with soup
    html = browser.html
    spaceSoup = bs(html, "html.parser")

# Find the relative image url
    carouselItems = spaceSoup.find('div', class_='img')
    spaceImgPath = carouselItems.find_all('img')[0]['src']

# Use the base url to create an absolute url
    spaceImgURL = spaceUrl + spaceImgPath

# print(spaceImgPath)
# print(spaceImgURL)



# 3.......Get hemispheres
    hemiUrl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemiUrl)

    html = browser.html
    hemiSoup = bs(html, "html.parser")

# Click the link, find the sample anchor, extract the href
    hemiresults = hemiSoup.find('div', class_='item')
    hemiImgPath = hemiresults.find_all('a')[0]['href']
    hemiImgUrl = hemiUrl + hemiImgPath

# print(hemiImgPath)
# print(hemiImgUrl)


# 4.......Get twitter weather
    weatherUrl = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weatherUrl)

    html = browser.html
    weatherSoup = bs(html, "html.parser")
# Pause for 5 seconds to let the Twitter page load before extracting the html
    time.sleep(5)

# First, find a tweet with the data-name `Mars Weather`
    weatherResults = weatherSoup.find('div', class_='css-1dbjc4n')
# weatherResults = weatherSoup.find('main', role="main")
    weatherText = weatherResults.find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    latest_weather = weatherResults.find_all('span')[5].text

# print(weatherResults)
# print(weatherText)
# print(latest_weather)


# 5........Get mars facts
    factsUrl = "http://space-facts.com/mars/"
    browser.visit(factsUrl)
#use pd.read_html and df.to_html
    factsTable = pd.read_html(factsUrl)    

    facts_df = factsTable[0]
    facts_df = facts_df.rename(columns={0: "Description", 1: "Value"})
    

    htmlTable = facts_df.to_html(table_id="html_tbl_css", justify="left", index=False)
    

# Store all scraped data in a dictionary
    mars_data = {
        "Latest_News_Title": news_title ,
        "Latest_News_Paragraph": news_p,
        "Space_Image": spaceImgURL,
        "Hemi_Image": hemiImgUrl,
        "Weather": latest_weather,
        "Table": htmlTable
}
    


#     # Stop webdriver and return data
    browser.quit()

    return mars_info
    # End Function


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

