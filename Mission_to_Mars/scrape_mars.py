#!/usr/bin/env python
# coding: utf-8

# setup dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

# NASA Mars News Scrape
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    soup.find("div", class_="content_title")
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text


# JPL Mars Space Images - Featured Image Scrape
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    full_img = browser.find_by_tag("button")
    full_img.click()
    html = browser.html
    img_soup = bs(html,"html.parser")


    img_url = img_soup.find(class_="headerimage fade-in").get('src')
    img_url


    featured_image_url = f"https://spaceimages-mars.com/{img_url}"
    print(featured_image_url)


    # Mars Facts

    mars_df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    mars_df.columns = ['Description', 'Mars Value','Earth Value']
    mars_df.set_index('Description',inplace=True)
    mars_df
    mars_df.to_html()


    # Mars Hemispheres
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)


    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')
    items = hemi_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemi_url + partial_img_url)
        partial_img_html = browser.html
        hemi_soup = bs(partial_img_html, 'html.parser')
        img_url = hemi_url + hemi_soup.find('img', class_='wide-image')['src']
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
    hemisphere_image_urls

    mars_data = {
            "news_title": news_title,
            "news_paragraph": news_p,
            "featured_image": featured_image_url,
            "mars_facts": mars_df,
            "hemispheres": hemisphere_image_urls
            }

    browser.quit()

    return mars_data
