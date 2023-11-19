from marketing import Market, Product, EAN
from typing import List, Dict
from exceptions import InvalidFileFormatError
from thefuzz import fuzz

class MarketViewer:
    #MARKETS_SRC_FILE_PATH = "./resources/markets.csv"
    #PRODUCTS_SRC_FILE_PATH = "./resources/markets.csv"
    #SUBSTITUTIONS_SRC_FILE_PATH = "./resources/markets.csv"
    
    #Constant static configuration, set by the developer
    #File configuration, resource files must follow this
    DELIMITER = ','
    PRODUCT_COL_COUNT = 5

    def load_markets(self):

        # first, we need to load all registered shops from the
        # source file
        with open(self.__MARKETS_FILE_PATH, 'r') as market_f:

            #skipping the header of the file
            market_f.readline()

            for line in market_f:
                  
                #we process each row by splitting it by the delimiter
                record = line.rstrip().split(self.__DELIMITER)

                if not record[0].isdigit():
                    raise TypeError("ID of a market record must be integer!")

                market = Market(int(record[0]), record[1])
                self.__markets.append(market)
        
        print(f"Succesfully loaded {len(self.__markets)} markets!")

        # now, we need to load all registered products and assign
        # each to the corresponding market
        with open(self.__PRODUCTS_FILE_PATH, 'r') as product_f:
            
            #skipping the header of the file
            product_f.readline()

            for line in product_f:
                record = line.rstrip().split(self.__DELIMITER)

                if len(record) != self.PRODUCT_COL_COUNT:
                    raise InvalidFileFormatError("Invalid amount of columns in the product file!")
                
                market = ''
                found = False

                for market in self.__markets:
                    if market.get_ID() == int(record[-1]):
                        market.register_product(Product(ID=int(record[0]), ean=EAN(record[1]), name=record[2], price=float(record[3])))
                        print("FOUND!")
                        found = True
                        break
                
                if not found:
                    print(f"No market found for Product {record[0]}")

    def get_market(self, index : int) -> Market:
       return self.__markets[index]

    def get_market(self, name : str) -> Market:
        if not isinstance(name, str):
            raise TypeError("Invalid type for a market name! String needed.")
        
        max_match : float = 0
        result : Market = None
        for market in self.__markets:
            match : float = fuzz.ratio(market.name, name) #.match_strings(market.name, name)

            if match > max_match:
                max_match = match
                result = market
        
        if result is None:
            print("No market found! Use search_market() to get the available markets.")

        return result

    def search_market(self, name: str) -> None:
        
        if len(self.__markets) == 0:
            print("No loaded markets found! Try loading them or check for the resource files.")
            return []
        
        match_results = []
        #match_results.append({'market': '', 'match': -1})

        for market in self.__markets:
            match_result = {'market': market.name, 'match': fuzz.ratio(name, market.name)} # algorithm.match_strings(name, market.name)}

            if 'match' not in match_result:
                print(f"now: {market.name}")
                #match_results.append(match_result)

            match_results.append(match_result)
            
        match_results.sort(key=lambda x: x['match'], reverse=True)

        for market in match_results:
           print(f"Name: {market['market']}")
           print(f"Match: {market['match']}")

    def __init__(self, markets_file_path: str = "./resources/markets.csv",
            products_file_path: str = "./resources/products.csv",
            alternatives_file_path: str = "./resources/alternatives.csv",
            DELIMITER=',') -> None: 
    

        self.__MARKETS_FILE_PATH = markets_file_path
        self.__PRODUCTS_FILE_PATH = products_file_path
        self.__ALTERNATIVES_FILE_PATH = alternatives_file_path
        self.__DELIMITER = DELIMITER
        
        self.__markets: List[Market] = []