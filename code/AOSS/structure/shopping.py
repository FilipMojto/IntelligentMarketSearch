# shopping.py

"""
    This module defines fully implemented user interface when it comes to online shopping. It provides some general functions for working
    with markets and classes which define further structure and compatibility.

    Functions:
        market()
        markets()
        are_compatible()

    Classes:
        Product
        Market
        ProductCategory
"""

__ALL__ = ['market', 'markets', 'are_compatible', 'Product', 'Market', 'ProductCategory']
__AUTHOR__ = "Evening Programmer"
__VERSION__ = "1.0.0"

from typing import List
import threading
from AOSS.other.utils import PathManager
from enum import Enum
from config_paths import *
import csv
from dataclasses import dataclass, KW_ONLY
import time
from datetime import datetime



class ProductCategory(Enum):
    NEURČENÁ = 0
    OVOCIE_ZELENINA = 1
    PECIVO = 2
    MASO_MRAZENE_VYROBKY = 3
    UDENINY_NATIERKY_PASTETY = 4
    MLIECNE_VYROBKY = 5
    TRVANLIVE_POTRAVINY_VAJCIA = 6
    SLADKOSTI = 7
    SLANE_SNACKY_SEMIENKA = 8
    NEALKOHOLICKE_NAPOJE = 9
    TEPLE_NAPOJE = 10
    ALKOHOL = 11
    ZDRAVE_POTRAVINY = 12
    HOTOVE_INSTANTNE = 13
    

@dataclass
class Product:
    """
        This class represents a single Product object. It is a data class which should provide a
        convenient way of storing information about products  during program runtime.
        
        Attributes:
            a) ID (unsigned int) - unique identifier within the market which possess the product

            b) name (string) - unique name identifier of a product

            c) price (float) - decimal number representing the price of a product 

            d) approximation (bool) - flag indicating whether price is just an approximation

            e) category (string) - one of the possible categories

            f) hash (string) - hashed name attribute using sha256 - Removed

            g) market_ID (unsigned int) - unique identifier of a market which possess the product, -1 if not possessed by any market
    """

    ATTRIBUTE_COUNT = 9

    # --- Product File Configuration --- #

    # __PF_ID_INDEX = 0
    # __PF_NAME_INDEX = __PF_ID_INDEX + 1
    # __PF_PRICE_INDEX = __PF_NAME_INDEX + 1
    # __PF_APPROXIMATION_INDEX = __PF_PRICE_INDEX + 1
    # __PF_CATEGORY_INDEX = __PF_APPROXIMATION_INDEX + 1
    # __PF_MARKET_ID_INDEX = __PF_CATEGORY_INDEX + 1

    # __PF_ATTR_DELIMITER = ','
    __PF_ROW_DELIMITER = '\n'

    # def PF_ID_INDEX():
    #     return Product.__PF_ID_INDEX
    
    # def PF_NAME_INDEX():
    #     return Product.__PF_NAME_INDEX
    
    # def PF_PRICE_INDEX():
    #     return Product.__PF_PRICE_INDEX
    
    # def PF_APPROXIMATION_INDEX():
    #     return Product.__PF_APPROXIMATION_INDEX
    
    # def PF_CATEGORY_INDEX():
    #     return Product.__PF_CATEGORY_INDEX
    
    # def PF_MARKET_ID_INDEX():
    #     return Product.__PF_MARKET_ID_INDEX
    
    # def PF_ATTR_DELIMITER():
    #     return Product.__PF_ATTR_DELIMITER
    
    def PF_ROW_DELIMITER():
        return Product.__PF_ROW_DELIMITER

    @staticmethod
    def to_obj(row: str):
        
        attributes = row.split(PRODUCT_FILE['delimiter'])

        if len(attributes) != Product.ATTRIBUTE_COUNT:
            raise ValueError("Provided row contains invalid amount of attributes!")

        return Product(#ID=int(attributes[Product.__PF_ID_INDEX]),
                       name=attributes[PRODUCT_FILE['columns']['name']['index']],# Product.__PF_NAME_INDEX],
                       price=float(attributes[ PRODUCT_FILE['columns']['price']['index']]),# Product.__PF_PRICE_INDEX]),
                       approximation=int(attributes[PRODUCT_FILE['columns']['approximation']['index']]),# Product.__PF_APPROXIMATION_INDEX]),
                       category=attributes[PRODUCT_FILE['columns']['query_string']['index']],# Product.__PF_CATEGORY_INDEX],
                      normalized_category=ProductCategory[attributes[PRODUCT_FILE['columns']['category']['index']]],
                      # market_ID=int(attributes[Product.__PF_MARKET_ID_INDEX]),
                       created_at=attributes[PRODUCT_FILE['columns']['created_at']['index']],#datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                        updated_at=attributes[PRODUCT_FILE['columns']['updated_at']['index']]#datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
                        )
    name: str
    _: KW_ONLY
    price: float = -1
    approximation: int = -1
    category: str = "unspecified"
    normalized_category: ProductCategory = ProductCategory.NEURČENÁ
    created_at: str
    updated_at: str



