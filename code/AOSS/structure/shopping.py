# shopping.py

# ------- Module Description ------- #

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

# ------- System Import -------- #

from typing import List
from enum import Enum
from dataclasses import dataclass, KW_ONLY
from abc import ABC, abstractmethod

import csv
import polars as pl

import threading
import time
from datetime import datetime

# ------- My Imports ------- #

from config_paths import *
from AOSS.other.utils import PathManager, TextEditor
from AOSS.other.exceptions import IllegalProductStructureError, InvalidFileFormatError

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


    name: str
    _: KW_ONLY
    price: float = -1
    approximation: int = -1
    category: str = "unspecified"
    created_at: str
    updated_at: str

    def __post_init__(self):
        self.normalized_name = TextEditor.standardize_str(self.name)



@dataclass
class RegisteredProduct(Product):

    ID: int
    market_ID: int
    _: KW_ONLY
    normalized_category: ProductCategory = ProductCategory.NEURČENÁ

    @staticmethod
    def to_obj(row: str):
        
        attributes = row.split(PRODUCT_FILE['delimiter'])

        if len(attributes) != PRODUCT_FILE['col_count']:
            raise ValueError("Provided row contains invalid amount of attributes!")

        return RegisteredProduct(
            ID=attributes[PRODUCT_FILE['columns']['ID']['index']],
            name=attributes[PRODUCT_FILE['columns']['name']['index']],
            price=float(attributes[ PRODUCT_FILE['columns']['price']['index']]),
            approximation=int(attributes[PRODUCT_FILE['columns']['approximation']['index']]),
            category=attributes[PRODUCT_FILE['columns']['query_string']['index']],
            normalized_category=ProductCategory[attributes[PRODUCT_FILE['columns']['category']['index']]],
            market_ID=attributes[PRODUCT_FILE['columns']['market_ID']['index']],
            created_at=attributes[PRODUCT_FILE['columns']['created_at']['index']],
            updated_at=attributes[PRODUCT_FILE['columns']['updated_at']['index']]
        )
    


class ProductIdentification(ABC):
       
    
    @abstractmethod
    def assign_product_ID(self, market):
        pass
        

class MarketView:
    
    """
        This class is supposed to hold basic information about an online market stored locally and provide
        access to its products.

        Attributes:

            a) ID - unique identifier of a market, best if set by a market hub
            
            b) name - market company name

            c) store_name - unique name of a specific market store

            d) categories - a sublist of all category names as they are used online, they are basically query strings

    """

    def __init__(self, ID:int, name: str, store_name: str, product_file: str,  category_file: str): #hash_file: tuple[str, bool], category_file: tuple[str, bool]):
        self.__ID = ID
        self.__name = name
        self.__store_name = store_name
        self.__categories: List[str] = []

        self.__product_file = product_file
        PathManager.check_if_exists(path=product_file, type='file')

        self.__category_file = category_file
        PathManager.check_if_exists(category_file, type='file')

        
        #we laod categories from provided file
        with open(file=self.__category_file, mode='r', encoding='utf-8') as file:
            categories = csv.DictReader(file)

            for metadata in categories:

                if int(metadata['market_ID']) == self.__ID:
                    self.__categories.append(metadata['name'])

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
    
    def categories(self):
        return tuple(self.__categories)
    

    def product_file(self):
        return self.__product_file
    
    def category_file(self):
        return self.__category_file

    
    def get_product(self, ID: int):

        """
            This is one of the CRUD methods provided by class Market. It is suppossed to load the desired
            product metadata and return it as a new Product object.
            
            Parameters:

                ID - unique identifier of a retrieved product

            Please note, that this method only works within this Market object, so even if the provided ID
            is in dataset but it is not associated with this Market, it will be ignored.
        """

        with open(file=self.__product_file, mode='r', encoding='utf-8') as product_file:
            products = csv.DictReader(product_file)

            for metadata in products:
                
                # return the object only if provided ID was found and if the market_ID equals to this market's
                if ( int(metadata['ID']) == ID and self.__ID == int(metadata['market_ID'])):
                    
                    return RegisteredProduct(
                        ID=metadata['ID'],
                        name=metadata['name'],
                        price=float(metadata['price']),
                        approximation=int(metadata['approximation']),
                        category=metadata['query_string'],
                        normalized_category=ProductCategory[metadata['category']],
                        market_ID=metadata['market_ID'],
                        created_at=metadata['created_at'],
                        updated_at=metadata['updated_at']
                    )
            
        return None

    
    
