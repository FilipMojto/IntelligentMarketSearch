import rapidfuzz.fuzz as fuzz
from typing import List, Dict
from unidecode import unidecode

from AOSS.structure.shopping import Product, RegisteredProduct, MarketHub
from AOSS.structure.shopping import ProductCategory
from config_paths import *


class ProductMatcher:
    
    """
        This class serves for an efficient product search by providing match rates.

        An instance of this class keeps a buffer containing mappings of registered products to the currently searched
        product name. This buffer is cleared every time a new name is searched.

        Attributes:
            __market_hub - a market base containing markets from which the product is searched
            __markets - the mentioned buffer
            __buffer_limit - the limit at which the buffer is cleared using adjust_at() method

        Methods:

            a) match()

            b) clear_at()

            c) __clear_buffer()
    """

    def __init__(self, market_hub: MarketHub, buffer_limit: int = 1000) -> None:

        """
            Class Constructor which initializes everything necessary.
        """

        self.__market_hub = market_hub
        self.__buffer_limit = buffer_limit
        self.__matches: List[tuple[RegisteredProduct, float]] = []
    
    def clear_at(self, matches: int = None):
        
        """
            This method serves both as a getter or a setter for reading or modifying the buffer limit.
        """

        if matches is not None:
            self.__buffer_limit = matches
        
        return self.clear_at


    def match(self, text: str, category: ProductCategory = None, min_match: float = 0, limit: int = 5, for_each: bool = False,
              markets: tuple = None):
        
        # Firstly we check whether the provided parameters fulfill several constraints 
        if not 0<=min_match<=1:
            raise ValueError("Minimal match must be a float in interval <0, 1>.")
        
        if limit >= self.__buffer_limit:
            raise ValueError("Provided limit value higher than buffer limit!")
        
        # Now we process the name string to contain only unicode lowercase characters and clear the buffer
        processed_text = unidecode(text.lower())
        self.__matches.clear()
        
        
        # At this point we can start comparing 
        with open(file=PRODUCT_FILE['path'], mode='r', encoding='utf-8') as file:    
            line = file.readline()

            if line is not None and PRODUCT_FILE['header']:
                line = file.readline()
        
            while(line):
                product = Product.to_obj(row=line)

                match = fuzz.token_sort_ratio(unidecode(product.name.lower()), processed_text)

                if match >= min_match:
                    self.__matches.append( (product, match) )
                
                #if len(self.__matches) > self.__buffer_limit:
                    #self.__clear_buffer(category=category.name.lower(), limit=limit, for_each=for_each)

                    
                line = file.readline()
            
        self.__clear_buffer(category=category, limit=limit, for_each=for_each)
        return self.__matches


    def __clear_buffer(self, limit: int, for_each: bool, category: str = None, markets: tuple = None) -> bool:
        
        # First, we sort matches in desceding order of the match rate, then we will filter only the results of
        # the required category
        self.__matches.sort(key=lambda pair: pair[1], reverse=True)
        
        if markets is not None:
            self.__matches = [(product, ratio) for product, ratio in self.__matches if product.market_ID() in markets]

        if category is not None:
            self.__matches = [(product, ratio) for product, ratio in self.__matches if product.category == category]

        # here we will attempt to restrict matches to the limit so that each market gets its top matches
        # len(self.__matches) <= len(self.__market_hub.markets()) * limit
        if for_each:
            matches_count: Dict[int, int] = {}
            matches = []

            for market in self.__market_hub.markets():
                matches_count[market.ID()] = 0


            for match in self.__matches:
                if matches_count[match[0].market_ID] < limit:
                    matches_count[match[0].market_ID] += 1
                    matches.append(match)

                if len(matches) == limit * len(self.__market_hub.markets()):
                    break
            
            self.__matches = matches
            assert(len(self.__matches) <= len(self.__market_hub.markets()) * limit)
            

        else:
            # we restrict match buffer to the required limit
            self.__matches = self.__matches[:limit]