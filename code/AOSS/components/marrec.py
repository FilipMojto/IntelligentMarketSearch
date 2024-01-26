
__AUTHOR__ = "Evenining Programmer"
__VERSION__ = "0.0.1"

from typing import List, Dict
from code.AOSS.shopping import Market, Product
from code.components.product_search import ProductMatcher

class MarketExplorer:
    def __init__(self, markets: List[Market], matcher: ProductMatcher = None) -> None:
        self.__markets = markets
        self.__matcher = matcher
        self.__product_lists: Dict[Market, List[Product]] = {}

        for market in self.__markets:
            self.__product_lists[market] = []

        if self.__matcher is None:
            self.__matcher = ProductMatcher(markets=self.__markets, adjust_at=500)
    
    def product_lists(self):
        return self.__product_lists

    def explore(self, products: List[Product], min_match: float = 0.5):
        if not 0<=min_match<=1:
            raise ValueError("Minimal match must be float between 0 and 1.")
        
        for value in self.__product_lists.values():
            value.clear()


        best_matches = []
        processed_markets: List[int] = []

        for product in products:

            matches = self.__matcher.match(text=product.name, category=product.category, limit=5, for_each=True)
            matches.sort(key=lambda pair: (pair[0].market_ID, -pair[1], pair[0].price))

            for match in matches:
                if match[0].market_ID not in processed_markets:
                    processed_markets.append(match[0].market_ID)
                    best_matches.append(match)

            processed_markets.clear()

            for match in best_matches:
                
                for market, product_list in self.__product_lists.items():
                    if market.ID() == match[0].market_ID:
                        product_list.append(match[0])
                        break
            
            best_matches.clear()
        
        for product_list in self.__product_lists.values():
            assert(len(product_list) <= len(products))
    
    def best_market(self) -> Dict[Market, List[Product]]:
        min_sum = -1
        results: Dict[Market, List[Product]] = {}

        for market, product_list in self.__product_lists.items():
            
            cur_sum = 0

            for product in product_list:
                cur_sum += product.price


            if cur_sum < min_sum:
                results.clear()
                results[market] = product_list
                min_sum = cur_sum
            elif cur_sum == min_sum:
                results[market] = product_list
            elif min_sum == -1:
                results[market] = product_list
                min_sum = cur_sum

            
        return results
        #print(self.__best_markets)





