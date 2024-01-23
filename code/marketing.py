
import csv
from typing import List
from enum import Enum
import threading
from utils import hash_string

class Product:

    ATTRIBUTE_COUNT = 6

    @staticmethod
    def to_product(row: str):
        attributes = row.split(Market.PF_ATTR_DELIMITER)

        if len(attributes) != Product.ATTRIBUTE_COUNT:
            raise ValueError("Provided row contains invalid amount of attributes!")

        return Product(ID=int(attributes[Market.PF_ID_INDEX]),
                       name=attributes[Market.PF_NAME_INDEX],
                       price=float(attributes[Market.PF_PRICE_INDEX]),
                       approximation=int(attributes[Market.PF_APPROXIMATION_INDEX]),
                       category=attributes[Market.PF_CATEGORY_INDEX],
                       market_ID=attributes[Market.PF_MARKET_ID_INDEX])


    def __init__(self, name: str, price: float, approximation: bool, ID: int = -1, category: str = "unspecified", market_ID: int = -1) -> None:
        self.__ID = ID
        self.__name = name
        self.__price = price
        self.__aproximation = approximation
        self.__category = category
        self.__hash = hash_string(self.__name)
        self.__market_ID = market_ID
        
    
    def __str__(self, end = '\n'):
        print("{{ID: {}, name: {}, price: {}, approximation: {}, category: {}, market: {}}}".format(
            self.__ID,
            self.__name,
            self.__price,
            self.__aproximation,
            self.__category,
            self.__market_ID
        ), end=end)

    def ID(self, ID: int = None) -> int:
        if ID is not None:
            self.__ID = ID

        return self.__ID
    
    def name(self) -> str:
        return self.__name
    
    def hash(self):
        return self.__hash

    def price(self) -> float:
        return self.__price
    
    def approximation(self) -> bool:
        return self.__aproximation
    
    # def category(self) -> str:
    #     return self.__category
    
    def category(self, category: str = None) -> str:
        if category is not None:
            self.__category = category
        return self.__category

    def market_ID(self, ID: int = None) -> int:
        if ID is not None:
            self.__market_ID = ID
        
        return self.__market_ID


