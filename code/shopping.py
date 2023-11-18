from marketing import Market, Product
import algorithm
from typing import List, Dict

class MarketViewer:
    #MARKETS_SRC_FILE_PATH = "./resources/markets.csv"
    #PRODUCTS_SRC_FILE_PATH = "./resources/markets.csv"
    #SUBSTITUTIONS_SRC_FILE_PATH = "./resources/markets.csv"

    def load_markets(self):

        with open(self.__MARKETS_FILE_PATH, 'r') as market_f:

            #here we skip the header of the file
            market_f.readline()

            for line in market_f:
                  
                #we process each row by splitting it by the delimiter
                record = line.rstrip().split(self.__DELIMITER)

                market = Market(record[0], record[1])
                self.__markets.append(market)
        
        print(f"Succesfully loaded {len(self.__markets)} markets!")

    def get_market(self, index : int) -> Market:
       return self.__markets[index]

    def search_market(self, name: str) -> List[Dict]:
        
        if len(self.__markets) == 0:
            print("No loaded markets found! Try loading them or check for the resource files.")
            return []
        
        match_results = []
        #match_results.append({'market': '', 'match': -1})

        for market in self.__markets:
            match_result = {'market': market.name, 'match': algorithm.match_strings(name, market.name)}

            if 'match' not in match_result:
                print(f"now: {market.name}")
                #match_results.append(match_result)

            match_results.append(match_result)
            
        match_results.sort(key=lambda x: x['match'], reverse=True)
        return match_results

    def __init__(self, markets_file_path: str = "./resources/markets.csv",
            products_file_path: str = "./resources/markets.csv",
            substitutions_file_path: str = "./resources/markets.csv",
            DELIMITER=',') -> None: 
        
        self.__MARKETS_FILE_PATH = markets_file_path
        self.__PRODUCTS_FILE_PATH = products_file_path
        self.__SUBSTITUTIONS_FILE_PATH = substitutions_file_path
        self.__DELIMITER = DELIMITER
        
        self.__markets: List[Market] = []