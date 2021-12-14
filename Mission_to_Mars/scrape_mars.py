# setup dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape():
    mars_data = {}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_p = news(browser)
    mars_data['title'] = news_title
    mars_data['paragraph'] = news_p
    mars_data['image'] = image(browser)
    mars_data['facts'] = facts()
    mars_data['hemisphere'] = hemis(browser)
    return mars_data

# NASA Mars News
def news(browser):
    browser.visit('https://redplanetscience.com/')
    news_title = browser.find("div", class_="content_title").get_text()
    news_p = browser.find('div', class_="article_teaser_body").get_text()
    return news_title, news_p

# JPL Mars Space Images - Featured Image
def image(browser):
    browser.visit('https://spaceimages-mars.com/')
    browser.find_by_tag("button")[1].click()
    return browser.find(class_="headerimage fade-in").get('src')

# Mars Facts
def facts():
    mars_df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    mars_df.columns = ['Description', 'Mars Value','Earth Value']
    mars_df.set_index('Description',inplace=True)
    mars_df
    return mars_df.to_html(classes='data table', index=False, header=False, border=0)

# Mars Hemispheres
def hemis(browser):
    browser.visit("https://marshemispheres.com/")
    hemisphere_image_urls = []
    for i in range(4):
        hemisphere = {}
        hemisphere['title'] = browser.find('a.itemLink h3')[i].text
        browser.find('a.itemLink h3')[i].click()
        hemisphere['url'] = browser.find_by_text('Sample')['href']
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    browser.quit()
    return hemisphere_image_urls