class Market:
    
    # --- Product File Configuration --- #

    PF_ID_INDEX = 0
    PF_NAME_INDEX = PF_ID_INDEX + 1
    PF_PRICE_INDEX = PF_NAME_INDEX + 1
    PF_APPROXIMATION_INDEX = PF_PRICE_INDEX + 1
    PF_CATEGORY_INDEX = PF_APPROXIMATION_INDEX + 1
    PF_MARKET_ID_INDEX = PF_CATEGORY_INDEX + 1

    PF_ATTR_DELIMITER = ','
    PF_ROW_DELIMITER = '\n'

    # --- Market File Configuration --- #

    MF_ID_INDEX = 0
    MF_NAME_INDEX = MF_ID_INDEX + 1
    MF_STORE_NAME_INDEX = MF_NAME_INDEX + 1
    MF_NEXT_PRODUCT_INDEX = MF_STORE_NAME_INDEX + 1
    MF_CATEGORIES_INDEX = MF_NEXT_PRODUCT_INDEX + 1

    MF_ATTR_DELIMITER = ','
    MF_CATEGORIES_DELIMITER = ';'

    # --- Hash File Configuration --- #

    HF_ID_INDEX = 0
    HF_MARKET_ID_INDEX = HF_ID_INDEX + 1
    HF_HASH_INDEX = HF_MARKET_ID_INDEX + 1

    __HF_ATTR_DELIMITER = ','
    __HF_ROW_DELIMITER = '\n'

    @staticmethod
    def get_market(market_file: str, product_file: str, hash_file: str, ID: int):
        with open(market_file, 'r', newline='') as file:
            reader = csv.reader(file)
            lines = list(reader)

        for line in lines:
            if line[Market.MF_ID_INDEX] == str(ID):
                return Market(ID=ID,
                              name=line[Market.MF_NAME_INDEX],
                              store_name=line[Market.MF_STORE_NAME_INDEX],
                              product_ID=int(line[Market.MF_NEXT_PRODUCT_INDEX]),
                              categories=line[Market.MF_CATEGORIES_INDEX]
                              .split(Market.MF_CATEGORIES_DELIMITER),
                              market_file=market_file,
                              product_file=product_file,
                              hash_file=hash_file)
        
        return None
    
    @staticmethod
    def markets(market_file: str, product_file: str, headerless = True):
        list: List[Market] = []

        with open(market_file, 'r', encoding='utf-8') as file:

            line = file.readline()

            if not headerless:
                line = file.readline()

            while(line):
                record_vals = line.split(Market.MF_ATTR_DELIMITER)

                list.append(Market(ID=record_vals[Market.PF_MARKET_ID_INDEX],
                                   name=line[Market.MF_NAME_INDEX],
                                    store_name=line[Market.MF_STORE_NAME_INDEX],
                                    product_ID=int(line[Market.MF_NEXT_PRODUCT_INDEX]),
                                    categories=line[Market.MF_CATEGORIES_INDEX]
                                    .split(Market.MF_CATEGORIES_DELIMITER), product_file=product_file))
                
                line = file.readline()
        
        return tuple(list)


    def __init__(self, ID: int, name: str, store_name: str, product_ID: int, categories: tuple[str], market_file: str,
                 product_file: str, hash_file: str, unregistered_limit: int = 1000) -> None:
        self.__ID = ID
        self.__name = name
        self.__store_name = store_name
        self.__product_ID = product_ID
        self.__categories = categories
        self.__unregistered_products: List[Product] = []
        self.__unregistered_limit = unregistered_limit
        self.__unregistered_lock = threading.Lock()

        self.__market_file = market_file
        self.__product_file = product_file
        self.__hash_file = hash_file
        
    
    def ID(self) -> int:
        return self.__ID
    
    def name(self) -> str:
        return self.__name
    
    def store_name(self) -> str:
        return self.__store_name
    
    def product_ID(self) -> ID:
        return self.__product_ID
    
    def for_registration(self, product: Product):

        if len(self.__unregistered_products) >= self.__unregistered_limit:
            self.register_products()

        with self.__unregistered_lock:
            # Let's firstly check the unregistered products to prove product's uniqueness
            for _product in self.__unregistered_products:
                if (product.hash() == _product.hash()):
                    raise ValueError("Conflicting ID or name with an unregistered product!")
            
            # Now we check the registered products for the same purpose
            with open(self.__hash_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                lines = list(reader)

            for line in lines:
                if line[self.HF_MARKET_ID_INDEX] == self.__ID and (line[self.HF_ID_INDEX] == product.ID() or line[self.HF_HASH_INDEX] == product.hash()):
                    raise ValueError("Product already registered!")
            
            # Finally, we can add the product for registration
            self.__unregistered_products.append(product)
    

    def get_product(self, ID: int):

        with open(file=self.__product_file, mode='r', encoding='utf-8') as file:
            line = file.readline()

            while(line):
                attributes = line.split(sep=self.PF_ATTR_DELIMITER)

                if attributes[self.PF_ID_INDEX] == str(ID) and self.__ID == int(attributes[self.PF_MARKET_ID_INDEX]):
                    return Product(ID=int(attributes[self.PF_ID_INDEX]),
                                   name=attributes[self.PF_NAME_INDEX],
                                   price=float(attributes[self.PF_PRICE_INDEX]),
                                   approximation=int(attributes[self.PF_APPROXIMATION_INDEX]),
                                   category=attributes[self.PF_CATEGORY_INDEX],
                                   market_ID=attributes[self.PF_MARKET_ID_INDEX].rstrip())


                line = file.readline()
        
        return None


    def register_products(self):


        # with open(self.__product_file, 'r', newline='', encoding='utf-8') as file:
        #     reader = csv.reader(file)
        #     lines = list(reader)

        # for line in lines:
        #     if line[self.__MARKET_ID_INDEX] == self.__ID() and (line[self.__NEXT_PRODUCT_INDEX] == product.ID() or line[self.__NAME_INDEX] == product.name()):
        #         raise ValueError("Product already registered!")
        
        # # category = product.category()

        # # if category == None:
        # #     category = "unspecified"
        
        # firstly, the unregistered products are registered in product file

        with self.__unregistered_lock:
            with open(self.__product_file, 'a', encoding='utf-8') as file:
                

                for product in self.__unregistered_products:

                    # let's get the last product and register it
                    #product = self.__unregistered_products[_len - 1 - i]
                    
                    file.write(str(self.__product_ID) + self.PF_ATTR_DELIMITER + product.name() + self.PF_ATTR_DELIMITER + str(product.price())
                                + self.PF_ATTR_DELIMITER + str(int(product.approximation())) + self.PF_ATTR_DELIMITER + product.category() +
                                self.PF_ATTR_DELIMITER + str(self.__ID) + self.PF_ROW_DELIMITER)

                    product.ID(ID=self.__product_ID)
                    self.__product_ID += 1
                    
                    #self.__unregistered_products.pop()
            
            #with open(self.__market_file, 'w')

            with open(self.__market_file, 'r', newline='') as file:
                reader = csv.reader(file)
                lines = list(reader)

            for line in lines:
                if line[self.MF_ID_INDEX] == str(self.ID()):
                    line[self.MF_NEXT_PRODUCT_INDEX] = self.product_ID()
                    break
            else:
                raise ValueError("Market is not officially registered!")

            with open(self.__market_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)

            # now we can create hashes for the products
                    
            with open(self.__hash_file, 'a', encoding='utf-8') as hash_file:
                _len = len(self.__unregistered_products)

                # here we are popping elements from the end
                for i in range(_len):
                    product = self.__unregistered_products[_len - 1 - i]
                
                    hash_file.write(str(product.ID()) + self.__HF_ATTR_DELIMITER + str(self.__ID) + self.__HF_ATTR_DELIMITER + str(product.hash()) +
                                    self.__HF_ROW_DELIMITER)
                    
                    self.__unregistered_products.pop()

            # all unregistered products should be removed
            assert(len(self.__unregistered_products) == 0)
            
        
        

            # for product in self.__unregistered_products:    

            #     file.write(str(self.__product_ID) + self.__PF_ATTR_DELIMITER + product.name() + self.__PF_ATTR_DELIMITER + str(product.price())
            #                 + self.__PF_ATTR_DELIMITER + str(int(product.approximation())) + self.__PF_ATTR_DELIMITER + product.category() +
            #                 self.__PF_ATTR_DELIMITER + str(self.__ID) + self.__PF_ROW_DELIMITER)

            #     self.__product_ID += 1
            
            # assert(len(self.__unregistered_products) == 0)
    
    # def update_market(self):
    #     with open(self.__src_file, 'r', newline='') as file:
    #         reader = csv.reader(file)
    #         lines = list(reader)

    #     for line in lines:
    #         if line[self.ID_INDEX] == str(self.ID()):
    #             line[self.PRODUCT_ID_INDEX] = self.product_ID()
    #             break
    #     else:
    #         raise ValueError("Market is not officially registered!")

    #     with open(self.__src_file, 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerows(lines)  

    # #original_val = self.__product_ID
    #     self.__product_ID += 1
    #     #return original_val
        
    def categories(self) -> tuple[str]:
        return self.__categories



# class MarketManager:
#     ID_INDEX = 0
#     NAME_INDEX = ID_INDEX + 1
#     STORE_NAME_INDEX = NAME_INDEX + 1
#     PRODUCT_ID_INDEX = STORE_NAME_INDEX + 1
#     CATEGORIES_ID_INDEX = PRODUCT_ID_INDEX + 1

#     __ATTR_DELIMITER = ','
#     __CATEGORIES_DELIMITER = ';'

#     def __init__(self, src_file: str, product_file: str, headerless=True) -> None:
#         self.__src_file = src_file
#         self.__product_file = product_file
#         self.__headerless = headerless
#         pass

    # def get_market(self, ID: int) -> Market:
    #     with open(self.__src_file, 'r', newline='') as file:
    #         reader = csv.reader(file)
    #         lines = list(reader)

    #     for line in lines:
    #         if line[MarketManager.ID_INDEX] == str(ID):
    #             return Market(ID=ID,name=line[MarketManager.NAME_INDEX], store_name=line[MarketManager.STORE_NAME_INDEX], product_ID=int(line[MarketManager.PRODUCT_ID_INDEX]),
    #                           categories=line[MarketManager.CATEGORIES_ID_INDEX].split(MarketManager.__CATEGORIES_DELIMITER), product_file=self.__product_file)
        
    #     return None
    
    # def markets(self) -> tuple[Market]:
    #     list: List[Market] = []

    #     with open(self.__src_file, 'r', encoding='utf-8') as file:

    #         line = file.readline()

    #         if not self.__headerless:
    #             line = file.readline()

    #         while(line):
    #             record_vals = line.split(self.__ATTR_DELIMITER)

    #             list.append(Market(ID=record_vals[self.ID_INDEX],
    #                                name=record_vals[MarketManager.NAME_INDEX],
    #                                store_name=record_vals[MarketManager.STORE_NAME_INDEX],
    #                                product_ID=int(record_vals[MarketManager.PRODUCT_ID_INDEX]),
    #                                categories=record_vals[MarketManager.CATEGORIES_ID_INDEX].split(MarketManager.__CATEGORIES_DELIMITER),
    #                                product_file=self.__product_file))
                
    #             line = file.readline()
        
    #     return tuple(list)


    # def update_market(self, market: Market):
    #     with open(self.__src_file, 'r', newline='') as file:
    #         reader = csv.reader(file)
    #         lines = list(reader)

    #     for line in lines:
    #         if line[self.ID_INDEX] == str(market.ID()):
    #             line[self.PRODUCT_ID_INDEX] = market.product_ID()
    #             break
    #     else:
    #         raise ValueError("Market is not officially registered!")

    #     with open(self.__src_file, 'w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerows(lines)    


    

if __name__ == "__main__":

    product = Product(name="Hrusky zelene", price=1.23, approximation=0, category="ovocie&zelenina")
    product.__str__()

    # ha = MarketManager(src_file="../resources/markets.csv", product_file="../resources/products.csv")
    # market = ha.get_market(1)
    # market.register_product()

    # ha.update_market(market)
    # print("HAHA")