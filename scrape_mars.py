# Mission to Mars
## Exported and Cleaned Code from mission_to_mars.ipynb to scrape_mars.py 

# Import Dependencies
import os
from xml.dom.minidom import Attr 
import pandas as pd
import requests
import datetime as dt
from bs4 import BeautifulSoup as bs
from splinter import Browser


def scrape_all():
    # initialize chrome browser
    browser = Browser('chrome', **executable_path, headless=False)

    # Pairs
    news_title, news_paragraph = mars_news(browser)
    hemisphere_img_urls = hemisphere(browser)

    # Dictionary for Code Storage 
    data = {
        "news_title" : news_title,
        "news_paragraph" : news_paragraph,
        "featured_image" : featured_image(browser),
        "facts" : mars_facts(), 
        "hemispheres" : hemisphere_img_urls,
        "datetime_modified" : dt.datetime.now()
    }

    # quit browser, returning data
    browser.quit()
    return data

## Scrape Mars News Website 

def mars_news(browser):
    
    # visit mars news site 
    mars_url = "https://redplanetscience.com/"
    browser.visit(mars_url)

    # html object
    html = browser.html
    # html.parser
    soup = bs(html, "html.parser")

    # try/except 
    try:
        # title text extraction
        mars_news_title = soup.find("div", class_="content_title").get_text()
        # paragraph text extraction
        mars_news_paragraph = soup.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return mars_news_title, mars_news_paragraph

## Scrape Featured Space Image

def featured_image(browser):

    # featured space image site url
    space_url = "https://spaceimages-mars.com"
    browser.visit(space_url)

    # Use spliter, find and get `featured_image_url`
    featured_image_url = "https://spaceimages-mars.com/image/featured/mars1.jpg"
    featured_image_url

    # Alternative 
    full_image = browser.find_by_id("full_image")[0]
    full_image.click()

    # html object
    html = browser.html
    # html.parser
    soup = bs(html, "html.parser")

    # try/except
    try: 
        img_url_rel = soup.select_one("figure.lede a img").get("src")

    except AttributeError:
        return None

    img_url = f'https://spaceimages-mars.com{img_url_rel}'

    return img_url

## Scrape Mars Facts

def mars_facts():

    # try/except 
    try:
        # DataFrame from HTML table, zero indexing
        df = pd.read_html("https://galaxyfacts-mars.com")[0]

    except BaseException:
        return None

    df.columns = ["description", "Mars", "Earth"]
    df.set_index("description", inplace = True)

    return df.to_html()

## Scrape Mars Hemispheres

def hemisphere(browser):

    astro_url = "https://marshemispheres.com/"
    browser.visit(astro_url)

    hemisphere_img_urls = []

    browser.visit(astro_url)
    html = browser.html
    soup = bs(html, "html.parser")
    m_url = soup.find_all("div", class_="item")
    titles = []

    for x in m_url:
        title = x.find("h3").text
        url = x.find("a")["href"]
        hemix_img_url = astro_url + url
        # visit img url
        browser.visit(hemix_img_url)
        html = browser.html
        soup = bs(html, "html.parser")
        hemisphere_img_original = soup.find("div", class_="downloads")
        hemisphere_img_url = hemisphere_img_original.find("a")["href"]
        # print url
        print(hemisphere_img_url)
        data = dict({"title":title, "img_url": hemisphere_img_url})
        hemisphere_img_urls.append(data)

        browser.back()
    return hemisphere_img_urls

if __name__== "__main__":
    print(scrape_all())


