import rapidfuzz.fuzz as fuzz
from shopping import Market, Product
from typing import List, Dict

class ProductMatcher:
    
    def __init__(self, product_file: str, adjust_at: int = 1000) -> None:
        self.__product_file = product_file
        self.__adjust_at = adjust_at
        self.__matches: List[tuple[Product, float]] = []
    
    def adjust_at(self, matches: int = None):
        if matches is not None:
            self.__adjust_at = matches
        
        return self.adjust_at


    def match(self, text: str, category: str = None, headerless: bool = True, limit: int = 5):

        if limit >= self.__adjust_at:
            raise ValueError("Matches limit must be lower than adjustment point.")

        with open(file=self.__product_file, mode='r', encoding='utf-8') as file:
            self.__matches.clear()

            line = file.readline()

            if not headerless:
                line = file.readline()
        
            while(line):
                product = Product.to_obj(row=line)
                self.__matches.append( (product, fuzz.partial_ratio(product.name().lower(), text.lower())) )
                
                if len(self.__matches) > self.__adjust_at:
                    self.__adjust_matches(category=category, limit=limit)

                    
                line = file.readline()
            
        self.__adjust_matches(category=category, limit=limit)
        return self.__matches

    def __adjust_matches(self, category: str, limit: int) -> bool:
        self.__matches.sort(key=lambda pair: pair[1], reverse=True)
        
        filter(lambda pair: pair[0].category() == category,  self.__matches)
        
        self.__matches = self.__matches[:limit]