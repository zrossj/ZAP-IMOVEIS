import re
from bs4 import BeautifulSoup





def scrape_listed_re(catalog_html_text) -> dict: 

    catalog_html_content = BeautifulSoup(catalog_html_text, 'html.parser')
    obj_list = catalog_html_content.find_all('a', class_= re.compile('ListingCard_result-card'))

    keys = ['link', 'data-id']
    dc = {}
    
    for obj in obj_list:
        
        link = obj['href'] 
        key_id =  obj['data-id']
        
        dc[key_id] = {'link': link}
        

    return dc