from typing import List
import threading
from utils import hash_string


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

    PF_ID_INDEX = 0
    PF_NAME_INDEX = PF_ID_INDEX + 1
    PF_PRICE_INDEX = PF_NAME_INDEX + 1
    PF_APPROXIMATION_INDEX = PF_PRICE_INDEX + 1
    PF_CATEGORY_INDEX = PF_APPROXIMATION_INDEX + 1
    PF_MARKET_ID_INDEX = PF_CATEGORY_INDEX + 1

    PF_ATTR_DELIMITER = ','
    PF_ROW_DELIMITER = '\n'

    @staticmethod
    def to_obj(row: str):
        attributes = row.split(Product.PF_ATTR_DELIMITER)

        if len(attributes) != Product.ATTRIBUTE_COUNT:
            raise ValueError("Provided row contains invalid amount of attributes!")

        return Product(ID=int(attributes[Product.PF_ID_INDEX]),
                       name=attributes[Product.PF_NAME_INDEX],
                       price=float(attributes[Product.PF_PRICE_INDEX]),
                       approximation=int(attributes[Product.PF_APPROXIMATION_INDEX]),
                       category=attributes[Product.PF_CATEGORY_INDEX],
                       market_ID=int(attributes[Product.PF_MARKET_ID_INDEX]))

    
    def __init__(self, name: str, price: float, approximation: bool, ID: int = -1, category: str = "unspecified", market_ID: int = -1) -> None:

        self.ID = ID
        
        self.name = name
        self.price = price
        self.aproximation = approximation
        self.category = category
        self.hash = hash_string(self.name)
        self.market_ID = market_ID
        
    
    def __repr__(self):
       return f"Product(ID: {self.ID}, name: {self.name}, price: {self.price}, approximation: {self.aproximation}, category: {self.category}, market: {self.market_ID})"




# --- Market - Class Declaration&Definition --- #

