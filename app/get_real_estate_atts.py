from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import datetime as dt
import logging


def get_re_atts(listed_id, listing: dict):

    # 1. get the data on the imovel's own page.
    
    try:

        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(listing['link'])
        imovel_data = driver.page_source

        driver.close()
        

    except Exception as e:

        print(f"Ops, broke. {e}")
        return listing['link']
        

    # gets the relevant html data.
    soup = BeautifulSoup(imovel_data, 'html.parser')


    ## atts
    price_atts= {}
    att_dc = {}
    listing['data-id'] = listed_id
    

    # price, condominal price, address location and type of ad.

    try:
            
        prices = list(soup.find('div', {'class': 'price-value-wrapper'}).children)[0].find_all('p')
        for i in range(0, len(prices), 2):

            price_key = prices[i].text
            value = prices[i+1].text
            price_atts[price_key] = value

        rent_price = price_atts.get('Aluguel')
        sell_price = price_atts.get('Venda')
        condo_price = soup.find(id='condo-fee-price')
        ad_type = soup.find('p', {'id': 'business-type-info'})
        address = soup.find_all('div', {'class':"address-info-wrapper"})[0].find('p', {'data-testid': "address-info-value"})
        rstate_type = soup.find('li', {'class': 'l-breadcrumb__item'})
        
        for var_key, var in zip(
            ['ad_type', 'sell_price','rent_price', 'condo_price', 'address', 'rstate_type'], 
            [ad_type, sell_price, rent_price, condo_price, address, rstate_type]):

            try:
                att_dc[var_key] = var.text
        
            except:
                att_dc[var_key] = var
                
    except Exception as e: 
        logging.info(f'{e}\n\n\n{imovel_data}') # if error in scraping atts, save the html to log for debugging; 



    # HOUSE ATTS (bathrooms, bedrooms, etc)
    amenities = soup.find_all('ul', {'class': "amenities-list"})

    try:
        for att in amenities[0].find_all('span', {'class':"amenities-item-text"}):
        
            att_dc[att.parent['itemprop']] = att.text

    except Exception as e:
        print(f'Atts were not scraped, error: {e} - id: {listed_id}')
        logging.info(f'Atts were not scraped, error: {e} - id: {listed_id}')

    
    listing['atts'] = att_dc

    # registering the date; 
    date_of_scrape = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    listing['date'] = date_of_scrape
       
        
    return listing
