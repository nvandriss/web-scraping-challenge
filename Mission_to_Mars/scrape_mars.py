#!/usr/bin/env python
# coding: utf-8

# In[1]:


# setup dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# NASA Mars News
url = "https://redplanetscience.com/"
browser.visit(url)


# In[4]:


html = browser.html
soup = bs(html, "html.parser")


# In[5]:


soup.find("div", class_="content_title")


# In[6]:


news_title = soup.find("div", class_="content_title").get_text()
print(news_title)


# In[7]:


news_p = soup.find('div', class_="article_teaser_body").get_text()
print(news_p)


# In[9]:


# JPL Mars Space Images - Featured Image
url = "https://spaceimages-mars.com/""
browser.visit(url)


# In[12]:


full_img = browser.find_by_tag("button")
full_img.click()


# In[19]:


html = browser.html
img_soup = bs(html,"html.parser")


# In[22]:


img_url = img_soup.find(class_="headerimage fade-in").get('src')
img_url


# In[24]:


featured_image_url = f"https://spaceimages-mars.com/{img_url}"
print(featured_image_url)


# In[31]:


# Mars Facts
mars_df = pd.read_html("https://galaxyfacts-mars.com/")[0]
mars_df.columns = ['Description', 'Mars Value','Earth Value']
mars_df.set_index('Description',inplace=True)
mars_df


# In[32]:


mars_df.to_html()


# In[36]:


# Mars Hemispheres
hemi_url = "https://marshemispheres.com/"
browser.visit(hemi_url)


# In[37]:


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

