Projeto de Web scraping no Zap Imóveis
<br>
<br>
O Objetivo deste projeto é de aprimorar abilidades de web scraping e análise de dados, gerando métricas a respeito do setor imobiliário na cidade de São Paulo. 
Além disso, treinar a utilização das seguintes tecnologias:
<br>
* NoSQL (com MongoDB);
* PostgreSQL (RDB);
* Tableau
* DBT
* Selenium
* BeautifulSoup
<br>
<br>
<br>
**HOW TO RUN:**
<br>
<br>
<br>
1. Setup the profiles.yml needed for DBT use (read the documentation from https://docs.getdbt.com/docs/get-started-dbt); 
2. Setup the app.properties file (here, you need only to write 1 line as follow -> uri = database_connection_string. This will be used as a variable for SqlAlchemy connection with DB)
3. Install the libraries required (requirements.txt)
4. Make sure MongoDB service is running.
5. Execute the cells in the notebook "WebScrapZap.ipynb" --> set up how many pages you want to scrape per floor_size interval in the function 'catalog_page_scraper' and in catalog_page_scraper.py, respectively. This notebook will collect the data from the origin and store its raw data in MongoDB. 
6. Execute the notebook "DataExploration_SilverLayer" - this notebook will read the raw data, clean and transform producing a silver layer which will be stored in Postgres and used for our dashboard 
<br>
<br>
<br>
**Data Visualization with Tableau Public**
https://public.tableau.com/app/profile/john.zwarg/viz/zapimoveisproject-rentandsaleprice/ds_prices?publish=yes (the project file is also available in the main folder)
<br>
<br>
<br>
Below is a screenshot of the Tableau dashboard created for this project:
<br>
<br>
<br>
![tableau_project](https://github.com/user-attachments/assets/3b5df13d-1d69-4cc3-aa9a-68761aed5d52)
