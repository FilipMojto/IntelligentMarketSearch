from AOSS.structure.shopping import Product, ProductCategory, MarketHub
from AOSS.components.search import ProductMatcher
from typing import List
from config_paths import *
from AOSS.other.exceptions import InvalidFileFormatError
import csv
import time
import polars as pl
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
    """
        This function categorizes a product based on the training market's product categories in the provided market hub.
        It uses a ProductMatcher object to find the best match for the product in the training market product dataset.

        To be able to categorize a product successfully, following must be met:

            a) Provided market must contain a training market

            b) Training market must provide at least one product for each of its categories
        
        Otherwise ValueError exception is thrown.
    """

    training_market = market_hub.training_market()

    if training_market is None:
        raise ValueError("Cannot categorize product because provided market hub doesn't contain any training market!")
    else:
        product_df = pl.read_csv(market_hub.product_file())
        categories = training_market.categories()

        for category in categories:
            if len(product_df.filter((product_df['market_ID'] == training_market.ID()) &
                                     (product_df['query_string'] == category))) == 0:

                raise ValueError("Cannot categorize product because training market contains no data for one of its categories!")
    
    # After all requirements are met, we can categorize product by finding its best match within training dataset

    matcher = ProductMatcher(market_hub=market_hub, buffer_limit=500)
    match = matcher.match(text=product.name, category=None, min_match=0, limit=1, markets=market_hub.training_market().ID())

    product.normalized_category = match[0][0].normalized_category



def categorize_manually(product: Product, mappings_file: str, header: bool = False):

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