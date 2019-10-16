#!/usr/bin/env python
# coding: utf-8




from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests 
import time
import pandas as pd





def open_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape_info():

    # call function to open browser 
    browser = open_browser()

    mars_dict = {}

    # ## mars.nasa.gov

    # URL of news page
    news_url = 'https://mars.nasa.gov/news/'

    # send browser to news url
    browser.visit(news_url) 
    time.sleep(1)

    # retrieve html
    news_response = browser.html

    # make bs object, parse with 'lxml'
    news_soup = bs(news_response, 'lxml')

    #find article heading and paragraph text
    mars_dict['mars_news_title'] = news_soup.find("div", class_="content_title").text
    mars_dict['mars_news_paragraph_text'] = news_soup.find("div", class_="article_teaser_body").text

    # quit browser
    #browser.quit()            

    # print article heading and paragraph text
    #print(mars_news_title)
    #print(mars_news_paragraph_text)

    # ## Space Images

    # URL of image page 
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # call function to open browser 
    #browser = open_browser()

    # send browser to image url
    browser.visit(image_url) 

    # navigate to image page
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    # retrieve html and make bs object, parse with 'html.parser'
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    # find image URL
    temp_img_url = image_soup.find('img', class_='main_image')
    back_half_img_url = temp_img_url.get('src')

    # create full URL
    mars_dict['featured_image_url'] = "https://www.jpl.nasa.gov" + back_half_img_url

    # quit browser
    #browser.quit()         

    # print URL
    #print(featured_image_url)


    # ## WEATHER

    # URL of weather page
    weather_url = "https://twitter.com/marswxreport?lang=en"

    # call function to open browser 
    #browser = open_browser()

    # send browser to image url
    browser.visit(weather_url) 

    # retrieve html and make bs object, parse with 'html.parser'
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')

    # find tweet
    tweet_containers = weather_soup.find_all('div', class_="js-tweet-text-container")


    # get text
    mars_dict['mars_weather'] = tweet_containers[0].text
    print(mars_weather)

    # quit browser
    #browser.quit()            


    # ## FACTS TABLE

    # URL of weather page
    facts_url = "https://space-facts.com/mars/"

    # use pandas to read the html
    facts_list = pd.read_html(facts_url)    

    #scrape lists
    facts_df = facts_list[1]      

    #send table to html
    mars_dict['facts_table'] = facts_df.to_html(header=False, index=False)                    # converts dataframe to html table
    print(facts_table)        


    # ## HEMISPHERE PICTURES

    # URL of hemishpere pictures
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # call function to open browser 
    #browser = open_browser()

    # send browser to image url
    browser.visit(hemi_url) 

    # retrieve html and make bs object, parse with 'html.parser'
    hemi_html = browser.html   
    soup = bs(hemi_html, "html.parser")

    # find view names
    hemisphere_names = soup.find_all('h3')

    hemisphere_image_urls=[]

    # cycle through views 
    for i in range(len(hemisphere_names)):
        
        # find view name
        title=hemisphere_names[i].text
        
        hemi_dict = {}
        
        # click view link
        browser.visit(hemi_url) 
        browser.click_link_by_partial_text(title)
        
        # retrieve html and parse with 'html.parser'
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, 'html.parser')

        # find URL
        temp_img_url = hemi_soup.find('ul').find('li')

        # add name and URL to dictionary
        hemi_dict['title'] = title
        hemi_dict['img_url'] = temp_img_url.a['href']
        
        # append dictionary to list
        hemisphere_image_urls.append(hemi_dict)
        
    mars_dict['hemisphere_image_urls']=hemisphere_image_urls
    # quit browser
    browser.quit()   
    #print(hemisphere_image_urls)

    return mars_dict



