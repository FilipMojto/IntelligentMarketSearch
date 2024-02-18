
__AUTHOR__ = "Evenining Programmer"
__VERSION__ = "0.0.1"

from typing import List, Literal
from dataclasses import dataclass, field

from AOSS.structure.shopping import MarketHub, Market, RegisteredProduct, ProductCategory
from AOSS.components.search import ProductMatcher

# class MarketExplorer:

#     """
#         This class explores list of registered markets and attempts to recommend the best one according to a criterium (mostly price).
#         Each market gets allocated a buffer containing products that represent market's offer for the provided product list.

        
#     """

#     def __init__(self, markets: List[Market], matcher: ProductMatcher = None) -> None:
#         self.__markets = markets
#         self.__matcher = matcher
#         self.__product_lists: Dict[Market, List[Product]] = {}

#         for market in self.__markets:
#             self.__product_lists[market] = []

#         if self.__matcher is None:
#             self.__matcher = ProductMatcher(markets=self.__markets, adjust_at=500)
    
#     def product_lists(self):
#         return self.__product_lists



#     def explore(self, products: List[Product], min_match: float = 0.5):
#         if not 0<=min_match<=1:
#             raise ValueError("Minimal match must be float between 0 and 1.")
        
#         for value in self.__product_lists.values():
#             value.clear()


#         best_matches = []
#         processed_markets: List[int] = []

#         for product in products:

#             matches = self.__matcher.match(text=product.name, category=product.category, limit=5, for_each=True)
#             matches.sort(key=lambda pair: (pair[0].market_ID, -pair[1], pair[0].price))

#             for match in matches:
#                 if match[0].market_ID not in processed_markets:
#                     processed_markets.append(match[0].market_ID)
#                     best_matches.append(match)

#             processed_markets.clear()

#             for match in best_matches:
                
#                 for market, product_list in self.__product_lists.items():
#                     if market.ID() == match[0].market_ID:
#                         product_list.append(match[0])
#                         break
            
#             best_matches.clear()
        
#         for product_list in self.__product_lists.values():
#             assert(len(product_list) <= len(products))
    
#     def best_market(self) -> Dict[Market, List[Product]]:
#         min_sum = -1
#         results: Dict[Market, List[Product]] = {}

#         for market, product_list in self.__product_lists.items():
            
#             cur_sum = 0

#             for product in product_list:
#                 cur_sum += product.price


#             if cur_sum < min_sum:
#                 results.clear()
#                 results[market] = product_list
#                 min_sum = cur_sum
#             elif cur_sum == min_sum:
#                 results[market] = product_list
#             elif min_sum == -1:
#                 results[market] = product_list
#                 min_sum = cur_sum

            
#         return results


from typing import Dict


class MarketExplorer:
    
    @dataclass
    class Exploration:
    
        market_ID: int
        # setting this only as [] would create a static variable, because of mutable list
        
        total_price: float
        products: List[tuple[RegisteredProduct, float]] = field(default_factory=list)
        EXPECTED_SIZE: int = -1



        def __post_init__(self):
            if self.EXPECTED_SIZE == -1:
                self.EXPECTED_SIZE = len(self.products)

            if self.EXPECTED_SIZE == 0:
                self.succession_rate = -1
            else:
                self.succession_rate = round((len(self.products)/self.EXPECTED_SIZE) * 100, 2)   




    """
         This class explores list of registered markets and attempts to recommend the best one according to a criterium (mostly price).
         Each market gets allocated a buffer containing products that represent market's offer for the provided product list.
    """

    
    def __init__(self, market_hub: MarketHub) -> None:
        self.__market_hub = market_hub
        self.__matcher = ProductMatcher(market_hub=self.__market_hub)
     
        self.__markets = self.__market_hub.markets()





    def explore(self, product_list: List[ tuple[str, ProductCategory, int]],
                metric: Literal['price', 'success_rate'] = 'price', limit: int = 1):
        """
        
            returns
                Dictionary containing mapping of market IDs on their explored product lists.

        """
        explorations: List[MarketExplorer.Exploration] = []
        
    
        #ha = self.Exploration()
        

        #explorations: List[tuple[int, List[RegisteredProduct], float]] = []

        #product_lists: Dict[int, List[RegisteredProduct]] = {}

        #for market in self.__markets:
           # product_lists.append( (market.ID(), [], 0) )


        for market in self.__markets:
            products: List[List[tuple[RegisteredProduct, float]]] = []
            total_price: List[int] = []

            for i in range(limit):
                products.append([])
                total_price.append(0)

            for explored_product, category, amount in product_list:
                

                match_record = self.__matcher.match(text=explored_product, markets=(market.ID(),), category=None,
                                                    limit=limit, sort_words=True)

                for i in range(limit):

                    #product = market.get_product(ID=match_record[0][0])
                    product = market.get_product(identifier=match_record[i].product_ID)
                    products[i].append((product, match_record[i].ratio))
                    total_price[i] += product.price
                
            for i in range(limit):
                explorations.append(self.Exploration(market_ID=market.ID(), products=products[i], total_price=total_price[i]))
            


            #explorations.append( (market.ID(), products, total_price))

                # for market_ID, products, total_price in product_lists:
                    
                #     if market_ID == market.ID():
                #         _product = market.get_product(ID=match_record[0].product_ID)

                #         products.append(_product)
                #         total_price += _product.price
                #         break


        # for product, category in product_list:

        #     for market in self.__markets:
        
        #         match_record = self.__matcher.match(text=product, markets=(market.ID(),), category=category, limit=1 )
                
        #         #product = market.get_product(ID=match_record[0][0])

        #         for market_ID, products, total_price in product_lists:
                    
        #             if market_ID == market.ID():
        #                 _product = market.get_product(ID=match_record[0].product_ID)

        #                 products.append(_product)
        #                 total_price += _product.price
        #                 break
                #product_lists[market.ID()].append(market.get_product(ID=match_record[0].product_ID))
        
        if metric == 'price' and limit == 1:
            explorations.sort(key=lambda exploration : exploration.total_price)


        return explorations
        






        