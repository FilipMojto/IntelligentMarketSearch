import rapidfuzz.fuzz as fuzz
from AOSS.structure.shopping import Market, Product
from typing import List, Dict
import AOSS.structure.shopping as shopping
from AOSS.structure.shopping import ProductCategory
from unidecode import unidecode

class ProductMatcher:
    
    def __init__(self, markets, adjust_at: int = 1000) -> None:
        self.__markets: List[Market] = []


        if (isinstance(markets, list) or isinstance(markets, tuple)) and shopping.are_compatible(markets=markets):
            self.__markets.extend(markets)
        elif isinstance(markets, Market):
            self.__markets.append(markets)
        else:
            raise TypeError("Unknown type for markets! Must be object or list!")

        #self.__product_file = product_file
        self.__adjust_at = adjust_at
        self.__matches: List[tuple[Product, float]] = []
    
    def adjust_at(self, matches: int = None):
        if matches is not None:
            self.__adjust_at = matches
        
        return self.adjust_at


    def match(self, text: str, category: ProductCategory = None, min_match: float = 0, limit: int = 5, for_each: bool = False):
        if not 0<=min_match<=1:
            raise ValueError("Minimal match must be float between 0 and 1.")
        
        processed_text = unidecode(text.lower())

        if limit >= self.__adjust_at:
            raise ValueError("Matches limit must be lower than adjustment point.")

        with open(file=self.__markets[0].product_file()[0], mode='r', encoding='utf-8') as file:
            self.__matches.clear()
            line = file.readline()

            if line is not None and self.__markets[0].product_file()[1]:
                line = file.readline()
        
            while(line):
                product = Product.to_obj(row=line)

                match = fuzz.token_sort_ratio(unidecode(product.name.lower()), processed_text)

                if match >= min_match:
                    self.__matches.append( (product, match) )
                
                if len(self.__matches) > self.__adjust_at:
                    self.__adjust_matches(category=category.name.lower(), limit=limit, for_each=for_each)

                    
                line = file.readline()
            
        self.__adjust_matches(category=category.name.lower(), limit=limit, for_each=for_each)
        return self.__matches

    def __adjust_matches(self, category: str, limit: int, for_each: bool) -> bool:

        self.__matches.sort(key=lambda pair: pair[1], reverse=True)
        self.__matches = [(product, ratio) for product, ratio in self.__matches if product.category == category]

        if for_each:
            matches_count: Dict[int, int] = {}
            matches = []

            for market in self.__markets:
                matches_count[market.ID()] = 0


            for match in self.__matches:
                if matches_count[match[0].market_ID] < limit:
                    matches_count[match[0].market_ID] += 1
                    matches.append(match)

                if len(matches) == limit * len(self.__markets):
                    break
            
            self.__matches = matches
            

        else:
            self.__matches = self.__matches[:limit]