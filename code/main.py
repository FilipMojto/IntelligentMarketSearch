import requests
from shopping import *
from bs4 import BeautifulSoup
from thefuzz import fuzz
from tkinter import *
#import tkinter as tk
#import math




# def main():
#     print(compare("tesco", "tsvcosddsasaddsa"))


#     #URL = 'https://www.tesco.com'
#     #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
#     #page = requests.get(URL)#, headers=headers)

#     print("hellow")



if __name__ == "__main__":
    root = Tk()
    root.title("AOSS Application v2.0.1")

    #print(algorithm.match_strings("tesco", "TesCo", case_sensitive=True))
    # ha = " tesco"
    # ha2 = "tesco"
    # print(f"similarity: {fuzz.ratio(ha, ha2)}")
    #print("Launching new market...")

    market_base = MarketViewer()
    market_base.load_markets()
    
    root.mainloop()
    #for market in market_base.search_market("bill"):
    #    print(f"Name: {market['market']}")
    #    print(f"Match: {market['match']}")

    #print(algorithm.match_strings('tesco', ' tesco'))

    #market_base.search_market(' tesco')

    #print(market_base.get_market('lidddsdsdsdl tesco').name)


    print("Program terminated successfully!")


