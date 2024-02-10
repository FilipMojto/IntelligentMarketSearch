
import time





# import config_paths as cfg
# from AOSS.structure.shopping import MarketHub
# from AOSS.components.search import Matcher

# from distutils.core import setup
# from Cython.Build import cythonize

from config_paths import *


from AOSS.structure.shopping import MarketHub, Market, MarketView, ProductCategory
from AOSS.components.scraping.base import ProductScraper, Product
from AOSS.components.marrec import MarketExplorer
from AOSS.components.search import ProductMatcher

from AOSS.components.processing import ProductCategorizer

with MarketHub(src_file=MARKET_HUB_FILE['path']) as hub:
    
    #matcher 

    #categorizer = ProductCategorizer(market_hub=hub)
    #print(categorizer.categorize(product="stolove hrozno biele 500g").name)

    categorizer = ProductCategorizer(market_hub=hub)

    categorizer.recategorize()
    
    # matcher = ProductMatcher(market_hub=hub)
    # start = time.time()
    # match = matcher.match(text="stolove hrozno biele 500g",  markets=(2, ), limit=5, for_each=False)
    # end = time.time()

    # print(f"Time: {end - start}")

    # for m in match:

    #     print(f"{hub.market(ID=m.market_ID).get_product(ID=m.product_ID).name}: {m.ratio}")

    # explorer = MarketExplorer(market_hub=hub)

    # results = explorer.explore(product_list=[("pivo zlaty bazant svetle", ProductCategory.ALKOHOL),
    #                                          ("rozok biely", ProductCategory.PECIVO)])
    
    # for market, product_list in results.items():
    #     print(f"{hub.market(ID=market).name()}: {[ product.name for product in product_list]}")

exit(0)
    #matcher = ProductMatcher(market_hub=hub)
    #matches = matcher.match(text="pivo zlaty bazant svetle", limit=5, for_each=5, category=ProductCategory.ALKOHOL)
    #markets = hub.markets()
    #print(markets[1].get_product(ID=82843).__str__())
    #for match in matches:
    #    print(match)

     #   print(f"Market: {hub.market(ID=match[3]).get_product(ID=match[0]).__str__()}")
    

    #print(matches)

    #explorer = MarketExplorer(market_hub=hub)
    #explorer.explore(product_list=None)



    # market = MarketView(ID=1, name="LSDL", store_name="SDK", category_file="../resources/data/category_mappings.csv",
    #                     product_file="../resources/data/products.csv")
    
    #hub.register(market=market)



    #exit(0)


# with MarketHub(src_file=MARKET_HUB_FILE['path'], header=MARKET_HUB_FILE['header']) as hub:

#     market = hub.market(ID=3)

#     market.for_registration(product=Product(name='Zlatý Bažant 0.0% svetlé nealkoholické pivo 500 ml',
#                                             price=1.08, approximation=0,
#                                             category='alkohol-49',
#                                             created_at='2024-02-07 18:40:44',
#                                             updated_at='2024-02-07 18:40:44'))
    
#     print("no bug!")


# # # from timeit import timeit

# t1 = timeit(
#     "factorial(100)",
#     setup="from cython_test import factorial",
#     number=10_000,
# )

# t2 = timeit(
#     "factorial(100)",
#     setup="from ccython_test import factorial",
#     number=10_000,
# )

# print(f"Pyhon: {t1:.3f}")
# print(f"Cython: {t2:.3f}")


#setup(ext_modules=cythonize("./haha.pyx"))


# start = time.time()
# with open(file=cfg.PRODUCT_FILE['path'], mode='r', encoding='utf-8') as file:
#     line = file.readline()

#     while line:
#         line = file.readline()
# end = time.time()

# print(f"time: {end - start}")


# with MarketHub(src_file=cfg.MARKET_HUB_FILE['path'], header=cfg.MARKET_HUB_FILE['header']) as hub:
#     market = hub.market(ID=2)

#     search = Matcher(market_hub=hub)

#     start = time.time()
#     haha = search.match(text="JUJ", markets=(2,), limit=1)
#     end = time.time()
#     print(f"time: {end - start}")



exit(0) 
# from distutils.spawn import find_executable
# import requests
# import json

# url = "https://restaurant-api.wolt.com/v4/venues/slug/tesco-kamenne-namestie/menu"

# response = requests.get(url)

# def find_name(data, category_ID: str):

#     for category in data['categories']:
#         if category.get("id") == category_ID:
#             return category.get("name")
        


# categories = []

# if response.status_code == 200:
#     data = response.json()
#     products = []
#     for item in data["items"]:
#         name = item.get("name", "No Name")
#         price = item.get("baseprice", "No Price")
#         amount = item.get("quantity_left", "None")
#         category_ID = item.get("category", "None")
        


#         category = find_name(data=data, category_ID=category_ID)
        
#         if category not in categories:
#             categories.append(category)

#         products.append((name, price, amount, category_ID, category))
    
#     for product in products:
#         #print(products)

#         print(f"Name: {product[0]}, Price: {product[1]}, Quantity left: {product[2]}, name: {product[4]}")
# else:
#     print(f"Failed to fetch data: {response.status_code}")
