import rapidfuzz.fuzz as fuzz
from marketing import Market, Product
from typing import List, Dict

class ProductMatcher:

    def __init__(self, product_file: str) -> None:
        self.__product_file = product_file

    def __top_matches(self, matches: List[Dict[Product, float]], limit: int):
        matches.sort(key=lambda x: list(x.values()), reverse=True)

        if len(matches) <= limit:
            return matches
        else:
            return matches[0 : limit + 1]


    
    def match(self, text: str, headerless: bool = True, limit: int = 5):
        with open(file=self.__product_file, mode='r', encoding='utf-8') as file:
            
            top_matches: List[Dict[Product, float]] = []


            line = file.readline()

            if not headerless:
                line = file.readline()


        
            while(line):
                #attributes = line.split(sep=Market.PF_ATTR_DELIMITER)
                
                product = Product.to_product(row=line)


                top_matches.append({ product : fuzz.partial_ratio(product.name().lower(), text.lower()) })
                
                if len(top_matches) > 1000:
                    top_matches = self.__top_matches(matches=top_matches, limit=limit)

                # print(f"{row[Market.PF_NAME_INDEX]}: {fuzz.token_set_ratio(line.split(Market.PF_ATTR_DELIMITER)[Market.PF_NAME_INDEX], text)}")
                # line = file.readline()
                    
                line = file.readline()
            
        return self.__top_matches(matches=top_matches, limit=limit)

