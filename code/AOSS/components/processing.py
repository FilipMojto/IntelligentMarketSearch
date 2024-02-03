from AOSS.structure.shopping import Product, ProductCategory, MarketHub
from AOSS.components.search import ProductMatcher
from typing import List
from config_paths import *
from AOSS.other.exceptions import InvalidFileFormatError
import csv
import time
from datetime import datetime

PRICE_APPROXIMATION_SIGN = '~'
CURRENCY_SIGN='€'


def process_scraped_products(products: (list[tuple[str, str, str]] | tuple[str, str, str]),
                              substition: (list[tuple[str, str]] | tuple[str, str]) = (',', '.')):

    if isinstance(products, list):
        results: List[Product] = []

        for name, price, category in products:
            
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

def categorize_product(product: Product, market_hub: MarketHub):


    matcher = ProductMatcher(market_hub=market_hub, buffer_limit=500)
    match = matcher.match(text=product.name, category=None, min_match=0, limit=1, markets=market_hub.training_market().ID())

    product.normalized_category = match[0][0].normalized_category

    #print(match[0][0])




def categorize_manually(product: Product, categories_file: str, header: bool = False):
    category_ID = -1

    with open(file=categories_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)

        if header:
            next(reader)
        


        for row in reader:
            if row[QUERY_STRING_FILE['columns']['name']['index']] == product.category:

                category_ID = int(row[QUERY_STRING_FILE['columns']['category_ID']['index']])
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
                product.normalized_category = ProductCategory(value=category_ID)
                return product 

            line = file.readline()
        else:
            raise ValueError("Target category is not found!")


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