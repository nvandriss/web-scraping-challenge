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
    news_title = browser.find_by_css('div', class_='content_title').get_text()
    news_p = browser.find_by_css('div', class_="article_teaser_body").get_text()
    return news_title, news_p

# JPL Mars Space Images - Featured Image
def image(browser):
    browser.visit('https://spaceimages-mars.com/')
    browser.find_by_tag('button')[1].click()
    return browser.find_by_css(class_='img.fancybox-image').get('src')

# Mars Facts
def facts():
    mars_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    mars_df.columns = ['Description', 'Mars Value','Earth Value']
    mars_df.set_index('Description',inplace=True)
    return mars_df.to_html(classes='data table', index=False, header=False, border=0)

# Mars Hemispheres
def hemis(browser):
    browser.visit("https://marshemispheres.com/")
    hemisphere_image_urls = []
    for i in range(4):
        browser.links.find_by_partial_text('Hemisphere')[i].click()
        title =bs(browser.html, 'html.parser').find('h2', class_='title').text
        img_url =bs(browser.html, 'html.parser').find('li').a.get('href')
        hemisphere = {}
        hemisphere['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemisphere['title'] = title
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    browser.quit()
    return hemisphere_image_urls