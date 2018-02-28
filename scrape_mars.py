

import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape():

    # NASA Mars News
    # use splinter to navigate to the website and fetch the news title and descritption
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find('div', class_='image_and_description_container')
    image_url = articles.find('div', class_='list_image')
    image_url.find('img')['src']
    info = articles.find('div', class_='list_text')
    news_title = info.find('div', class_="content_title").get_text()
    news_description = info.find('div', class_="article_teaser_body").get_text()
    

    # JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    time.sleep(3)
    #get full image url by clicking on the Full Image button and navigating to that page
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_div= soup.find('div', class_='fancybox-inner')
    img_url =img_div.find('img')['src']
    # append the url to the base url
    featured_image_url = 'https://www.jpl.nasa.gov/' + img_url
    featured_image_url



    #Mars Weather
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # wait untill the browser fetches the information
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather= soup.find('p', class_='js-tweet-text').text
    mars_weather


    # Mars Facts
    url = 'https://space-facts.com/mars/'
    facts_df = pd.read_html(url)[0]
    facts_df = facts_df.rename(columns={0: 'description', 1: 'value'})
    #convert it to dictionaries and then to list of dictionaries
    mars_facts = facts_df.T.to_dict().values()
    mars_facts = list(mars_facts)

 

    # Mars Hemisperes
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url)
    # wait untill the browser fetches the information
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # create an emty list to save dictionaries of img_urls and titles
    hemisphere_image_urls = []

    base_url = "https://astrogeology.usgs.gov/"
    hemispheres= soup.find_all('div', class_='item')
    for hemisphere in hemispheres:
        hemisphere_info = {}
        hemispheres_title = hemisphere.find('h3').text
        hemisphere_info['title'] = hemispheres_title
        hemispheres_url = hemisphere.find('a')['href']
        browser.visit(base_url + hemispheres_url)
        new_html = browser.html
        new_soup = BeautifulSoup(new_html, 'html.parser')
        hemisphere_full_url = new_soup.find('img', class_="wide-image")['src']
        hemisphere_info['img_url'] = base_url + hemisphere_full_url
        hemisphere_image_urls.append(hemisphere_info)
        browser.back()


    return {'news_description' : news_description, 
            'news_title' : news_title,
            'featured_image_url': featured_image_url,
            'mars_weather': mars_weather,
            'hemisphere_image_urls': hemisphere_image_urls,
            'mars_facts' : mars_facts}