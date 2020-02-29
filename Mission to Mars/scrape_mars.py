def scrape():

    from splinter import Browser
    from bs4 import BeautifulSoup
    import time
    import pandas as pd
    import requests



    
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

   

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
   
    time.sleep(10)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title=soup.find('div', class_="content_title").text
    news_p=soup.find('div',class_="article_teaser_body").text

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)

    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov'+feat_img_url

   

    twitter_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)  
    time.sleep(10)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    mars_weather=soup.find('div',class_="css-1dbjc4n r-1j3t67a").text

   


    table_url="https://space-facts.com/mars/"
    browser.visit(table_url)
    time.sleep(10)

    table=pd.read_html(table_url)
    table_df=pd.DataFrame(table[1])
    table_df.columns=["Comparison","Mars","Earth"]
    table_df=table_df.drop("Earth",axis=1)
    table_df=table_df.to_html()
    table_df.replace('\n', '')
    
   


    
    

    hemisphere_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    time.sleep(10)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_images_urls = []

    hemisphere_titles = soup.find_all('h3')

    for i in range(len(hemisphere_titles)):
        hemisphere_title = hemisphere_titles[i].text
        hemisphere_image = browser.find_by_tag('h3')
        hemisphere_image[i].click()
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        image = soup.find('img', class_='wide-image')['src']
        image_url = "https://astrogeology.usgs.gov" + image
    
    
        hemisphere_dict = {"title": hemisphere_title, "imgage_url":image_url}
        hemisphere_images_urls.append(hemisphere_dict)

    
    mars_dict={"news_title":news_title, "news_p":news_p, "featured_image_url":featured_image_url, "mars_weather":mars_weather, "table_df":table_df, "hemisphere_images_urls":hemisphere_images_urls} 

    browser.quit()
    return mars_dict















