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
from AOSS.utils import hash_string
from enum import Enum

# --- Market File Configuration --- #

MF_ID_INDEX = 0
MF_NAME_INDEX = MF_ID_INDEX + 1
MF_STORE_NAME_INDEX = MF_NAME_INDEX + 1
MF_NEXT_PRODUCT_INDEX = MF_STORE_NAME_INDEX + 1
MF_PRODUCT_FILE_INDEX = MF_NEXT_PRODUCT_INDEX + 1
MF_PF_HEADER_INDEX = MF_PRODUCT_FILE_INDEX + 1
MF_HASH_FILE_INDEX = MF_PF_HEADER_INDEX + 1
MF_HF_HEADER_INDEX = MF_HASH_FILE_INDEX + 1
MF_CATEGORIES_FILE_INDEX = MF_HF_HEADER_INDEX + 1
MF_CF_HEADER_INDEX = MF_CATEGORIES_FILE_INDEX + 1

MF_ATTR_DELIMITER = ','

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
    ALKOHOL = 10
    TEPLE_NAPOJE = 11
    HOTOVE_INSTANTNE = 12
    ZDRAVE_POTRAVINY = 13

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

            f) hash (string) - hashed name attribute using sha256

            g) market_ID (unsigned int) - unique identifier of a market which possess the product, -1 if not possessed by any market
    """

    ATTRIBUTE_COUNT = 6

    # --- Product File Configuration --- #

    __PF_ID_INDEX = 0
    __PF_NAME_INDEX = __PF_ID_INDEX + 1
    __PF_PRICE_INDEX = __PF_NAME_INDEX + 1
    __PF_APPROXIMATION_INDEX = __PF_PRICE_INDEX + 1
    __PF_CATEGORY_INDEX = __PF_APPROXIMATION_INDEX + 1
    __PF_MARKET_ID_INDEX = __PF_CATEGORY_INDEX + 1

    __PF_ATTR_DELIMITER = ','
    __PF_ROW_DELIMITER = '\n'

    def PF_ID_INDEX():
        return Product.__PF_ID_INDEX
    
    def PF_NAME_INDEX():
        return Product.__PF_NAME_INDEX
    
    def PF_PRICE_INDEX():
        return Product.__PF_PRICE_INDEX
    
    def PF_APPROXIMATION_INDEX():
        return Product.__PF_APPROXIMATION_INDEX
    
    def PF_CATEGORY_INDEX():
        return Product.__PF_CATEGORY_INDEX
    
    def PF_MARKET_ID_INDEX():
        return Product.__PF_MARKET_ID_INDEX
    
    def PF_ATTR_DELIMITER():
        return Product.__PF_ATTR_DELIMITER
    
    def PF_ROW_DELIMITER():
        return Product.__PF_ROW_DELIMITER
    

    @staticmethod
    def to_obj(row: str):
        attributes = row.split(Product.__PF_ATTR_DELIMITER)

        if len(attributes) != Product.ATTRIBUTE_COUNT:
            raise ValueError("Provided row contains invalid amount of attributes!")

        return Product(ID=int(attributes[Product.__PF_ID_INDEX]),
                       name=attributes[Product.__PF_NAME_INDEX],
                       price=float(attributes[Product.__PF_PRICE_INDEX]),
                       approximation=int(attributes[Product.__PF_APPROXIMATION_INDEX]),
                       category=attributes[Product.__PF_CATEGORY_INDEX],
                       market_ID=int(attributes[Product.__PF_MARKET_ID_INDEX]))

    
    def __init__(self, name: str, price: float = -1, approximation: bool = -1, ID: int = -1, category: str = "unspecified", market_ID: int = -1) -> None:

        self.ID = ID
        
        self.name = name
        self.price = price
        self.aproximation = approximation
        self.category = category
        self.hash = hash_string(self.name)
        self.market_ID = market_ID
        
    
    def __repr__(self):
       return f"Product(ID: {self.ID}, name: {self.name}, price: {self.price}, approximation: {self.aproximation}, category: {self.category}, market: {self.market_ID})"



def __to_obj(attributes: List[str], market_file: str, MF_header: bool = False):
    categories = set()

    with open(file=attributes[MF_CATEGORIES_FILE_INDEX].rstrip(), mode='r', encoding='utf-8') as file:
        line = file.readline()
        
        if line is not None and int(attributes[MF_CF_HEADER_INDEX]):
            line = file.readline()

        while line:
            
            c_attributes = line.split(sep=Market.CF_ATTR_DELIMITER())
            
            if c_attributes[Market.CF_MARKET_ID()].rstrip() == attributes[MF_ID_INDEX]:
                categories.add(c_attributes[Market.CF_URL_NAME_INDEX()])

            line = file.readline()
            
    return Market(  ID=int(attributes[MF_ID_INDEX]),
                    name=attributes[MF_NAME_INDEX],
                    store_name=attributes[MF_STORE_NAME_INDEX],
                    product_ID=int(attributes[MF_NEXT_PRODUCT_INDEX]),
                    categories=tuple(categories),
                    market_file=(market_file, MF_header),
                    product_file=(attributes[MF_PRODUCT_FILE_INDEX], bool(int(attributes[MF_PF_HEADER_INDEX]))),
                    hash_file=(attributes[MF_HASH_FILE_INDEX], bool(int(attributes[MF_HF_HEADER_INDEX]))),
                    categories_file=(attributes[MF_CATEGORIES_FILE_INDEX], bool(int(attributes[MF_CF_HEADER_INDEX]))))


    
def market(ID: int, market_file: str, header: bool = False):

    with open(file=market_file, mode='r', encoding='utf-8') as file:
        line = file.readline()
        
        if line is not None and header:
            line = file.readline()


        while line:

            if line[MF_ID_INDEX] == str(ID):
                return __to_obj(attributes=line.split(MF_ATTR_DELIMITER), market_file=market_file, MF_header=header)
            
            line = file.readline()

    return None
    
def markets(market_file: str, header: bool = False):
    list: List[Market] = []

    with open(market_file, 'r', encoding='utf-8') as file:
        line = file.readline()

        if line is not None and header:
            line = file.readline()

        while(line):

            list.append(__to_obj(attributes=line.split(MF_ATTR_DELIMITER), market_file=market_file, MF_header=header))
            line = file.readline()
    
    return tuple(list)




# --- Market - Class Declaration&Definition --- #

class Market:
    
    

    #MF_CATEGORIES_INDEX = MF_NEXT_PRODUCT_INDEX + 1

    # --- Hash File Configuration --- #

    __HF_ID_INDEX = 0
    __HF_MARKET_ID_INDEX = __HF_ID_INDEX + 1
    __HF_HASH_INDEX = __HF_MARKET_ID_INDEX + 1

    __HF_ATTR_DELIMITER = ','
    __HF_ROW_DELIMITER = '\n'

    # --- Categories File Configuration --- #

    __CF_ID_INDEX = 0
    __CF_URL_NAME_INDEX = __CF_ID_INDEX + 1
    __CF_NAME_INDEX = __CF_URL_NAME_INDEX + 1
    __CF_MARKET_ID = __CF_NAME_INDEX + 1

    __CF_ATTR_DELIMITER = ','
    __CF_ROW_DELIMITER = '\n'


    @staticmethod
    def HF_ID_INDEX():
        return Market.__HF_ID_INDEX
    
    @staticmethod
    def HF_MARKET_ID_INDEX():
        return Market.__HF_MARKET_ID_INDEX
    
    @staticmethod
    def HF_HASH_INDEX():
        return Market.__HF_HASH_INDEX
    
    @staticmethod
    def HF_ATTR_DELIMITER():
        return Market.__HF_ATTR_DELIMITER
    
    @staticmethod
    def HF_ROW_DELIMITER():
        return Market.__HF_ROW_DELIMITER
    
    @staticmethod
    def CF_ID_INDEX():
        return Market.__CF_ID_INDEX
    
    @staticmethod
    def CF_URL_NAME_INDEX():
        return Market.__CF_URL_NAME_INDEX
    
    @staticmethod
    def CF_NAME_INDEX():
        return Market.__CF_NAME_INDEX
    
    @staticmethod
    def CF_MARKET_ID():
        return Market.__CF_MARKET_ID
    
    @staticmethod
    def CF_ATTR_DELIMITER():
        return Market.__CF_ATTR_DELIMITER
    
    @staticmethod
    def CF_ROW_DELIMITER():
        return Market.__CF_ROW_DELIMITER

    def __init__(self, ID: int, name: str, store_name: str, product_ID: int, categories: tuple[str], market_file: tuple[str, bool],
                 product_file: tuple[str, bool], hash_file: tuple[str, bool], categories_file: tuple[str, bool], buffer: int = 1000) -> None:
        
        # --- Market Attributes --- #
        self.__ID = ID
        self.__name = name
        self.__store_name = store_name
        self.__product_ID = product_ID
        self.__categories = categories

        # --- Market External Files Configuration --- #

        self.__market_file = market_file
        self.__product_file = product_file
        self.__hash_file = hash_file
        self.__categories_file = categories_file

        # --- Market Product Registration Attributes --- #

        self.__registration_buffer: List[Product] = []
        self.__buffer_limit = buffer
        self.__buffer_lock = threading.Lock()

        
        
    def __repr__(self):
        return f"Market(ID: {self.__ID}, name: {self.__name}, store_name: {self.__store_name}, roduct_ID: {self.__product_ID}, categories: {self.__categories})"

    def ID(self) -> int:
        return self.__ID
    
    def name(self) -> str:
        return self.__name
    
    def store_name(self) -> str:
        return self.__store_name
    
    def product_ID(self) -> int:
        return self.__product_ID
    
    def buffer(self, size: int):
        with self.__buffer_lock:
            self.__buffer_limit = size

    def market_file(self) -> tuple[str, bool]:
        return self.__market_file
    
    def product_file(self) -> tuple[str, bool]:
        return self.__product_file
    
    def hash_file(self) -> tuple[str, bool]:
        return self.__hash_file 

    def for_registration(self, product: Product):

        with self.__buffer_lock:
            # Let's firstly check the unregistered products to prove product's uniqueness
            for _product in self.__registration_buffer:
                if (product.hash == _product.hash):
                    raise ValueError("Conflicting ID or name with an unregistered product!")
            
            # Now we check the registered products for the same purpose
                

            with open(self.__hash_file[0], 'r', encoding='utf-8') as file:
                line = file.readline()

                if line is not None and self.__hash_file[1]:
                    line = file.readline()


                while line:
                    attributes = line.split(sep=self.__HF_ATTR_DELIMITER)

                    #if (int(attributes[self.HF_MARKET_ID_INDEX]) == self.ID )

                    if int(attributes[self.__HF_MARKET_ID_INDEX]) == self.__ID and (int(attributes[self.__HF_ID_INDEX]) == product.ID or attributes[self.__HF_HASH_INDEX].rstrip() == product.hash):
                        raise ValueError("Product already registered!")
                    
                    line = file.readline()
            
            # here we verify the category of the product, whether the market provides it
            with open(self.__categories_file[0], mode='r', encoding='utf-8') as categories_f:
                line = categories_f.readline()

                if line is not None and self.__categories_file[1]:
                    line = categories_f.readline()

                while line:
                    attributes = line.split(Market.__CF_ATTR_DELIMITER)

                    if (product.category == attributes[Market.__CF_URL_NAME_INDEX]):
                        product.category = attributes[Market.__CF_NAME_INDEX]
                        break
                    elif product.category == attributes[Market.__CF_NAME_INDEX]:
                        break

                    line = categories_f.readline()
                else:
                    raise ValueError("The market doesn't provide such a category.")

            # Finally, we can add the product for registration
            self.__registration_buffer.append(product)
        
            if len(self.__registration_buffer) >= self.__buffer_limit:
                self.register_products()
    



    def get_product(self, ID: int):

        with open(file=self.__product_file[0], mode='r', encoding='utf-8') as file:
            line = file.readline()

            while(line):
                attributes = line.split(sep=Product.PF_ATTR_DELIMITER())

                if attributes[Product.PF_ID_INDEX()] == str(ID) and self.__ID == int(attributes[Product.PF_MARKET_ID_INDEX()]):
                    
                    return Product.to_obj(row=line)

                line = file.readline()
        
        return None



    def register_products(self):


        with open(self.__product_file[0], 'a', encoding='utf-8') as file:
            for product in self.__registration_buffer:

                file.write(str(self.__product_ID) + Product.PF_ATTR_DELIMITER() + product.name + Product.PF_ATTR_DELIMITER() + str(product.price)
                            + Product.PF_ATTR_DELIMITER() + str(int(product.aproximation)) + Product.PF_ATTR_DELIMITER() + product.category +
                            Product.PF_ATTR_DELIMITER() + str(self.__ID) + Product.PF_ROW_DELIMITER())

                product.ID = self.__product_ID
                self.__product_ID += 1
                


        with open(self.__market_file[0], 'r') as file:
            line = file.readline()
            lines = []
            found = False
            
            while line:

                if line.split(MF_ATTR_DELIMITER)[MF_ID_INDEX] == str(self.__ID):
                    attributes: List[str] = line.split(MF_ATTR_DELIMITER)
                    attributes[MF_NEXT_PRODUCT_INDEX] = str(self.__product_ID)
                    lines.append(','.join(attributes))
                    found = True
                else:
                    lines.append(line)

                line = file.readline()
            
            if not found:
                raise ValueError("Market is not officially registered!")

        with open(self.__market_file[0], 'w') as file:
            file.writelines(lines)

        # now we can create hashes for the products
                
        with open(self.__hash_file[0], 'a', encoding='utf-8') as hash_file:
            _len = len(self.__registration_buffer)

            # here we are popping elements from the end
            for i in range(_len):
                product = self.__registration_buffer[_len - 1 - i]
            
                hash_file.write(str(product.ID) + self.__HF_ATTR_DELIMITER + str(self.__ID) + self.__HF_ATTR_DELIMITER + str(product.hash) +
                                self.__HF_ROW_DELIMITER)
                
                self.__registration_buffer.pop()

        # all unregistered products should be removed
        assert(len(self.__registration_buffer) == 0)
            
        
        
    def categories(self) -> tuple[str]:
        return self.__categories




def are_compatible(markets: List[Market]) -> bool:

    if len(markets) == 0 or len(markets) == 1:
        raise ValueError("Cannot compare this count of markets!")

    count = len(markets)

    for i in range(count):

        for g in range(count):

            if (markets[i].market_file()[0] != markets[g].market_file()[0] or markets[i].product_file()[0] != markets[g].product_file()[0]
            or markets[i].hash_file()[0] != markets[g].hash_file()[0]):
                return False
    
    return True
                


if __name__ == "__main__":

    product = Product(name="Hrusky zelene", price=1.23, approximation=0, category="ovocie&zelenina")
    product.__str__()

