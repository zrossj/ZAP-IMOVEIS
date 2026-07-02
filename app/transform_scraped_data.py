import pandas as pd
import logging


logger = logging.getLogger(__name__)

logging.basicConfig(filename= 'app.log', level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(filename)s)")


class Transform:


    def __init__(self, data):

        self.data = data

        return None
        

    def _transf_normalize(self):

        """
        Receives the dictionary containing the data that was obtained directly from the API
        variables: data (dict)
        """
        try:
            self.df = pd.DataFrame(self.data['search']['result']['listings'])
        except Exception as e:
            logger.error(f"The page scrapped returned a different dict format. {e}")   
            return False
        

        self.df_normalized = pd.json_normalize(self.data['search']['result']['listings'])

        # NORMALIZING THE AMENITIES DATA

        transf_col = []
        for x in self.df_normalized['listing.amenities']:
            
            y = dict(zip(x, len(x) * [1]))
            transf_col.append(y)

        self.df_normalized = self.df_normalized.join(pd.DataFrame(transf_col).fillna(0))


        ### NORMALIZING PRICING INFO; 

        self.df_price = pd.json_normalize(self.df_normalized['listing.pricingInfos']) 
        # this assumes that the data will be at max two dicts - one for sale and one for rental.
        price1 = pd.json_normalize(self.df_price[0])
        
        try:
            price2 = pd.json_normalize(self.df_price[1])

        except Exception as e:
            price2 = pd.DataFrame() 
            logger.info(f'{e}')
        
        # need the following beceause its undetermined if df_price[0] is sale or rent
        self.df_price_mix = pd.concat(
            [price1, price2]
        ) 

        # get condo, iptu
        others_cols = ['yearlyIptu', 'monthlyCondoFee']
        cols_to_create = [col if not col in self.df_price_mix.columns else '' for col in others_cols]
        for col in cols_to_create:
            if col != '':
                self.df_price_mix[col] = None
        df_price_others = self.df_price_mix[others_cols]
        df_price_others = df_price_others[~df_price_others.index.duplicated()]

        # segregate them based on business type to join on rows; 
        df_rental = self.df_price_mix[self.df_price_mix.businessType == 'RENTAL'][['price']].rename(columns = {'price': 'price_rent'})   #duvida  - preciso por self. aqui? entender.
        df_sale = self.df_price_mix[self.df_price_mix.businessType == 'SALE'][['price']].rename(columns = {'price': 'price_sale'})

        self.df_price = df_price_others \
            .join(df_sale) \
            .join(df_rental) \
            .rename(columns = {
                'yearlyIptu': 'iptu', 
                'monthlyCondoFee': 'condo_fee'}
            )
  
        self.df_normalized = self.df_normalized.join(self.df_price)


        return self.df_normalized
    


    def _transform_slice(self):


        cols_of_interest = [
            'listing.createdAt', 
            'listing.unitTypes',
            'listing.id', 
            'listing.propertyType',
            'price_rent',
            'price_sale',
            'condo_fee',
            'iptu',
            'listing.parkingSpaces',
            'listing.address.zipCode', 
            'listing.address.city', 
            'listing.address.point.approximateLat', 
            'listing.address.point.approximateLon',
            'listing.address.zone', 
            'listing.address.street', 
            'listing.address.neighborhood', 
            'listing.suites', 
            'listing.bathrooms', 
            'listing.usageTypes', 
            'listing.usableAreas',
            'listing.bedrooms', 
            'link.href',
            'listing.address.streetNumber',
            'listing.address.point.lon',
            'listing.address.point.lat',
            'POOL',
            'FURNISHED',
            'GYM',
            'SAUNA'
            ]


        empty_df = pd.DataFrame(data = [len(cols_of_interest)*['-1']], columns = cols_of_interest)

        self.df_interest = pd.concat([empty_df, self.df_normalized], join = 'inner')
        self.df_interest = self.df_interest[self.df_interest['listing.propertyType'] != '-1']

        return self.df_interest
    
    def _transf_names(self):

        # RENAMING COLS

        new_names =  {
            'listing.createdAt': 'created_at', 
            'listing.unitTypes': 'kind', 
            'listing.propertyType': 'property_type',
            'listing.id': 'id',
            'listing.parkingSpaces': 'parking_spaces', 
            'listing.address.zipCode': 'zip_code', 
            'listing.address.point.approximateLat': 'approx_lat', 
            'listing.address.point.approximateLon': 'approx_lon',
            'listing.address.zone': 'zone',
            'listing.address.street': 'street',
            'listing.address.city': 'city',
            'listing.address.neighborhood': 'neighborhood',
            'listing.suites': 'suites',
            'listing.bathrooms': 'bathrooms',
            'listing.usageTypes': 'usage_types', 
            'listing.usableAreas': 'floor_size', 
            'listing.bedrooms': 'rooms',
            'link.href': 'link',
            'listing.address.streetNumber': 'address_number', 
            'listing.address.point.lon': 'lon', 
            'listing.address.point.lat': 'lat',
            'POOL': 'pool', 
            'FURNISHED': 'furnished', 
            'GYM': 'gym',
            'SAUNA': 'sauna',
            'price': 'price_rent',
            'condo_fee': 'price_condominium'
        }

        self.df_interest = self.df_interest.rename(columns = new_names)

        df = pd.DataFrame(columns = list(new_names.values()))
        self.df_interest = pd.concat([df, self.df_interest])
        
        return self.df_interest
    


    def _transf_arrayed_data(self):

        ### ARRAY DATA

        mask = self.df_interest.map(lambda x: isinstance(x, list)).sum() > 0

        self.columns_with_array = mask[mask ==True].index

        # its best to exclude those rows where is a announcement for a building instead of a single unit option (like its 3 or 4 bedrooms where area will vary)

        self.df_cols_w_array_len = self.df_interest[self.columns_with_array].map(lambda x: len(x))
        self.rows_w_array_to_drop = self.df_cols_w_array_len[self.df_cols_w_array_len >1].dropna(how = 'any').index


        if not self.rows_w_array_to_drop.empty:
            self.df_interest.drop(index = self.rows_w_array_to_drop)


        self.df_interest.loc[:, self.columns_with_array] = self.df_interest[self.columns_with_array].map(lambda x: x[0] if len(x) >0 else pd.NA)

        return self.df_interest
    

    def _transf_dtypes(self):


        ### DATETIME
        self.df_interest.loc[:, 'created_at'] = pd.to_datetime(self.df_interest.created_at).dt.date


        ### NA values in totalAreas. - if they dont show up the area, exclude; 

        self.df_interest = self.df_interest[~self.df_interest.floor_size.isna()]
        
        #self.df_interest = self.df_interest.fillna({'suites': '0'}) 

        self.df_interest = self.df_interest.map(lambda x: "" if len(str(x))==0 else x) # somehow a '' was not categorized as NA value. This fix this problem.


        ### INTEGERS;

        int_cols = ['parking_spaces', 'suites', 'bathrooms', 'rooms', 'address_number', 'pool', 'gym', 'sauna']
        
        for col in int_cols:
            self.df_interest[col] = pd.to_numeric(
                self.df_interest[col], errors= 'coerce'
            )

        ### FLOAT

        float_cols = 'price_rent', 'price_condominium', 'iptu', 'approx_lat', 'approx_lon', 'floor_size', 'lon', 'lat'
        self.df_interest.loc[:, float_cols] = self.df_interest.loc[:, float_cols].astype(float)


        return self.df_interest
    

    def _calculate_fields(self):



        self.df_interest['rent_plus_condo'] = self.df_interest.price_rent + self.df_interest.price_condominium
        self.df_interest['price_rent_per_m2'] = self.df_interest.price_rent / self.df_interest.floor_size

        # sale/m2
        self.df_interest['price_sale_per_m2'] = self.df_interest.price_sale / self.df_interest.floor_size

        # ranking floor size
        rank_over_floor_size = lambda x: "A" if x <=30 else "B" if x<=50 else "C" if x<=70 else "S"
        self.df_interest['floor_size_rank'] = self.df_interest.floor_size.map(rank_over_floor_size)


        return self.df_interest



    def transform(self):

        self._transf_normalize()
        self._transform_slice()
        self._transf_names()
        self._transf_arrayed_data()
        self._transf_dtypes()
        self._calculate_fields()

        return self.df_interest
    
