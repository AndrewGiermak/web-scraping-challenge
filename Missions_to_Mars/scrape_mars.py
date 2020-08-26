# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

#create global dictionary 
mars_dict = {}

# scrape one section at a time
# NASA Mars News

def scrape_news():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find("div", class_= "content_title").get_text()
    paragraph_text = soup.find("div", class_="article_teaser_body").get_text()

    # put in mars_dict
    mars_dict["news_title"] = news_title
    mars_dict["paragraph_text"] = paragraph_text

    browser.quit()
    return mars_dict

# featured image
def scrape_image():
    browser = init_browser()
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    time.sleep(1)

    html_image = browser.html
    soup = bs(html_image, "html.parser")

    featured_image_url  = soup.find("article")["style"].replace("background-image: url(','').replace(');', '')[1:-1]")
    main_url = "https://www.jpl.nasa.gov"
    featured_image_url = main_url + featured_image_url
    featured_image_url

    mars_dict["featured_image_url"] = featured_image_url

    browser.quit()
    return mars_dict

# Mars Facts
def scrape_facts():
    browser = init_browser()
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")

    tables = pd.read_html(facts_url)
    mars_df = tables[1]
    html_table = (mars_df.to_html()).replace('\n', '')

    mars_dict["html_table"] = html_table

    browser.quit()
    return mars_dict

# Hemispheres
def scrape_hemispheres():
    browser = init_browser()
    hemisphere_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    items = soup.find_all("div", class_="item")
    hem_image_urls = []
    hem_main_url = "https://astrogeology.usgs.gov"
    for item in items: 
        title = item.find("h3").text
        image_url = item.find("a", class_="itemLink product-item")["href"]
        browser.visit(hem_main_url + image_url)
        image_html = browser.html
        soup = bs(image_html, "html.parser")
        image_url = hem_main_url + soup.find("img", class_="wide-image")["src"]
        hem_image_urls.append({"Title" : title, "Image_URL" : image_url})

    mars_dict["hem_image_urls"] = hem_image_urls

    browser.quit()
    return mars_dict