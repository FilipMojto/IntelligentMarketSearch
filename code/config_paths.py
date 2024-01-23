import json

CONFIG_FILE_PATH = "./.config.json"

with open(file=CONFIG_FILE_PATH, mode='r') as config_file:
    PATHS = json.load(config_file)

RESOURCES = PATHS["resources"]

DATA = PATHS["resources"]["data"]

MARKET_FILE_PATH = PATHS["resources"]["data"]["markets"]
PRODUCT_FILE_PATH = PATHS["resources"]["data"]["products"]
PRODUCT_HASH_FILE_PATH = PATHS['resources']["data"]["product_hashes"]

GUI = PATHS["resources"]["gui"]

NEW_ITEM_ICON = GUI["new_item_icon"]
SHOPPING_CART_ICON = GUI["shopping_cart_icon"]