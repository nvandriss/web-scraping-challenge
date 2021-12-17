# setup dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)


# NASA Mars News
def news(browser):
    browser.visit('https://redplanetscience.com/')
    news_title = browser.find_by_css('div.content_title').text 
    news_p = browser.find_by_css('div.article_teaser_body').text
    return news_title, news_p

# JPL Mars Space Images - Featured Image
def image(browser):
    browser.visit('https://spaceimages-mars.com/')
    browser.find_by_tag('button')[1].click()
    return browser.find_by_css('img.fancybox-image')['src']

# Mars Facts
def facts():
    try:
        mars_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None
    mars_df.columns = ['Description', 'Mars Value','Earth Value']
    mars_df.set_index('Description',inplace=True)
    return mars_df.to_html(classes='table table-striped')

# Mars Hemispheres
def hemis(browser):
    browser.visit("https://marshemispheres.com/")
    hemisphere = []
    for i in range(4):
        hemispheres = {}
        hemispheres['title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemispheres['url'] = browser.find_by_text('Sample')['href']
        hemisphere.append(hemispheres)
        browser.back()
    return hemisphere

def scrape_all():
    news_title, news_p = news(browser)
    img_url = image(browser)
    mfacts = facts()
    mhemisphere = hemis(browser)

    mars_data = {
        "news_title":news_title,
        "news_p": news_p,
        "image": img_url,
        "facts": mfacts,
        "hemisphere":mhemisphere
    }
    browser.quit()
    return mars_data
if __name__ == "__main__":
    print(scrape_all())