class Market:
    


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

    #MF_CATEGORIES_INDEX = MF_NEXT_PRODUCT_INDEX + 1

    MF_ATTR_DELIMITER = ','
    MF_CATEGORIES_DELIMITER = ';'

    # --- Hash File Configuration --- #

    HF_ID_INDEX = 0
    HF_MARKET_ID_INDEX = HF_ID_INDEX + 1
    HF_HASH_INDEX = HF_MARKET_ID_INDEX + 1

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
    def __to_obj(attributes: List[str], market_file: str, MF_header: bool = False):
        categories = set()

        with open(file=attributes[Market.MF_CATEGORIES_FILE_INDEX].rstrip(), mode='r', encoding='utf-8') as file:
            line = file.readline()
            
            if line is not None and int(attributes[Market.MF_CF_HEADER_INDEX]):
                line = file.readline()

            while line:
                
                c_attributes = line.split(sep=Market.__CF_ATTR_DELIMITER)
                
                if c_attributes[Market.__CF_MARKET_ID].rstrip() == attributes[Market.MF_ID_INDEX]:
                    categories.add(c_attributes[Market.__CF_URL_NAME_INDEX])

                line = file.readline()
                
        return Market(  ID=int(attributes[Market.MF_ID_INDEX]),
                        name=attributes[Market.MF_NAME_INDEX],
                        store_name=attributes[Market.MF_STORE_NAME_INDEX],
                        product_ID=int(attributes[Market.MF_NEXT_PRODUCT_INDEX]),
                        categories=tuple(categories),
                        market_file=(market_file, MF_header),
                        product_file=(attributes[Market.MF_PRODUCT_FILE_INDEX], bool(int(attributes[Market.MF_PF_HEADER_INDEX]))),
                        hash_file=(attributes[Market.MF_HASH_FILE_INDEX], bool(int(attributes[Market.MF_HF_HEADER_INDEX]))),
                        categories_file=(attributes[Market.MF_CATEGORIES_FILE_INDEX], bool(int(attributes[Market.MF_CF_HEADER_INDEX]))))


    @staticmethod
    def market(ID: int, market_file: str, header: bool = False):

        with open(file=market_file, mode='r', encoding='utf-8') as file:
            line = file.readline()
            
            if line is not None and header:
                line = file.readline()


            while line:

                if line[Market.MF_ID_INDEX] == str(ID):
                    return Market.__to_obj(attributes=line.split(Market.MF_ATTR_DELIMITER), market_file=market_file, MF_header=header)
                
                line = file.readline()

        return None
    
    @staticmethod
    def markets(market_file: str, header: bool = False):
        list: List[Market] = []

        with open(market_file, 'r', encoding='utf-8') as file:
            line = file.readline()

            if line is not None and header:
                line = file.readline()

            while(line):

                list.append(Market.__to_obj(attributes=line.split(Market.MF_ATTR_DELIMITER), market_file=market_file, MF_header=header))
                line = file.readline()
        
        return tuple(list)


    def __init__(self, ID: int, name: str, store_name: str, product_ID: int, categories: tuple[str], market_file: tuple[str, bool],
                 product_file: tuple[str, bool], hash_file: tuple[str, bool], categories_file: tuple[str, bool], buffer: int = 1000) -> None:
        
        # --- Market Attributes --- #
        self.ID = ID
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
        return f"Market(ID: {self.ID}, name: {self.__name}, store_name: {self.__store_name}, roduct_ID: {self.__product_ID}, categories: {self.__categories})"

    def ID(self) -> int:
        return self.ID
    
    def name(self) -> str:
        return self.__name
    
    def store_name(self) -> str:
        return self.__store_name
    
    def product_ID(self) -> ID:
        return self.__product_ID
    
    def buffer(self, size: int):
        with self.__buffer_lock:
            self.__buffer_limit = size



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
                 # reader = csv.reader(file)
                # lines = list(reader)

                while line:
                    attributes = line.split(sep=self.__HF_ATTR_DELIMITER)

                    if int(attributes[self.HF_MARKET_ID_INDEX]) == self.ID and (int(attributes[self.HF_ID_INDEX]) == product.ID or attributes[self.HF_HASH_INDEX].rstrip() == product.hash):
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
                attributes = line.split(sep=Product.PF_ATTR_DELIMITER)

                if attributes[Product.PF_ID_INDEX] == str(ID) and self.ID == int(attributes[Product.PF_MARKET_ID_INDEX]):
                    
                    return Product.to_obj(row=line)
                    # return Product(ID=int(attributes[self.PF_ID_INDEX]),
                    #                name=attributes[self.PF_NAME_INDEX],
                    #                price=float(attributes[self.PF_PRICE_INDEX]),
                    #                approximation=int(attributes[self.PF_APPROXIMATION_INDEX]),
                    #                category=attributes[self.PF_CATEGORY_INDEX],
                    #                market_ID=attributes[self.PF_MARKET_ID_INDEX].rstrip())


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
        #with self.__unregistered_lock:
        with open(self.__product_file[0], 'a', encoding='utf-8') as file:
            for product in self.__registration_buffer:

                # let's get the last product and register it
                #product = self.__unregistered_products[_len - 1 - i]
                
                file.write(str(self.__product_ID) + Product.PF_ATTR_DELIMITER + product.name + Product.PF_ATTR_DELIMITER + str(product.price)
                            + Product.PF_ATTR_DELIMITER + str(int(product.aproximation)) + Product.PF_ATTR_DELIMITER + product.category +
                            Product.PF_ATTR_DELIMITER + str(self.ID) + Product.PF_ROW_DELIMITER)

                product.ID = self.__product_ID
                self.__product_ID += 1
                
                #self.__unregistered_products.pop()
        
        #with open(self.__market_file, 'w')

        with open(self.__market_file[0], 'r') as file:
            line = file.readline()
            lines = []
            found = False
            
            while line:

                if line[self.MF_ID_INDEX] == str(self.ID):
                    attributes: List[str] = line.split(self.MF_ATTR_DELIMITER)
                    attributes[self.MF_NEXT_PRODUCT_INDEX] = str(self.__product_ID)
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
            
                hash_file.write(str(product.ID) + self.__HF_ATTR_DELIMITER + str(self.ID) + self.__HF_ATTR_DELIMITER + str(product.hash) +
                                self.__HF_ROW_DELIMITER)
                
                self.__registration_buffer.pop()

        # all unregistered products should be removed
        assert(len(self.__registration_buffer) == 0)
            
        
        

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