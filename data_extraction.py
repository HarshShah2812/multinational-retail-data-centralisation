import pandas as pd
from database_utils import DatabaseConnector
import json
import requests
import tabula

class DataExtractor:
    
    def __init__(self):
        self.connector = DatabaseConnector()
        # self.headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
       
    def read_rds_table(self, table_name):
        engine = self.connector.init_db_engine()
        df = pd.read_sql_table(table_name, engine, index_col = 'index')
        return df
    
    def retrieve_pdf_data(self, link):
        tab = tabula.read_pdf(link, pages = "all")
        df = pd.DataFrame(tab[0])
        return df
    
    def list_number_of_stores(self, headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
        num_of_store = requests.get('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', headers = headers)
        num_of_store = num_of_store.json()
        # print(num_of_store.status_code)
        print(num_of_store)
        return num_of_store
    
    def retrieve_stores_data(self, headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
        num_of_store = self.list_number_of_stores()
        num_of_store = num_of_store['number_stores']
        df = pd.DataFrame()
        # store_data = requests.get(f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/1', headers = headers)
        # print(store_data.status_code)
        # print(store_data.json())
        #store_list = []
        #store_number = 0
        for store_number in range(num_of_store):
            # store_number += 1
            store_data = requests.get(f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}', headers = headers)
            x = store_data.json()
            # print(x)
            df2 = pd.json_normalize(x)
            df = pd.concat([df, df2])
        
        #print(df.head(10))
            # dfs = pd.concat([df, dfs])
        # print(df)
        return df


if __name__ == "__main__":
    extractor = DataExtractor()
    # extractor.read_rds_table()
    # extractor.retrieve_pdf_data()
    extractor.list_number_of_stores()
    extractor.retrieve_stores_data()


    
