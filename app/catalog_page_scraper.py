from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import logging
import numpy as np



def catalog_page_scraper(start_page: int, last_page = None):

    if last_page == None:
        last_page = start_page
    



    dc_pages_html_content = {}
    for page_num in range(start_page, last_page+1):
        
        # IMPORTANT! Define the max floor_size for your scrape here, on the pace variable. 
        
        pace = np.arange(0, 400, 100)
        bins = list(zip(pace[:-1], pace[1:]))
        page_content_bybin = []
        
        for min_m2, max_m2 in bins:
            
            
            
            # we filtered for obtain only non comercial places. 
            
            url = f"https://www.zapimoveis.com.br/aluguel/apartamentos/sp+sao-paulo/?transacao=aluguel&onde=,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,city,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,-23.532633,-46.791524,&tipos=apartamento_residencial,studio_residencial,kitnet_residencial,casa_residencial,sobrado_residencial,condominio_residencial,casa-vila_residencial,cobertura_residencial,flat_residencial,loft_residencial,granja_residencial&pagina={page_num}&areaMinima={str(min_m2)}&areaMaxima={str(max_m2)}&ordem=Maior área"


            # setting webdriver;
            options = Options()
            #options.add_argument("-headless")  
            driver = webdriver.Firefox(options=options)
            driver.get(url)


            # loading page's content bloc
            for i in range(10):
                t1 = driver.page_source
                all_obj = BeautifulSoup(t1, 'html.parser').find_all('a', class_= re.compile('ListingCard_result-card'))
                
                try:
                    last_obj = all_obj[-1].parent.parent.attrs
                    css_key = list(last_obj.keys())[0]
                    ccs_val = last_obj[css_key]

                    # select and scroll to it
                    last_on_page =  driver.find_element(By.CSS_SELECTOR, f'div[{css_key}="{ccs_val}"]')
                    driver.execute_script("arguments[0].scrollIntoView();", last_on_page)
                    time.sleep(1)
                except: 
                    None

            page_html = driver.page_source # now gets all the html code;
            page_content_bybin.append(page_html)
            
            driver.close() # otherwise will consume memory;


        dc_pages_html_content[page_num] = '\n'.join(page_content_bybin)
   
    return  dc_pages_html_content