@dataclass
class RegisteredProduct(Product):

    ID: int
    market_ID: int
    _: KW_ONLY
    standardized_category: ProductCategory = ProductCategory.NEURČENÁ
    




# def __to_obj(attributes: List[str], market_file: str, MF_header: bool = False):
#     categories = set()

#     with open(file=attributes[MARKET_FILE['columns']['category_file']['index']].rstrip(), mode='r', encoding='utf-8') as file:
#         line = file.readline()
        
#         if line is not None and int(attributes[MARKET_FILE['columns']['category_file_header']['index']]):
#             line = file.readline()

#         while line:
            
#             c_attributes = line.split(sep=Market.CF_ATTR_DELIMITER())
            
#             if c_attributes[Market.CF_MARKET_ID()].rstrip() == attributes[MARKET_FILE['columns']['ID']['index']]:
#                 categories.add(c_attributes[Market.CF_URL_NAME_INDEX()])

#             line = file.readline()
            
#     return Market(  ID=int(attributes[MARKET_FILE['columns']['ID']['index']]),
#                     name=attributes[MARKET_FILE['columns']['name']['index']],
#                     store_name=attributes[MARKET_FILE['columns']['store_name']['index']],
#                     #product_ID=int(attributes[MF_NEXT_PRODUCT_INDEX]),
#                     categories=tuple(categories),
#                     market_file=(market_file, MF_header),
#                     product_file=(attributes[MARKET_FILE['columns']['product_file']['index']], bool(int(attributes[MARKET_FILE['columns']['PF_header']['index']]))),
#                     #hash_file=(attributes[MF_HASH_FILE_INDEX], bool(int(attributes[MF_HF_HEADER_INDEX]))),
#                     category_file=(attributes[MARKET_FILE['columns']['category_file']['index']], bool(int(attributes[MARKET_FILE['columns']['CF_header']['index']]))))







        

from abc import ABC, abstractmethod

class MarketHubInterface(ABC):
    @abstractmethod
    def can_register(self, market):
        pass             
    
    @abstractmethod
    def get_product_ID(self, market):
        pass
        

class MarketView:
    
    def __init__(self, ID:int, name: str, store_name: str, product_file: tuple[str, bool],  category_file: tuple[str, bool]): #hash_file: tuple[str, bool], category_file: tuple[str, bool]):
        self.__ID = ID
        self.__name = name
        self.__store_name = store_name

        self.__product_file = product_file
        PathManager.check_if_exists(path=product_file[0], type='file')

        self.__category_file = category_file
        PathManager.check_if_exists(category_file[0], type='file')

        self.__categories: List[str] = []

        #we laod categories from provided file
        with open(file=self.__category_file[0], mode='r', encoding='utf-8') as file:

            reader = csv.reader(file)

            if self.__category_file[1]:
                next(reader)
            
            for row in reader:

                if int(row[CATEGORY_MAP_FILE['columns']['market_ID']['index']]) == self.__ID:
                    self.__categories.append(row[CATEGORY_MAP_FILE['columns']['name']['index']])

    def __str__(self):
        return f"{{ID: {self.__ID}, name: {self.__name}, store_name: {self.__store_name}, categories: {self.__categories}}}" + '\n'


    def ID(self):
        return self.__ID

    def name(self, name: str = None):
        if name is not None:
            self.__name = name
        else:
            return self.__name
    
    def store_name(self, name: str = None):
        if name is not None:
            self.__store_name = name
        else:
            return self.__store_name
    
    def categories(self) -> tuple[str]:
        return self.__categories
    

    def product_file(self):
        return self.__product_file
    
    def category_file(self):
        return self.__category_file

    
    def get_product(self, ID: int):

        with open(file=self.__product_file[0], mode='r', encoding='utf-8') as file:
            line = file.readline()

            while(line):
                attributes = line.split(sep=Product.PF_ATTR_DELIMITER())

                if attributes[Product.PF_ID_INDEX()] == str(ID) and self.__ID == int(attributes[Product.PF_MARKET_ID_INDEX()]):
                    
                    return Product.to_obj(row=line)

                line = file.readline()
            

        
        return None

    
    