# --- Market - Class Declaration&Definition --- #

class Market(MarketView):
    
    """
        Class Market extends MarketView by adding registration functionalities, which basically
        allows the market instance to register new Product objects.

        Newly registered products are firstly stored in a buffer during runtime but can also be
        appended to the provided Product File. User can specify limit of this buffer, so that it
        is automatically saved to the file and cleared when necessary.
    
    """
    
    

    def __init__(self, ID: int, name: str, store_name: str, market_hub: ProductIdentification,
                 product_file: str, category_file: str, buffer: int = 5000) -> None:
        super().__init__(ID=ID, name=name, store_name=store_name, product_file=product_file, category_file=category_file)

        # --- Market Attributes --- #
        self.__ID = ID
        self.__market_hub = market_hub
     

        # --- Market Product Registration Attributes --- #

        self.__registration_buffer: List[tuple[Product, ProductCategory]] = []
        self.__buffer_limit = buffer
        self.__buffer_lock = threading.Lock()


    def ID(self) -> int:
        return self.__ID



    def buffer(self, size: int):
        with self.__buffer_lock:
            self.__buffer_limit = size



    def register_product(self, product: Product, norm_category: ProductCategory = ProductCategory.NEURČENÁ):
        
        """
            This method is another of the CRUD method of Market class. It registers the provided product
            by storing it to a list during runtime.

            Parameters:

                a) product - a Product instance to be registered

                b) norm_category - an ProductCategory instance, if product's category is normalized

            In order to register successfully the product has to:

                a) have unique name from the registered or locally stored products

                b) have a category which is supported by the market object
            
            Please note, that in order to store newly added instances persistenly to a Product File
            method save_products() must be used. Products are saved in this manner automatically when
            the buffer limit is reached.
        """


        with self.__buffer_lock:
            # Let's firstly check the unregistered products to prove product's uniqueness
            for _product in self.__registration_buffer:
                if (product.name == _product[0].name):
                    raise IllegalProductStructureError("Conflicting name with an unregistered product!")
            
            # Now we check the registered products for the same purpose
            
            with open(self.product_file(), mode='r', encoding='utf-8') as product_file:
                products = csv.DictReader(product_file)

                #products = csv.reader(product_file)
                
                for row in products:
                    
                    # name attribute must be unique only within a market, therefore we verify
                    # market_ID also
                    if (int(row['market_ID']) == self.__ID and row['name'] == product.name):
                        raise IllegalProductStructureError("Conflicting name with a registered product!")
                

            # here we verify the category of the product, whether the market provides it
            with open(self.category_file(), mode='r', encoding='utf-8') as categories_f:
                categories = csv.DictReader(categories_f)
                
                for metadata in categories:

                    if (product.category == metadata['name']):
                        break

                else:
                    raise IllegalProductStructureError("The market doesn't provide such a category.")

            # Finally, we can add the product for registration
            self.__registration_buffer.append((product, norm_category))
        
            if len(self.__registration_buffer) >= self.__buffer_limit:
                self.save_products()



    def save_products(self):

        """
            This method stores all products stored in a buffer during runtime to the Product File.
            The buffer is cleared at the end of process.
        """


        with open(self.product_file(), 'a', encoding='utf-8') as file:
            for product, category in self.__registration_buffer:
                id = self.__market_hub.assign_product_ID(market=self)
                file.write(str(id) + PRODUCT_FILE['delimiter'] +
                           product.name + PRODUCT_FILE['delimiter'] +
                           product.normalized_name + PRODUCT_FILE['delimiter'] +
                           str(product.price) + PRODUCT_FILE['delimiter'] +
                           str(int(product.approximation)) + PRODUCT_FILE['delimiter'] +
                           category.name + PRODUCT_FILE['delimiter'] +
                           product.category + PRODUCT_FILE['delimiter'] +
                           str(self.__ID) + PRODUCT_FILE['delimiter'] +
                           product.created_at + PRODUCT_FILE['delimiter'] +
                            datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\n')
        
        self.__registration_buffer.clear()





class MarketHub(ProductIdentification):

    """
        MarketHub provides an effective system for market storage and management.
        The implementation is file-based, therefore all metadata are loaded
        directly from files, stored and manipulated efficiently during program
        runtime and then updated back to source files.

        Necessary metadata which must be provided in the source file:

            a) market_ID - next ID assigned to a newly registered market
            b) product_ID - next ID registered by any registered market
            c) market_file - a valid path to a file which stores registered markets


        Registered markets must follow some rules:

            a) They share the same files for their products and categories

            b) Their IDs, names and store names must be unique
        
        Aggregating markets in this manner allows for their categorization and search of registered
        products or even exploring and recommending their instances.
        
        See Also:
            :class:`ProductCategorizer`
            :class:`ProductMatcher`
            :class:`MarketExplorer`
    """

    # ------ MarketHub Constructor ------- #

    def __init__(self, src_file: str) -> None:

        """
            Constructs a MarketHub object by loading its metadata from a provided source file.
            Source file must follow CSV format.
        """

        # this ensures that the provided source file exists
        if PathManager.check_if_exists(path=src_file, type='file'):
            self.__src_file = src_file
    

        # loads the necessary metadata from the source file and verify their format
        with open(file=self.__src_file, mode='r') as src_file:
            reader = csv.DictReader(src_file)
            metadata = next(reader)


            self.__market_ID = int(metadata['market_ID'])
            self.__product_ID = int(metadata['product_ID'])

            if PathManager.check_if_exists(metadata['market_file']):
                self.__market_file = metadata['market_file']

            self.__training_market = int(metadata['training_market'])

        
        self.__markets: List[tuple[Market, int]] = []


    def __enter__(self):
        """
            Apart from constructing a MarketHub object this also automatically loads the 
        """

        print("Loading markets from a file...")
        self.load_markets()
        self.load_products()
        
        print(f"Successfully loaded {len(self.__markets)} markets!")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Updating hub stats to file...")
        self.update()


    # ------ MarketHub - Public Interface ------- #

    def load_markets(self, console_log: bool = False):

        """
            Loads metadata about markets stored in the Market File and stores them as Market objects
            in the buffer. When loading metadata, their format is strictly checked. If certain line
            in the file contain invalid data, it might be skipped completely or logged.

            Paramters:

                console_log - if any errors with Market metadata are encountered, they are logged in
                                       theconsole  
        """

        self.__product_file: str = None
        self.__category_file: str = None

        with open(file=self.__market_file, mode='r', encoding='utf-8') as market_file:
            markets = csv.DictReader(market_file)

            # iterates line by line and loads market metadata storing as Market objects afterwards
            for index, metadata in enumerate(markets):
                ID = None

                try:
                    ID = int(metadata['ID'])
                except ValueError:

                    if console_log:
                        print(f"Error at line {index}: Failed to load ID attribute.")
                
                name = metadata['name']
                store_name = metadata['store_name']

                if (name is None or not name or store_name is None or not store_name) and console_log:
                    print(f"Error at line {index}: Failed to load name or store_name attribute.")


                # checks the existence of the loaded paths
                try:

                    product_file = metadata['product_file']
                    category_file = metadata['category_file']       

                    PathManager.check_if_exists(path=product_file)
                    PathManager.check_if_exists(path=category_file)

                except ValueError:
                    if console_log:
                        print(f"Error at line {index}: Invalid Product File or Category File paths.")

                # checks the consistence of Product and Category File paths
                if self.__product_file is None and self.__category_file is None:
                    self.__product_file = product_file
                    self.__category_file = category_file
                elif ((self.__product_file != product_file or self.__category_file != category_file)
                    and console_log):
                    print(f"Error at line {index}: Inconsistent Product File or Category File paths.")

                new_market = Market(ID=ID,
                                    name=name,
                                    store_name=store_name,
                                    market_hub=self,
                                    product_file=product_file,
                                    category_file=category_file
                            )


                if not self.can_register(market=new_market) and console_log:
                    print("Error at line {index}: Market cannot be aggregated by the market hub!")



                # aggregates new Market object
                self.__markets.append((new_market, new_market.ID()))
            
            # eventually sets the training market
            self.__training_market = self.market(ID=self.__training_market)



    def load_products(self):
        self.__product_df = pl.read_csv(self.__product_file)



    def update(self):
        """
            This method updates MarketHub metadata (product_ID and market_ID) by
            writing it back to the source file.

            This method is called automatically at the end when used along with
            the with statement.
        """

        metadata: List[str] = None

        # updating MarketHub metadata

        with open(self.__src_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            metadata = next(reader)
            
            metadata['market_ID']= str(self.__market_ID)
            metadata['product_ID'] = str(self.__product_ID)


        with open(self.__src_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows([metadata])


        lines = []

        with open(self.__market_file, mode='r', encoding='utf-8') as market_file:
            reader = csv.DictReader(market_file)
            fieldnames = reader.fieldnames
            lines.append(MARKET_FILE['delimiter'].join(fieldnames) + '\n')
            

        for market, ID in self.__markets:
            lines.append(str(ID) + MARKET_FILE['delimiter'] + market.name() + MARKET_FILE['delimiter'] + market.store_name() + MARKET_FILE['delimiter'] + self.__product_file + MARKET_FILE['delimiter'] + self.__category_file + '\n')

        

        with open(self.__market_file, mode='w', newline='', encoding='utf-8') as file:
            file.writelines(lines)


        print("Data updated successfully!")


    
    def product_file(self):
        return self.__product_file

    

    def __get_market_ID(self):
        old_val = self.__market_ID
        self.__market_ID += 1
        return old_val

 
    

    def product_df(self):
        return self.__product_df
    
    def training_market(self):
        return self.__training_market


    def can_register(self, market: MarketView) -> bool:
        """
            This method checks whether the provided market object meets all the necessary
            conditions so that it can be registered by this MarketHub object.

            The mentioned conditions are as follows:
                
                a) The consistency of Product and Category File with the MarketHub instance

                b) Uniqueness of name and store_name attributes
        """

        if (self.__product_file != market.product_file() or self.__category_file
                  != market.category_file()): #or self.__hash_file != market.hash_file()[0]):
            return False
        
        for __market, _ in self.__markets:

            if __market.name() == market.name() or __market.store_name() == market.store_name():
                return False

        return True
    
    def register(self, market: MarketView):
        if self.can_register(market=market):
            self.__markets.append((market, self.__get_market_ID()))
        else:
            raise ValueError("Cannot register provided market!")
    
    def can_categorize(self):
        """
            This methods checks whether categorization by a training market is possible.
            This means, that it cannot be None and it must contain at least one product
            for each of its categories.

            Returns:
                bool: True, if this hub can categorize products, False otherwise

        """

        if self.__training_market is None:
            return False
        else:
            categories = self.__training_market.categories()

            for category in categories:
                if len(self.__product_df.filter((self.__product_df['market_ID'] == self.__training_market.ID()) &
                                        (self.__product_df['query_string'] == category))) == 0:
                    return False
            
        return True


    def market(self, ID: int):
        """
            This will return a registered market by its ID.
        """

        for market, _ in self.__markets:
            if market.ID() == ID:
                return market
            
        return None


    def markets(self):
        """
            This will return a tuple of all aggregated markets.
        """

        return tuple(market for market, _ in self.__markets)
    

    
    def assign_product_ID(self, market: Market):
        
        for market, _ in self.__markets:
            if market.ID() == market.ID():
                old_value = self.__product_ID
                self.__product_ID += 1
                return old_value
        else:
            raise ValueError("Provided market is not aggregated by this market hub! Register it first.")
            
    
                    


if __name__ == "__main__":

    product = Product(name="Hrusky zelene", price=1.23, approximation=0, category="ovocie&zelenina")
    product.__str__()

