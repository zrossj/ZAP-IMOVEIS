#%%
import re
from bs4 import BeautifulSoup


def scrape_listed_re(catalog_html_text) -> dict: 

    catalog_html_content = BeautifulSoup(catalog_html_text, 'html.parser')
    obj_list = catalog_html_content.find_all(
        lambda tag: tag.name == 'li' 
                    and tag.get('data-cy') == 'rp-property-cd' 
                    and tag.find('a', href=True)
    )

    keys = ['link', 'data-id']
    dc = {}

    for listed_obj in obj_list:
        
        fchild = list(listed_obj.children)[0]

        link = fchild['href'] 

        # regex to get id 
        key_id =  re.search('(?<=id-)\d+', link)
        if key_id:
            key_id = key_id.group()
        
        # include in dicionary
        dc[key_id] = {'link': link}
        

    return dc
# %%
