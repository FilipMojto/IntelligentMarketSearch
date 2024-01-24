from shopping import Market, Product, ProductCategory
from product_scraping import ProductScraper
from product_search import ProductMatcher
from marrec import MarketExplorer
import config_paths
import rapidfuzz.fuzz as fuzz

import shopping as shopping
import polars as pl

explorer = MarketExplorer(markets=shopping.markets(market_file=config_paths.MARKET_FILE_PATH, header=True) )
explorer.explore(products=[Product(name="Rozok biely", category=ProductCategory.PECIVO)])

markets = explorer.best_market()

for market in markets.keys():
    print(str(market))



#markets = explorer.best_market()

#print(str(markets))

# pl_df = pl.read_csv(config_paths.PRODUCT_FILE_PATH)



# market = Market.market(ID=1, market_file=config_paths.MARKET_FILE_PATH, header=True)

# scraper = ProductScraper(market=market)
# scraper.scrape_category(category="pecivo-111", register=True, _print=True)

# market.register_products()
# print("END")

# print(ProductCategory.NEALKOHOLICKE_NAPOJE.value)

# markets = shopping.markets(market_file=config_paths.MARKET_FILE_PATH, header=True)

# for market in markets:
#     print(market.__repr__())

# print(shopping.are_compatible(markets=markets))

# matcher = ProductMatcher(markets=markets)
# matches = matcher.match(text="rozok", category=ProductCategory.PECIVO, limit=15)

# for match in matches:
#     print(f"{match[0].__repr__()}: {match[1]}")





# matcher = ProductMatcher(product_file=(config_paths.PRODUCT_FILE_PATH, True), adjust_at=500)
# matches = matcher.match(text='popcorn', category=ProductCategory.SLANE_SNACKY_SEMIENKA, limit=100)


# for match in matches:
#     print(f"{match[0].__repr__()} : {match[1]}")

# print(fuzz.partial_token_ratio("penne cestoviny este nieco", "BILLA Penne rigate 500g".lower()))
# print("TERMINATED")


#product.__repr__()

# markets = Market.markets(market_file=config_paths.MARKET_FILE_PATH, MF_header=True, CF_header=True)

# for market in markets:
#     market.__str__()


