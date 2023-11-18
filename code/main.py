import requests
from shopping import *
from bs4 import BeautifulSoup
#import math


def compare(str1: str, str2 : str) -> float:
    len_1 = len(str1)
    len_2 = len(str2)

    min_len = min(len_1, len_2)
    fragment = 1/max(len_1, len_2)

    #min_len = min(len_1, len_2)
    i = 0
    match = 0

    for i in range(0, min_len):
        if str1[i] == str2[i]:
            match += fragment

    return round(match, 2)




# def main():
#     print(compare("tesco", "tsvcosddsasaddsa"))


#     #URL = 'https://www.tesco.com'
#     #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
#     #page = requests.get(URL)#, headers=headers)

#     print("hellow")



if __name__ == "__main__":

    print("Launching new market...")

    market_base = MarketViewer()
    market_base.load_markets()
    
    for market in market_base.search_market("bill"):
        print(f"Name: {market['market']}")
        print(f"Match: {market['match']}")


    #market = Market("Tesco")

    #print(f"Market \"{market.name}\" successfully launched!")

    #market.register_product

    print("now")




