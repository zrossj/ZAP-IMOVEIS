Projeto de Webscraping no ZapImoveis

O Objetivo deste projeto é de treinar as skills de webscraping e análise de dados, gerando métricas a respeito do aluguel de imóveis na cidade de São Paulo-SP. 
Além disso, treinar abilidades no uso de tecnologias de DataScience como: 

* MongoDB (para armazenar os dados no formato html);
* Postgre para os dados formatados em tabelas;
* Airflow - para orchestração do webscraping e armazenamento;

Outras tecnologias passíveis de uso: 
* Tableau
* DBT
* scikit-learn
* Spark


Data Visualization with Tableau Public: https://public.tableau.com/app/profile/john.zwarg/viz/zapimoveisproject-rentandsaleprice/ds_prices?publish=yes (the project file is also available in the main folder)



HOW TO RUN: 

1. Setup the profiles.yml needed for DBT use (please read the documentation from https://docs.getdbt.com/docs/get-started-dbt); 
2. Setup the app.properties file (here, you need only to declare 1 line as follow -> uri = database_connection_string. This will be used as a variable for SqlAlchemy connection with DB)
3. Run pip -r install requirements.txt
4. Execute the cells in the notebook "WebScrapZap.ipynb"
