from app.catalog_page_scraper import catalog_page_scraper as scraper
from app.transform_scraped_data import Transform
import pandas as pd


data_cole  =[]

for i in range(1,10):

    data = scraper(str(i))
    data_cole.append(data)
    


df = pd.DataFrame()

k = 0
for data in data_cole:
    trf = Transform(data = data)
    temp_df = trf.transform()
    
    if temp_df == False:
        # No reason to keep iterating over. Probably the search got to a end and returned an API error.
        break

    temp_df['page_n'] = k
    df = pd.concat([df, temp_df])
    k+=1

df = df.reset_index(drop = True)