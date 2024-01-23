from matching import ProductMatcher
import config_paths

matcher = ProductMatcher(product_file=config_paths.PRODUCT_FILE_PATH)

products = matcher.match(text="Energetak", headerless=False, limit=10, category=)

for product in products:
    product[0].__str__()