# --- Market - Class Declaration&Definition --- #

class Market(MarketView):
    
    


    def __init__(self, ID: int, name: str, store_name: str, market_hub: MarketHubInterface,
                 product_file: tuple[str, bool], category_file: tuple[str, bool], buffer: int = 1000) -> None:
        super().__init__(ID=ID, name=name, store_name=store_name, product_file=product_file, category_file=category_file)

        # --- Market Attributes --- #
        self.__ID = ID
        self.__market_hub = market_hub
     

        # --- Market Product Registration Attributes --- #

        self.__registration_buffer: List[Product] = []
        self.__buffer_limit = buffer
        self.__buffer_lock = threading.Lock()

        
    

   
        
    #def __repr__(self):
        #return f"Market(ID: {self.__ID}, name: {self.__name}, store_name: {self.__store_name}, roduct_ID: {self.__product_ID}, categories: {self.__categories})"

    def ID(self) -> int:
        return self.__ID


    
    def buffer(self, size: int):
        with self.__buffer_lock:
            self.__buffer_limit = size



    def for_registration(self, product: Product):

        with self.__buffer_lock:
            # Let's firstly check the unregistered products to prove product's uniqueness
            for _product in self.__registration_buffer:
                if (product.name == _product.name):
                    raise ValueError("Conflicting name with an unregistered product!")
            
            # Now we check the registered products for the same purpose
            
            with open(self.product_file()[0], mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)

                if self.product_file()[1]:
                    next(reader)
                
                for row in reader:

                    if (int(row[PRODUCT_FILE['columns']['market_ID']['index']]) == self.__ID and
                        row[PRODUCT_FILE['columns']['name']['index']] == product.name):
                        raise ValueError("Conflicting name with a registered product!")
                

            # here we verify the category of the product, whether the market provides it
            with open(self.category_file()[0], mode='r', encoding='utf-8') as categories_f:
                line = categories_f.readline()

                if line is not None and self.category_file()[1]:
                    line = categories_f.readline()

                while line:
                    attributes = line.split(CATEGORY_MAP_FILE['delimiter'])

                    if (product.category == attributes[CATEGORY_MAP_FILE['columns']['name']['index']]):
                        break
  
                    line = categories_f.readline()
                else:
                    raise ValueError("The market doesn't provide such a category.")

            # Finally, we can add the product for registration
            self.__registration_buffer.append(product)
        
            if len(self.__registration_buffer) >= self.__buffer_limit:
                self.register_products()
    


    def register_products(self):


        with open(self.product_file()[0], 'a', encoding='utf-8') as file:
            for product in self.__registration_buffer:
                id = self.__market_hub.get_product_ID(market=self)
                file.write(str(id) + PRODUCT_FILE['delimiter'] +
                           product.name + PRODUCT_FILE['delimiter'] +
                           str(product.price) + PRODUCT_FILE['delimiter'] +
                           str(int(product.approximation)) + PRODUCT_FILE['delimiter'] +
                           product.normalized_category.name + PRODUCT_FILE['delimiter'] +
                           product.category + PRODUCT_FILE['delimiter'] +
                           str(self.__ID) + PRODUCT_FILE['delimiter'] +
                           product.created_at + PRODUCT_FILE['delimiter'] +
                            datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\n')
        
        self.__registration_buffer.clear()






class MarketHub(MarketHubInterface):
    ATTR_DELIMITER = ','

    def __init__(self, src_file: str, header: bool = False, create_files: bool = False) -> None:
        self.__create_files = create_files
        
        if not self.__create_files:
            self.__src_file = PathManager.check_if_exists(path=src_file, type='file')
        else:
            self.__src_file = PathManager.make_if_not_exists(path=src_file, type='file')

        self.__src_file_header = header
        
        with open(file=src_file, mode='r') as file:
            
            line = file.readline()

            if line is not None and  self.__src_file_header:
                line = file.readline()

            
            attributes = line.split(sep=self.ATTR_DELIMITER)

            self.__market_ID: int = int(attributes[MARKET_HUB_FILE['columns']['market_ID']['index']])
            self.__product_ID: int = int(attributes[MARKET_HUB_FILE['columns']['product_ID']['index']])
            self.__training_market: Market = None
            self.__market_file = attributes[MARKET_HUB_FILE['columns']['market_file']['index']]
            self.__MF_header = int(attributes[MARKET_HUB_FILE['columns']['market_file_header']['index']])
            
        self.__markets: List[Market] = []


    def __enter__(self):
        print("Loading markets from a file...")
        self.load_markets()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Updating hub stats to file...")
        self.update()

    
    def product_file(self):
        return self.__product_file

    def update(self):
        rows: List[str] = []

        with open(self.__src_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            
        
        row = rows[0] if not self.__src_file_header else rows[1]

        row[MARKET_HUB_FILE['columns']['market_ID']['index']] = self.__market_ID
        row[MARKET_HUB_FILE['columns']['product_ID']['index']] = self.__product_ID


        with open(file=self.__src_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        
        print("Data updated successfully!")

    def __get_market_ID(self):
        old_val = self.__market_ID
        self.__market_ID += 1
        return old_val

    def get_product_ID(self, market: Market):
        
        for market in self.__markets:
            if market.ID() == market.ID():
                old_value = self.__product_ID
                self.__product_ID += 1
                return old_value
            
        return -1
            

    def load_markets(self):    
        
        with open(file=self.__market_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            if self.__MF_header:
                next(reader)

            header_row = next(reader)

            if not self.__create_files:
                self.__product_file = PathManager.check_if_exists(path=header_row[MARKET_FILE['columns']['product_file']['index']],
                                                                type='file')

                self.__categories_file = PathManager.check_if_exists(path=header_row[MARKET_FILE['columns']['category_file']['index']],
                                                                    type='file')
            else:
                self.__product_file = PathManager.make_if_not_exists(path=header_row[MARKET_FILE['columns']['product_file']['index']],
                                                                type='file')

                self.__categories_file = PathManager.make_if_not_exists(path=header_row[MARKET_FILE['columns']['category_file']['index']],
                                                                    type='file')
        

        with open(file=self.__market_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            if self.__MF_header:
                next(reader)


            for row in reader:
                
                market_base = MarketView(
                    ID=int(row[MARKET_FILE['columns']['ID']['index']]),
                    name=row[MARKET_FILE['columns']['name']['index']],
                    store_name=row[MARKET_FILE['columns']['store_name']['index']],
                    
                    product_file= (row[MARKET_FILE['columns']['product_file']['index']] , row[MARKET_FILE['columns']['PF_header']['index']]),
                    category_file=(row[MARKET_FILE['columns']['category_file']['index']], row[MARKET_FILE['columns']['CF_header']['index']])
                )

               
                market = Market(
                    name=market_base.name(),
                    store_name=market_base.store_name(),
                    
                    product_file=market_base.product_file(),
                    category_file=market_base.category_file(),

                    ID=market_base.ID(),
                    market_hub=self
                )

                if self.can_register(market=market):

                    print(f"Market: {str(market)} loaded successfully!")

                    self.__markets.append(market)
                else:
                    print(f"Market: {repr(market_base)} cannot be loaded!")
        
        with open(file=self.__src_file, mode='r', encoding='utf-8') as file:
            line = file.readline()

            if self.__src_file_header:
                line = file.readline()

            training_m_ID = int(line.split(MARKET_HUB_FILE['delimiter'])[MARKET_HUB_FILE['columns']['training_market']['index']])

            for market in self.__markets:
                if market.ID() == training_m_ID:
                    self.__training_market = market
                    break
            

    def training_market(self):
        return self.__training_market


    def can_register(self, market: Market) -> bool:
        if (self.__product_file != market.product_file()[0] or self.__categories_file
                  != market.category_file()[0]): #or self.__hash_file != market.hash_file()[0]):
            return False
        
        for __market in self.__markets:

            if __market.store_name() == market.store_name() or __market.ID() ==market.ID():
                return False

        return True    
        


    def market(self, ID: int):
        
        for market in self.__markets:
            if market.ID() == ID:
                return market
            
        return None



    def markets(self):
        return tuple(self.__markets)
    
                    


if __name__ == "__main__":

    product = Product(name="Hrusky zelene", price=1.23, approximation=0, category="ovocie&zelenina")
    product.__str__()

