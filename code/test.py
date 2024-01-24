from shopping import Market, Product
from product_scraping import ProductScraper
import config_paths

# market = Market.market(ID=1, market_file=config_paths.MARKET_FILE_PATH, MF_header=True, CF_header=True)
# market.for_registration(product=Product(name="KAAJA", price=12.3, approximation=1), header=True)
# market.register_products()

# print("END")

market: Market = Market.market(ID=3, market_file=config_paths.MARKET_FILE_PATH, header=True)
print(market.__repr__())
market.buffer(500)

scraper = ProductScraper(market=market, session_limit=6)
scraper.scrape_all(register=True, _print=True)

market.register_products()

print("TERMINATED")


#product.__repr__()

# markets = Market.markets(market_file=config_paths.MARKET_FILE_PATH, MF_header=True, CF_header=True)

# for market in markets:
#     market.__str__()


