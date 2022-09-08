from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup as bs
import requests
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(f"{url}")
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    html = browser.html
    mars_image_soup = bs(html, 'html.parser')
    image_path = mars_image_soup.find_all('img')[1]["src"]
    featured_image_url = image_url + image_path

    # Mars Facts HTML
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(mars_facts_url)
    mars_factsDF = tables[0]
    mars_facts_html = mars_factsDF.to_html()
    mars_facts_html.replace('\n', '')

    # Mars Hemispheres
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')

    # For loop for the hemisphere images
    for i in range(4):
    
        browser.find_by_css('a.product-item img')[i].click()
        time.sleep(3)
    
        image_soup = bs(browser.html, 'html.parser')
        img_title = browser.find_by_css('h2.title').text
        img_url = image_soup.find('img', class_="wide-image")['src']
        hemisphere_image_url = hemispheres_url + img_url
    
        hemisphere_image_urls.append({"title": img_title,
                              "img_url": hemisphere_image_url})
    
    browser.quit()

    # Mars Dictionary of Information
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_facts_html),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict