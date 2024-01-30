import json

CONFIG_FILE_PATH = "./.config.json"

with open(file=CONFIG_FILE_PATH, mode='r') as config_file:
    PATHS = json.load(config_file)

RESOURCES = PATHS["resources"]



DATA = PATHS["resources"]["data"]

MARKET_FILE = DATA["markets"]
PRODUCT_FILE = DATA["products"]
CATEGORY_FILE = DATA["categories"]
QUERY_STRING_FILE = DATA["category_query_strings"]
MARKET_HUB_FILE = DATA["market_hub"]




GUI = PATHS["resources"]["gui"]

NEW_ITEM_ICON = GUI["new_item_icon"]
SHOPPING_CART_ICON = GUI["shopping_cart_icon"]