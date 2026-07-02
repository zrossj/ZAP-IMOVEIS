#%%
import logging
from curl_cffi import requests as r


logger = logging.getLogger(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO, format="%(asctime)s [%(levelname)s] (%(filename)s)")


## The cap for the backend is a maximum Offset of 10.000. Using 30 per page, you can't go longer than 333 pages.



def catalog_page_scraper(page_num: str, price_min: int, price_max: int):

    """
    variables: page_num (str): set the page number of the search that you want to scrape. offset (str): equals the offset to listed itens based on pagination. 
    
    
    """
    logger.info('requesting data from the given url')

    # basic parameters
    offset = (page_num - 1) * 30
    base_url = f"""https://glue-api.zapimoveis.com.br/v4/listings?user=00473d9f-8471-48dd-b66f-60324d83ec36&portal=ZAP&includeFields=fullUriFragments%2Cpage%2Csearch%28result%28listings%28listing%28expansionType%2CcontractType%2ClistingsCount%2CpropertyDevelopers%2CsourceId%2CdisplayAddressType%2Camenities%2CusableAreas%2CconstructionStatus%2ClistingType%2Cdescription%2Ctitle%2Cstamps%2CcreatedAt%2Cfloors%2CunitTypes%2CnonActivationReason%2CproviderId%2CpropertyType%2CunitSubTypes%2CunitsOnTheFloor%2ClegacyId%2Cid%2Cportal%2Cportals%2CunitFloor%2CparkingSpaces%2CupdatedAt%2Caddress%2Csuites%2CpublicationType%2CexternalId%2Cbathrooms%2CusageTypes%2CtotalAreas%2CadvertiserId%2CadvertiserContact%2CwhatsappNumber%2Cbedrooms%2CacceptExchange%2CpricingInfos%2CshowPrice%2Cresale%2Cbuildings%2CcapacityLimit%2Cstatus%2CpriceSuggestion%2CcondominiumName%2Cmodality%2CenhancedDevelopment%29%2Caccount%28id%2Cname%2ClogoUrl%2ClicenseNumber%2CshowAddress%2ClegacyVivarealId%2ClegacyZapId%2CcreatedDate%2Ctier%2CtrustScore%2CtotalCountByFilter%2CtotalCountByAdvertiser%29%2Cmedias%2CaccountLink%2Clink%2Cchildren%28id%2CusableAreas%2CtotalAreas%2Cbedrooms%2Cbathrooms%2CparkingSpaces%2CpricingInfos%29%29%29%2CtotalCount%29&categoryPage=RESULT&business=RENTAL&sort=LOWEST_PRICE&parentId=null&listingType=USED&__zt=mtc%3Adeduplication2023&priceMin={price_min}&priceMax={price_max}&addressCity=S%C3%A3o+Paulo&addressZone=&addressStreet=&addressLocationId=BR%3ESao+Paulo%3ENULL%3ESao+Paulo&addressState=S%C3%A3o+Paulo&addressNeighborhood=&addressPointLat=-23.555771&addressPointLon=-46.639557&addressType=city&unitTypes=APARTMENT%2CAPARTMENT%2CAPARTMENT%2CHOME%2CHOME%2CHOME%2CHOME%2CAPARTMENT%2CAPARTMENT%2CAPARTMENT&unitTypesV3=APARTMENT%2CSTUDIO%2CKITNET%2CHOME%2CTWO_STORY_HOUSE%2CCONDOMINIUM%2CVILLAGE_HOUSE%2CPENTHOUSE%2CFLAT%2CLOFT&unitSubTypes=UnitSubType_NONE%2CDUPLEX%2CTRIPLEX%7CSTUDIO%7CKITNET%7CUnitSubType_NONE%2CTWO_STORY_HOUSE%2CSINGLE_STOREY_HOUSE%2CKITNET%7CTWO_STORY_HOUSE%7CCONDOMINIUM%7CVILLAGE_HOUSE%7CPENTHOUSE%7CFLAT%7CLOFT&usageTypes=RESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL%2CRESIDENTIAL&page={page_num}&size=30&from={offset}&images=webp"""
    
    data = r.get(base_url, impersonate="chrome101", headers = {'x-domain': '.zapimoveis.com.br'})

    logger.info(f"request status_code: {data.status_code}")
    #logger.info(f"total listings for this search: {data.json()['search']['totalCount']}")


    return  data.json()

# %%
