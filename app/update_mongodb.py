    
from pymongo import MongoClient
import datetime as dt
import numpy as np

client = MongoClient()
db = client.zap_imoveis

docs = db.bronze.find({}) # get all the docs of collection `zap`
ids = {doc.get('data-id') for doc in docs}
    
# Creating Collection
try:
    db.create_collection("bronze")

except Exception as e:
    print(f'{e}')


def update_mongodb(dc: dict, ids = ids):

    data_id = dc['data-id']
    date_of_scrap = dt.date.today().strftime('%Y%m%d')


    if not data_id in ids:
        
        # insert in the main db
        result = db.bronze.insert_one(dc)

        # insert in the historical db;
        new_doc = {}
        new_doc['data_id'] = dc.pop('data-id')
        date = dc.pop('date')
        new_doc['atts'] = {date : dc.get('atts')}
        db.bronze_historical.insert_one(new_doc)
 

        print('not found in data base - insert now')

        return result
    

    elif db.bronze.find_one({'data-id': data_id}).get('atts') != dc.get('atts'):    # checks if the newly scrape data have any changes in comparission with the pre stored. If so, it will be updated and registered; 
        
        # assert for 
        assert dc.get('atts').get('floorSize') != np.nan 


        result = db.bronze.replace_one({'data-id': data_id}, dc)
        

        # storing a copy  in the historical if any changes were detected within the attributes (like price)
        
        db.bronze_historical.update_one(
            {'data_id': data_id}, 
            {'$set': {
                f"atts.{dc.pop('date')}": dc.pop('atts')
                }
            }
        )

        print('found in database with changes - updating')
        return result

    else:

        print('Found in database but identically - passing')
        return 'Neither new or modified in this listing'

        
    

