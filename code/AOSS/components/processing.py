from AOSS.structure.shopping import Product, RegisteredProduct, ProductCategory, MarketHub
from AOSS.components.search import ProductMatcher
from typing import List
from config_paths import *
from AOSS.other.exceptions import InvalidFileFormatError
from AOSS.other.regex_utils import extract_words
import csv
import time
import pandas as pd
import polars as pl
from datetime import datetime


PRICE_APPROXIMATION_SIGN = '~'
CURRENCY_SIGN='€'


def process_scraped_products(products: (list[tuple[str, str, str]] | tuple[str, str, str]),
                              substition: (list[tuple[str, str]] | tuple[str, str]) = (',', '.')):

    if isinstance(products, list):
        results: List[Product] = []

        for name, price, category, market_ID in products:
            
            if isinstance(substition, list):

                for subst in substition:
                    name = name.replace(subst[0], subst[1])
                    price = price.replace(subst[0], subst[1])
            elif isinstance(substition, tuple):
                name = name.replace(substition[0], substition[1])
                price = price.replace(substition[0], substition[1])

            approximation = 0

            if price is None or not price:
                continue

            # Here we check whether theprice is just an approximate value
            if(price[0] == PRICE_APPROXIMATION_SIGN):
                price = price[1:]
                approximation = 1

            # We remove the potential price approximation sign from the price text
            price = price.split(CURRENCY_SIGN)[0].strip()

            results.append(Product(
                name=name,
                price=float(price),
                approximation=approximation,
                category=category,
                created_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                updated_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            )
        
        return results
    elif isinstance(products, tuple):
        name, price, category, market_ID = products

        if isinstance(substition, list):

            for subst in substition:
                name = name.replace(subst[0], subst[1])
                price = price.replace(subst[0], subst[1])
        elif isinstance(substition, tuple):
            name = name.replace(substition[0], substition[1])
            price = price.replace(substition[0], substition[1])

        approximation = 0

        # Here we check whether the price is just an approximate value
        if(price[0] == PRICE_APPROXIMATION_SIGN):
            price = price[1:]
            approximation = 1

        # We remove the potential price approximation sign from the price text
        price = price.split(CURRENCY_SIGN)[0].strip()

        return Product(name=name, price=float(price), approximation=approximation, category=products[2],
                       created_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                       updated_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    else:
        raise TypeError("Unsupported type of products variable!") 

def process_product(product: Product):
    product.name = product.name.replace(',', '.')
    product.normalized_name = product.normalized_name.replace(',', '.')


class ProductCategorizer:

    @staticmethod
    def categorize_by_mapping(product: Product, mappings_file: str, header: bool = False):
        """
            This function categorizes a product manually based on category mapping in a file. This is especially useful for
            categorizing training market's products.

            It searches the provide custom-mapping file and if it contains a mapping for the product's category it attempts to
            find a normalized category. 
        """

        category_ID = -1

        with open(file=mappings_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            if header:
                next(reader)
            


            for row in reader:
                if row[CATEGORY_MAP_FILE['columns']['name']['index']] == product.category:

                    category_ID = int(row[CATEGORY_MAP_FILE['columns']['category_ID']['index']])
                    break
            else:
                raise ValueError("There is no mapping for the specified category!")
            

        with open(file=CATEGORY_FILE['path'], mode='r', encoding='utf-8') as file:
            
            line = file.readline()

            if len(line.split(CATEGORY_FILE['delimiter'])) != len(CATEGORY_FILE['columns']):
                raise InvalidFileFormatError("File contains invalid amount of columns!")

            if line is not None and CATEGORY_FILE['header']:
                line = file.readline()

            while line:
                
                attributes = line.split(CATEGORY_FILE['delimiter'])

                if int(attributes[CATEGORY_FILE['columns']['ID']['index']]) == category_ID:
                    return ProductCategory(value=category_ID)
                    #returnproduct 

                line = file.readline()
            else:
                raise ValueError("Target category is not found!")


    def __init__(self, market_hub: MarketHub) -> None:
        if not market_hub.can_categorize():
            raise ValueError("""Cannot categorize product because training market is unspecified or contains no data for one of
                         its categories!""")
        
        self.__market_hub = market_hub
        self.__training_market = self.__market_hub.training_market()


    def categorize(self, product: Product):
        """
            This function categorizes a product based on the training market's product categories in the provided market hub.
            It uses a ProductMatcher object to find the best match for the product in the training market product dataset.

            To be able to categorize a product successfully, following must be met:

                a) Provided market must contain a training market

                b) Training market must provide at least one product for each of its categories
            
            Otherwise ValueError exception is thrown.
        """

        # if not market_hub.can_categorize():
        #     raise ValueError("""Cannot categorize product because training market is unspecified or contains no data for one of
        #                     its categories!""")
        
        
        matcher = ProductMatcher(market_hub=self.__market_hub)

        match = matcher.match(text=product.normalized_name, markets=(self.__training_market.ID(),), limit=1, min_match=0)
        

        product_match = self.__training_market.get_product(ID=match[0][0])

        #match = matcher.match(text=modified_name, category=None, min_match=0, limit=1, markets=market_hub.training_market().ID())

        return product_match.normalized_category
    
        #    product.normalized_category = product.normalized_category
    
    def __function(self, element, matcher: ProductMatcher):
        
        # start = time.time()

        # #return ProductCategory.NEURČENÁ.name
        # name=  self.__market_hub.training_market().get_product(
        #     ID=matcher.match(element, markets=(2,), limit=1)[0][0]).normalized_category.name

        # end = time.time()

        # print(f"time: {end - start}")
        return ProductCategory.NEURČENÁ.name

    def categorize_all(self):
        df = pd.read_csv(PRODUCT_FILE['path'])

        df.to_hdf(ALL_DATA_FILE['path'], key='products', mode='w')
        print(f"len before: {len(df)}")

        matcher = ProductMatcher(market_hub=self.__market_hub)

        df = pd.read_hdf(ALL_DATA_FILE['path'], key='products')
        print(df)


        mask = (df['market_ID'] == 1)

        df.loc[mask, 'category'] = df.loc[mask, 'normalized_name'].apply(
            lambda x: self.__function(element=x, matcher=matcher)
        )



        print(df[df['market_ID'] == 1][['normalized_name', 'category']].head(20) )


        # Write the updated DataFrame back to HDF5 file
        df.to_hdf(ALL_DATA_FILE['path'], key='products', mode='w')
        
        df = pd.read_hdf(ALL_DATA_FILE['path'], key='products')
        print(f"len after: {len(df)}")








def category_details(category: str):

    with open(CATEGORY_FILE['path'], 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Assuming the first row contains headers

        if CATEGORY_FILE['header']:
            next(csv_reader)
        
        # Reading the rest of the rows
        for row in csv_reader:
            # Accessing columns by index
            if row[CATEGORY_FILE['columns']['name']['index']] == category:
                return row[CATEGORY_FILE['columns']['details']['index']]
        
    return None